"""
Non-Profit Grant Scraper Tool for the Grant Navigator Agent.

Strategy & Limitations:
- HealthWell Foundation: The fund listing is primarily JS-rendered. We scrape the
  static HTML for any fund tiles that may exist, and provide the direct URL if not found.
- TotalAssist (PAN Foundation successor): Also JS-rendered. We scrape static HTML and
  provide a fallback with the direct URL.
- RxAssist: A static-HTML pharmaceutical assistance directory. Fully scrapable.
- NeedyMeds Diagnosis-Based Assistance: Searchable via their site.

⚠️ Important: HealthWell and TotalAssist render fund OPEN/CLOSED status via JavaScript.
   For a production system, a headless browser (Playwright/Selenium) would be needed.
   The scraper returns the direct URLs and all eligibility requirements as a fallback
   so the agent can inform the patient even when live status can't be extracted.

All tools return a consistent schema:
{
    "foundation": str,
    "cancer_type_searched": str,
    "open_funds": list[dict],
    "closed_funds": list[dict],
    "direct_url": str,           # Always provided so patients can check manually
    "error": str | None
}
"""
import re
import requests
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Non-Profit Grant Scraper")

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    )
}


def _normalize_status(text: str) -> str:
    """Normalize fund status text to OPEN, CLOSED, or WAITLISTED."""
    t = text.strip().upper()
    if "OPEN" in t:
        return "OPEN"
    if "WAITLIST" in t:
        return "WAITLISTED"
    if "CLOSED" in t or "TEMPORARILY" in t:
        return "CLOSED"
    return t


def _match_cancer_type(fund_name: str, cancer_type: str) -> bool:
    """Check if a cancer type appears in the fund name (case-insensitive)."""
    cancer_keywords = cancer_type.lower().split()
    fund_lower = fund_name.lower()
    # Match if ANY significant keyword appears (skip common words)
    stop_words = {"cancer", "the", "a", "an", "and", "or", "of", "for"}
    sig_keywords = [kw for kw in cancer_keywords if kw not in stop_words]
    if not sig_keywords:
        sig_keywords = cancer_keywords
    return any(kw in fund_lower for kw in sig_keywords)


def _scrape_healthwell(cancer_type: str) -> dict:
    """
    Scrape HealthWell Foundation disease funds page using Playwright.
    HealthWell renders funds via JavaScript, so a headless browser is required.
    """
    url = "https://www.healthwellfoundation.org/disease-funds/"
    open_funds = []
    closed_funds = []
    
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            # Wait for DOM to load, then wait 3 seconds for client-side JS to render the funds
            page.goto(url, wait_until="domcontentloaded", timeout=15000)
            page.wait_for_timeout(3000)
            
            # The page is now fully rendered. Grab the HTML.
            html = page.content()
            browser.close()
            
        soup = BeautifulSoup(html, "lxml")

        # HealthWell typically renders funds in lists, tiles, or divs.
        fund_tiles = soup.find_all(
            lambda tag: tag.name in ["li", "div", "article", "a"]
            and any(c in tag.get("class", []) for c in ["fund", "disease", "tile", "card"])
        )
        
        if not fund_tiles:
            # Fallback if specific classes aren't found
            fund_tiles = soup.find_all("a", href=re.compile(r"fund|disease", re.I))

        matched = []
        for tile in fund_tiles:
            text = tile.get_text(" ", strip=True)
            if _match_cancer_type(text, cancer_type):
                status_match = re.search(
                    r"\b(open|closed|waitlist(?:ed)?|temporarily closed)\b",
                    text, re.IGNORECASE
                )
                status = _normalize_status(status_match.group(0)) if status_match else "UNKNOWN"
                fund_entry = {
                    "fund_name": text[:120],
                    "status": status,
                    "source": url,
                    "foundation": "HealthWell Foundation"
                }
                matched.append(fund_entry)
                if status == "OPEN":
                    open_funds.append(fund_entry)
                else:
                    closed_funds.append(fund_entry)

        return {
            "foundation": "HealthWell Foundation",
            "cancer_type_searched": cancer_type,
            "open_funds": open_funds,
            "closed_funds": closed_funds,
            "error": None if matched else "No matching funds found on HealthWell (checked via Playwright)."
        }

    except Exception as e:
        return {
            "foundation": "HealthWell Foundation",
            "cancer_type_searched": cancer_type,
            "open_funds": [],
            "closed_funds": [],
            "error": f"Playwright scrape failed: {str(e)}"
        }


