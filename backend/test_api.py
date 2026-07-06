import requests
import time
import json
import sys

BASE_URL = "http://127.0.0.1:8000"

def print_header(title):
    print(f"\n{'='*50}\n{title}\n{'='*50}")

def test_health():
    print_header("Testing Health Check")
    url = f"{BASE_URL}/api/health"
    try:
        response = requests.get(url, timeout=5)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Failed: {e}")

def test_mcp_openfda():
    print_header("Testing MCP OpenFDA (Generic Check)")
    url = f"{BASE_URL}/api/mcp/openfda/generic"
    params = {"brand_name": "Hydroxyurea"}
    try:
        response = requests.get(url, params=params, timeout=10)
        print(f"Status Code: {response.status_code}")
        print(f"Response:\n{json.dumps(response.json(), indent=2)}")
    except Exception as e:
        print(f"Failed: {e}")

def test_mcp_grants_agent():
    print_header("Testing MCP Grants Agent (Playwright/Web Scraper)")
    url = f"{BASE_URL}/api/mcp/grants/agent"
    params = {"diagnosis": "acute myeloid leukemia"}
    print("This might take a minute as it spins up a browser and agent...")
    try:
        response = requests.get(url, params=params, timeout=60)
        print(f"Status Code: {response.status_code}")
        print(f"Response:\n{json.dumps(response.json(), indent=2)}")
    except Exception as e:
        print(f"Failed: {e}")

def test_complete_workflow():
    print_header("Testing Complete Workflow (/api/intake)")
    url = f"{BASE_URL}/api/intake"
    payload = {
        "drug": "Hydroxyurea",
        "dosage": "500mg twice daily",
        "diagnosis": "acute myeloid leukemia"
    }
    print(f"Payload: {payload}")
    print("This runs both the clinical analyzer and the grants agent. May take a minute or two...")
    try:
        response = requests.post(url, json=payload, timeout=120)
        print(f"Status Code: {response.status_code}")
        print(f"Response:\n{json.dumps(response.json(), indent=2)}")
    except Exception as e:
        print(f"Failed: {e}")

if __name__ == "__main__":
    print("Starting tests...")
    
    test_health()
    
    # Adding slight delay between tests to respect any rate limits
    time.sleep(2)
    test_mcp_openfda()
    
    time.sleep(2)
    test_mcp_grants_agent()
    
    time.sleep(2)
    test_complete_workflow()
    
    print("\nTests complete!")

    #another triplet { "drug": "Tretinoin", "dosage": "10mg capsules, twice daily (dosed by body surface area)", "diagnosis": "acute promyelocytic leukemia" }