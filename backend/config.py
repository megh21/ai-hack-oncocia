"""Centralized configuration for the grant scraper."""

SCRAPER_USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/124.0.0.0 Safari/537.36"
)

REQUEST_TIMEOUT_SECONDS = 15
PLAYWRIGHT_NAVIGATION_TIMEOUT_MS = 15000
PLAYWRIGHT_RENDER_WAIT_MS = 3000

HEALTHWELL_DISEASE_FUNDS_URL = "https://www.healthwellfoundation.org/disease-funds/"
HEALTHWELL_PATIENTS_URL = "https://www.healthwellfoundation.org/patients/"
TOTALASSIST_FUNDS_URL = "https://totalassist.org/funds/"
NEEDYMEDS_DIAGNOSIS_ASSISTANCE_URL = "https://www.needymeds.org/search-programs"
NEEDYMEDS_HOME_URL = "https://www.needymeds.org/"
RXASSIST_SEARCH_RESULTS_URL = "https://www.rxassist.org/patients/search-results"

ALLOWED_SOURCE_URLS = {
    HEALTHWELL_DISEASE_FUNDS_URL,
    HEALTHWELL_PATIENTS_URL,
    TOTALASSIST_FUNDS_URL,
    NEEDYMEDS_DIAGNOSIS_ASSISTANCE_URL,
    NEEDYMEDS_HOME_URL,
    RXASSIST_SEARCH_RESULTS_URL,
}