def _scrape_totalassist(cancer_type: str) -> dict:
    """
    Scrape TotalAssist (successor to PAN Foundation) for open oncology funds using Playwright.
    """
    url = "https://totalassist.org/funds/"
    open_funds = []
    closed_funds = []
    
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            # Wait for DOM to load, then wait 3 seconds for client-side JS to render the funds
            page.goto(url, wait_until="domcontentloaded", timeout=15000)
            page.wait_for_timeout(3000)
            
            html = page.content()
            browser.close()
            
        soup = BeautifulSoup(html, "lxml")

        # TotalAssist renders fund tiles with status
        all_text_blocks = soup.find_all(
            lambda tag: tag.name in ["li", "div", "article", "section", "p"]
            and _match_cancer_type(tag.get_text(" ", strip=True), cancer_type)
            and len(tag.get_text(" ", strip=True)) < 300
        )

        for block in all_text_blocks:
            text = block.get_text(" ", strip=True)
            status_match = re.search(
                r"\b(open|closed|waitlist(?:ed)?|not accepting)\b",
                text, re.IGNORECASE
            )
            status = _normalize_status(status_match.group(0)) if status_match else "UNKNOWN"
            fund_entry = {
                "fund_name": text[:120],
                "status": status,
                "source": url,
                "foundation": "TotalAssist (formerly PAN Foundation)"
            }
            if status == "OPEN":
                open_funds.append(fund_entry)
            elif status in ("CLOSED", "WAITLISTED"):
                closed_funds.append(fund_entry)

        return {
            "foundation": "TotalAssist (formerly PAN Foundation)",
            "cancer_type_searched": cancer_type,
            "open_funds": open_funds,
            "closed_funds": closed_funds,
            "error": None if (open_funds or closed_funds) else "No matching funds found on TotalAssist (checked via Playwright)."
        }

    except Exception as e:
        return {
            "foundation": "TotalAssist (formerly PAN Foundation)",
            "cancer_type_searched": cancer_type,
            "open_funds": [],
            "closed_funds": [],
            "error": f"Playwright scrape failed: {str(e)}"
        }


def _scrape_needymeds(cancer_type: str) -> dict:
    """
    Scrape NeedyMeds.org Diagnosis-Based Assistance search.
    NeedyMeds does NOT have a public API. The search is a POST form.
    We attempt a GET with the encoded search term, but return the direct URL
    as a fallback since their site may block automated requests.
    """
    # NeedyMeds uses a search form — the correct approach is to direct users there
    direct_url = f"https://www.needymeds.org/diagnosis-assistance?diag={cancer_type.replace(' ', '+')}"
    base_url = "https://www.needymeds.org/diagnosis-assistance"

    try:
        resp = requests.get(
            base_url,
            params={"diag": cancer_type},
            headers=HEADERS,
            timeout=15
        )
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "lxml")

        open_funds = []
        # Look for program listings
        program_blocks = soup.find_all(
            lambda tag: tag.name in ["li", "div", "tr", "article"]
            and _match_cancer_type(tag.get_text(" ", strip=True), cancer_type)
            and 15 < len(tag.get_text(" ", strip=True)) < 400
        )
        for block in program_blocks:
            text = block.get_text(" ", strip=True)
            open_funds.append({
                "fund_name": text[:150],
                "status": "LISTED",
                "source": direct_url,
                "foundation": "NeedyMeds"
            })

        return {
            "foundation": "NeedyMeds",
            "cancer_type_searched": cancer_type,
            "open_funds": open_funds,
            "closed_funds": [],
            "direct_url": direct_url,
            "error": None if open_funds else (
                f"NeedyMeds returned no matching programs for '{cancer_type}'. "
                f"Visit directly: {direct_url}"
            )
        }

    except requests.exceptions.RequestException as e:
        return {
            "foundation": "NeedyMeds",
            "cancer_type_searched": cancer_type,
            "open_funds": [],
            "closed_funds": [],
            "direct_url": direct_url,
            "error": f"Request failed: {str(e)}. Visit: {direct_url}"
        }


def _get_rxassist(cancer_type: str) -> dict:
    """
    RxAssist (rxassist.org) is a static-HTML directory of pharmaceutical patient
    assistance programs. We search it for programs related to the cancer type.
    """
    direct_url = "https://www.rxassist.org/patients/search-results"
    try:
        resp = requests.get(
            "https://www.rxassist.org/patients/search-results",
            params={"pSearch": cancer_type},
            headers=HEADERS,
            timeout=15
        )
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "lxml")

        open_funds = []
        result_rows = soup.find_all(["li", "div", "tr"], limit=30)
        for row in result_rows:
            text = row.get_text(" ", strip=True)
            if _match_cancer_type(text, cancer_type) and 15 < len(text) < 300:
                open_funds.append({
                    "fund_name": text[:150],
                    "status": "LISTED",
                    "source": direct_url,
                    "foundation": "RxAssist"
                })

        return {
            "foundation": "RxAssist",
            "cancer_type_searched": cancer_type,
            "open_funds": open_funds,
            "closed_funds": [],
            "direct_url": direct_url,
            "error": None if open_funds else f"No programs found for '{cancer_type}' on RxAssist."
        }
    except requests.exceptions.RequestException as e:
        return {
            "foundation": "RxAssist",
            "cancer_type_searched": cancer_type,
            "open_funds": [],
            "closed_funds": [],
            "direct_url": direct_url,
            "error": f"Request failed: {str(e)}"
        }


