import requests
from datetime import datetime
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("CMS NADAC Cost Calculator")

# Official Data.Medicaid.gov DKAN API endpoint for NADAC
BASE_URL = "https://data.medicaid.gov/api/1/datastore/query/dfa2ab14-06c2-457a-9e36-5cb6d80f8d93/0"

@mcp.tool()
def get_baseline_cost(ndc_description: str, monthly_quantity: int) -> dict:
    """
    Queries the CMS NADAC dataset to calculate the baseline monthly acquisition cost.
    Tries an exact match first, and falls back to a partial match if nothing is found.
    
    Args:
        ndc_description: The description of the drug (e.g., brand name, dosage).
        monthly_quantity: The quantity of units prescribed per month.
    """
    # 1. Try exact match first
    params_exact = {
        "conditions[0][property]": "ndc_description",
        "conditions[0][value]": ndc_description.upper(),
        "conditions[0][operator]": "=",
        "sorts[0][property]": "effective_date",
        "sorts[0][order]": "desc",
        "limit": "1"
    }
    
    try:
        response = requests.get(BASE_URL, params=params_exact, timeout=10)
        response.raise_for_status()
        data = response.json()
        results = data.get("results", [])
        
        # 2. If no exact match, fallback to partial match
        if not results:
            params_partial = {
                "conditions[0][property]": "ndc_description",
                "conditions[0][value]": f"%{ndc_description.upper()}%",
                "conditions[0][operator]": "LIKE",
                "sorts[0][property]": "effective_date",
                "sorts[0][order]": "desc",
                "limit": "1"
            }
            response = requests.get(BASE_URL, params=params_partial, timeout=10)
            response.raise_for_status()
            data = response.json()
            results = data.get("results", [])
            
        if not results:
            return {"error": f"No pricing data found for: {ndc_description}"}
            
        record = results[0]
        nadac_per_unit = float(record.get("nadac_per_unit", 0))
        pricing_unit = record.get("pricing_unit", "Unknown")
        effective_date_str = record.get("effective_date", "")
        
        # Calculate worst-case baseline cost
        baseline_cost = nadac_per_unit * monthly_quantity
        
        # Check data freshness (older than 90 days?)
        warning = None
        if effective_date_str:
            # CMS typically returns ISO 8601 timestamps like "2024-05-22" or "2024-05-22T00:00:00.000"
            try:
                date_part = effective_date_str.split("T")[0]
                effective_date = datetime.strptime(date_part, "%Y-%m-%d")
                age_days = (datetime.now() - effective_date).days
                if age_days > 90:
                    warning = f"Pricing data is {age_days} days old (effective date: {date_part}). This may be outdated."
            except ValueError:
                pass
                
        return {
            "ndc_description_matched": record.get("ndc_description"),
            "nadac_per_unit": nadac_per_unit,
            "pricing_unit": pricing_unit,
            "monthly_quantity": monthly_quantity,
            "baseline_monthly_cost": round(baseline_cost, 2),
            "effective_date": effective_date_str,
            "warning": warning
        }
        
    except requests.exceptions.RequestException as e:
        return {"error": f"API request failed: {str(e)}"}

if __name__ == "__main__":
    mcp.run()
