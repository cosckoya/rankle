"""
Configuration settings for Rankle
"""

from pathlib import Path


# Base paths
BASE_DIR = Path(__file__).resolve().parent.parent
CONFIG_DIR = BASE_DIR / "config"
OUTPUT_DIR = BASE_DIR / "output"
REPORTS_DIR = BASE_DIR / "reports"

# Ensure directories exist
OUTPUT_DIR.mkdir(exist_ok=True)
REPORTS_DIR.mkdir(exist_ok=True)

# HTTP Settings
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
DEFAULT_TIMEOUT = 45
MAX_REDIRECTS = 10

# HTTP Headers
DEFAULT_HEADERS = {
    "User-Agent": USER_AGENT,
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "DNT": "1",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
}

# DNS Settings
DNS_TIMEOUT = 10
DNS_NAMESERVERS = ["8.8.8.8", "1.1.1.1"]

# SSL/TLS Settings
SSL_VERIFY = True
SSL_TIMEOUT = 10

# WAF Detection Settings
WAF_ACTIVE_DETECTION = True
WAF_MAX_PAYLOADS = 2  # Limit number of test payloads

# Certificate Transparency Settings
CRT_SH_URL = "https://crt.sh/"
CRT_SH_TIMEOUT = 30

# Subdomain Discovery Settings
MAX_SUBDOMAINS = 100

# Technology Signatures
TECH_SIGNATURES_FILE = CONFIG_DIR / "tech_signatures.json"

# Output Settings
JSON_INDENT = 2
SAVE_OUTPUT = True

# API Settings (for future extensions)
WHOIS_TIMEOUT = 30
GEO_API_TIMEOUT = 10

# Ethical Scanning Settings
ETHICAL_MODE = True
RATE_LIMIT_DELAY = 0.5  # seconds between requests
MAX_CONCURRENT_REQUESTS = 5

# Detection Thresholds
MINIMUM_DETECTION_CONFIDENCE = 0.2  # Minimum confidence for technology detection
CDN_DETECTION_THRESHOLD = 0.3  # Minimum confidence for CDN detection
WAF_DETECTION_THRESHOLD = 0.3  # Minimum confidence for WAF detection

# Display Limits
MAX_DISPLAY_TECHS = 10  # Maximum technologies to display in summary
MAX_DISPLAY_ORIGINS = 5  # Maximum origin IPs to display
MAX_DISPLAY_SUBDOMAINS = 6  # Maximum subdomains to display
MAX_DISPLAY_ITEMS = 3  # Default maximum items in truncated lists

# HTTP Response Limits
MAX_BODY_SIZE = 100000  # Maximum HTTP body size to analyze (100KB)
MAX_RESPONSE_TIME_SAMPLES = 10  # Number of response times to track for rate limiting

# Rate Limiting
MAX_RETRY_WAIT_SECONDS = 60.0  # Maximum time to wait on retry-after
RATE_LIMIT_DIMINISHING_FACTOR = 0.5  # Diminishing factor for confidence calculation