@mcp.tool()
def search_grants(cancer_type: str) -> dict:
    """
    Searches multiple non-profit patient assistance foundations for open grants
    matching the patient's cancer type.

    Searches:
    - HealthWell Foundation (disease-funds page)
    - TotalAssist / PAN Foundation (funds page)
    - NeedyMeds (search)

    Args:
        cancer_type: The patient's cancer type (e.g., 'breast cancer', 'lung cancer').

    Returns:
        A structured dict with open_funds, closed_funds, and per-source results.
    """
    results = {}
    all_open = []
    all_closed = []

    # Query each source
    for scraper_fn, key in [
        (_scrape_healthwell, "healthwell"),
        (_scrape_totalassist, "totalassist"),
        (_scrape_needymeds, "needymeds"),
        (_get_rxassist, "rxassist"),
    ]:
        result = scraper_fn(cancer_type)
        results[key] = result
        all_open.extend(result.get("open_funds", []))
        all_closed.extend(result.get("closed_funds", []))

    # Always include direct URLs as fallback for JS-rendered sites
    direct_urls = {
        "HealthWell Foundation": "https://www.healthwellfoundation.org/disease-funds/",
        "TotalAssist (PAN Foundation)": "https://totalassist.org/funds/",
        "NeedyMeds": f"https://www.needymeds.org/diagnosis-assistance?diag={cancer_type.replace(' ', '+')}",
        "RxAssist": "https://www.rxassist.org/patients/search-results"
    }

    return {
        "cancer_type_searched": cancer_type,
        "total_open_funds_found": len(all_open),
        "total_closed_funds_found": len(all_closed),
        "open_funds": all_open,
        "closed_funds": all_closed,
        "per_source_results": results,
        "direct_urls_for_manual_check": direct_urls,
        "disclaimer": (
            "Grant availability changes daily. HealthWell and TotalAssist render fund status "
            "via JavaScript — use the direct_urls_for_manual_check links to verify current status. "
            "Always confirm directly with the foundation before applying."
        )
    }


@mcp.tool()
def check_eligibility_requirements(foundation_name: str, cancer_type: str) -> dict:
    """
    Provides known eligibility requirements for major oncology assistance foundations.
    This is based on commonly published criteria (e.g., income limits as % of FPL).

    Args:
        foundation_name: The name of the foundation (e.g., 'HealthWell', 'PAN Foundation').
        cancer_type: The cancer type to check requirements for.

    Returns:
        Known eligibility criteria and application guidance.
    """
    # Static knowledge base of common eligibility requirements
    # These are publicly published and do not constitute legal advice
    known_requirements = {
        "healthwell": {
            "income_limit_fpl_pct": 500,
            "income_limit_description": "Generally up to 500% of the Federal Poverty Level (FPL)",
            "us_resident_required": True,
            "insurance_required": True,
            "insurance_note": "Must have insurance (Medicare, Medicaid, or private) for most funds",
            "application_url": "https://www.healthwellfoundation.org/patients/",
            "phone": "(800) 675-8416",
        },
        "pan foundation": {
            "income_limit_fpl_pct": 400,
            "income_limit_description": "Generally up to 400% of the Federal Poverty Level (FPL)",
            "us_resident_required": True,
            "insurance_required": True,
            "insurance_note": "Must have insurance to qualify for most PAN/TotalAssist programs",
            "application_url": "https://totalassist.org/funds/",
            "phone": "(866) 316-7263",
        },
        "totalassist": {
            "income_limit_fpl_pct": 400,
            "income_limit_description": "Generally up to 400% of the Federal Poverty Level (FPL)",
            "us_resident_required": True,
            "insurance_required": True,
            "application_url": "https://totalassist.org/funds/",
            "phone": "(866) 316-7263",
        },
        "needymeds": {
            "income_limit_fpl_pct": None,
            "income_limit_description": "Varies by program — NeedyMeds is a directory, not a foundation",
            "us_resident_required": True,
            "application_url": "https://www.needymeds.org/",
            "phone": None,
        }
    }

    key = foundation_name.lower().strip()
    for k, v in known_requirements.items():
        if k in key or key in k:
            return {
                "foundation": foundation_name,
                "cancer_type": cancer_type,
                "requirements": v,
                "disclaimer": (
                    "Eligibility requirements may change. Always verify current requirements "
                    "directly with the foundation before applying."
                )
            }

    return {
        "foundation": foundation_name,
        "cancer_type": cancer_type,
        "requirements": None,
        "error": (
            f"No pre-loaded eligibility data for '{foundation_name}'. "
            "Please check the foundation's website directly for current requirements."
        )
    }


if __name__ == "__main__":
    mcp.run()
