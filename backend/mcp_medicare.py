import json
import requests
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("CMS Medicare Part D Data")

# CMS Data API endpoint for "Medicare Part D Spending by Drug" (most recent available dataset)
# We use the dataset ID for the 2022 Part D Spending by Drug dataset:
# https://data.cms.gov/provider-summary-by-type-of-service/medicare-part-d-prescribers/medicare-part-d-spending-by-drug
# UUID for 2022 dataset: b0a538e1-58d3-4676-bacd-3bb3da4e9fa4
# Using the standard Data API endpoint:
CMS_API_URL = "https://data.cms.gov/data-api/v1/dataset/b0a538e1-58d3-4676-bacd-3bb3da4e9fa4/data"

@mcp.tool()
def get_medicare_spending(drug_name: str) -> dict:
    """
    Queries the CMS Medicare Part D Spending by Drug public use file.
    Returns national-level total spending, total claims, and average cost per claim.
    
    This provides real-world historical claims data (average spending) rather than 
    just the wholesale acquisition cost (NADAC).
    
    Args:
        drug_name: The generic or brand name of the drug (e.g., 'Ibrance', 'Palbociclib').
    """
    # The API is case-sensitive, and drug names in the dataset are typically UPPERCASE.
    drug_upper = drug_name.upper()
    
    try:
        # Search using the 'Brnd_Name' field first
        params_brand = {
            "filter[Brnd_Name]": drug_upper,
            "size": "50" # Fetch up to 50 matching rows
        }
        
        response = requests.get(CMS_API_URL, params=params_brand, timeout=15)
        response.raise_for_status()
        data = response.json()
        
        # If not found by brand name, try generic name 'Gnrc_Name'
        if not data:
            params_generic = {
                "filter[Gnrc_Name]": drug_upper,
                "size": "50"
            }
            response = requests.get(CMS_API_URL, params=params_generic, timeout=15)
            response.raise_for_status()
            data = response.json()

        if not data:
            return {
                "error": f"No Medicare Part D spending data found for drug: '{drug_name}'."
            }

        # The dataset can return multiple rows if there are different formulations
        # or manufacturers. We will aggregate them.
        total_claims = 0.0
        total_spending = 0.0
        
        formulations = []
        
        for row in data:
            try:
                # 'Tot_Clms' = Total Claims
                clms = float(row.get("Tot_Clms", 0))
                # 'Tot_Spndng' = Total Spending
                spnd = float(row.get("Tot_Spndng", 0))
                
                total_claims += clms
                total_spending += spnd
                
                formulations.append({
                    "brand_name": row.get("Brnd_Name"),
                    "generic_name": row.get("Gnrc_Name"),
                    "claims": clms,
                    "spending": spnd
                })
            except (ValueError, TypeError):
                continue
                
        if total_claims == 0:
            return {"error": f"Data found for '{drug_name}' but total claims was zero or missing."}
            
        avg_cost_per_claim = total_spending / total_claims

        return {
            "drug_searched": drug_name,
            "total_medicare_spending_usd": round(total_spending, 2),
            "total_medicare_claims": int(total_claims),
            "average_cost_per_claim_usd": round(avg_cost_per_claim, 2),
            "data_year": "2022", # Hardcoded based on the UUID dataset version
            "source": "CMS Medicare Part D Drug Spending Dashboard & Data",
            "formulations_found": len(formulations)
        }

    except requests.exceptions.RequestException as e:
        return {"error": f"CMS API request failed: {str(e)}"}

if __name__ == "__main__":
    mcp.run()
