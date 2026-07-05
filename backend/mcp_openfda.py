import requests
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("OpenFDA Clinical Mapper")

OPENFDA_URL = "https://api.fda.gov/drug/label.json"

def _query_openfda(params: dict) -> list:
    """Internal helper to query OpenFDA and return results list, or empty list on failure/404."""
    try:
        response = requests.get(OPENFDA_URL, params=params, timeout=10)
        if response.status_code == 404:
            return []
        response.raise_for_status()
        return response.json().get("results", [])
    except requests.exceptions.RequestException:
        return []


def _extract_openfda_block(result: dict, original_name: str) -> dict:
    """
    Safely extract the openfda block from a result.
    Handles the case where the block is missing (OTC, homeopathic, cosmetic drugs).
    """
    openfda = result.get("openfda", {})

    generic_name = openfda.get("generic_name", [])
    pharm_class_epc = openfda.get("pharm_class_epc", [])
    brand_name = openfda.get("brand_name", [])
    product_type = openfda.get("product_type", [])
    manufacturer = openfda.get("manufacturer_name", [])

    # Detect missing structured data (common in OTC, homeopathic, or cosmetic entries)
    is_otc_or_unstructured = (
        not generic_name
        or not pharm_class_epc
        or any("OTC" in pt.upper() for pt in product_type)
        or any("HOMEO" in pt.upper() for pt in product_type)
    )

    return {
        "brand_name": brand_name if brand_name else [original_name],
        "generic_name": generic_name if generic_name else ["N/A"],
        "pharm_class_epc": pharm_class_epc if pharm_class_epc else ["N/A"],
        "product_type": product_type,
        "manufacturer": manufacturer,
        "data_quality_warning": (
            "This drug entry lacks structured pharmacological data. It may be an OTC, "
            "homeopathic, or cosmetic product. For oncology specialty drugs, please verify "
            "the exact brand name (e.g., 'Ibrance', 'Tagrisso', 'Imbruvica')."
            if is_otc_or_unstructured else None
        )
    }


@mcp.tool()
def check_generic_equivalent(brand_name: str) -> dict:
    """
    Queries the FDA Drug Label API to return generic names and pharmacological class
    for a given brand-name prescription oncology drug.

    Filters to HUMAN PRESCRIPTION DRUG entries only to avoid OTC/homeopathic noise.
    Falls back to a broader search if the strict search yields no results.

    Args:
        brand_name: The brand name of the drug (e.g., 'Ibrance', 'Tagrisso').
    """
    # 1. Strict search: prescription drug + brand name
    strict_params = {
        "search": (
            f'openfda.brand_name:"{brand_name}" AND '
            f'openfda.product_type:"HUMAN PRESCRIPTION DRUG"'
        ),
        "limit": "1"
    }
    results = _query_openfda(strict_params)

    # 2. Fallback: search just by brand name if strict search failed
    if not results:
        fallback_params = {"search": f'openfda.brand_name:"{brand_name}"', "limit": "1"}
        results = _query_openfda(fallback_params)

    # 3. Fallback: try generic_name field
    if not results:
        generic_params = {
            "search": f'openfda.generic_name:"{brand_name}"',
            "limit": "1"
        }
        results = _query_openfda(generic_params)

    if not results:
        return {
            "error": (
                f"No FDA label data found for: '{brand_name}'. "
                "Please verify the drug name spelling or try the generic name."
            )
        }

    return _extract_openfda_block(results[0], brand_name)


@mcp.tool()
def verify_indication(drug_name: str, cancer_type: str) -> dict:
    """
    Parses the indications_and_usage field from the FDA Drug Label to verify
    whether a drug is approved for the given cancer type.

    Args:
        drug_name: The brand or generic name of the drug (e.g., 'Ibrance', 'palbociclib').
        cancer_type: The type of cancer to check (e.g., 'breast cancer', 'lung cancer').
    """
    # Try brand name first (prescription-only), then generic, then broad fallback
    search_queries = [
        (
            f'openfda.brand_name:"{drug_name}" AND '
            f'openfda.product_type:"HUMAN PRESCRIPTION DRUG"'
        ),
        f'openfda.brand_name:"{drug_name}"',
        f'openfda.generic_name:"{drug_name}"',
    ]

    results = []
    for query in search_queries:
        results = _query_openfda({"search": query, "limit": "1"})
        if results:
            break

    if not results:
        return {
            "error": (
                f"No FDA label data found for: '{drug_name}'. "
                "Please verify the drug name or try the generic name."
            )
        }

    result = results[0]
    openfda = result.get("openfda", {})
    product_type = openfda.get("product_type", [])

    indications_raw = result.get("indications_and_usage", [])
    indications_text = (
        " ".join(indications_raw) if isinstance(indications_raw, list)
        else str(indications_raw)
    )

    if not indications_text.strip():
        return {
            "drug_name": drug_name,
            "cancer_type": cancer_type,
            "is_indicated": False,
            "data_quality_warning": (
                "No indications_and_usage text found in the FDA label for this drug. "
                "This is common with OTC or homeopathic products."
            ),
            "indications_snippet": None
        }

    # Case-insensitive match of cancer type keywords in the indications text
    is_indicated = cancer_type.lower() in indications_text.lower()

    # Build snippet for the agent to reason over
    snippet = (
        indications_text[:600] + "..."
        if len(indications_text) > 600
        else indications_text
    )

    return {
        "drug_name": drug_name,
        "product_type": product_type,
        "cancer_type": cancer_type,
        "is_indicated": is_indicated,
        "indications_snippet": snippet,
        "data_quality_warning": (
            "This entry may be OTC or non-prescription. Oncology cost calculations "
            "are only valid for HUMAN PRESCRIPTION DRUG entries."
            if any("OTC" in pt.upper() for pt in product_type)
            else None
        )
    }


if __name__ == "__main__":
    # Initialize and run the server over stdio (compatible with ADK MCPToolset)
    mcp.run()
