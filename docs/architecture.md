# Architecture

This document describes Rankle's modular architecture, key design patterns, and API reference.

---

## Table of Contents

- [Directory Structure](#directory-structure)
- [Design Principles](#design-principles)
- [Core Components](#core-components)
- [Module System](#module-system)
- [Detector System](#detector-system)
- [Configuration Management](#configuration-management)
- [API Reference](#api-reference)
- [Adding New Modules](#adding-new-modules)
- [Design Patterns](#design-patterns)

---

## Directory Structure

```text
rankle/
├── pyproject.toml          # Modern Python packaging (PEP 621)
├── main.py                 # Entry point
├── rankle/                 # Main package
│   ├── core/
│   │   ├── scanner.py      # RankleScanner - orchestrates all modules
│   │   └── session.py      # SessionManager - HTTP with retry logic & pooling
│   ├── modules/
│   │   ├── dns.py          # DNSAnalyzer - DNS enumeration
│   │   ├── ssl.py          # SSLAnalyzer - TLS certificate analysis
│   │   ├── subdomains.py   # SubdomainDiscovery - CT log enumeration
│   │   ├── whois.py        # WHOISLookup - domain registration info
│   │   ├── geolocation.py  # GeolocationLookup - IP/cloud detection
│   │   ├── http_fingerprint.py  # HTTPFingerprinter - concurrent scanning
│   │   └── security_headers.py  # SecurityHeadersAuditor
│   ├── detectors/          # Technology detectors
│   │   ├── technology.py   # CMS, frameworks, libraries
│   │   ├── cdn.py          # CDN detection (20+ providers)
│   │   ├── waf.py          # WAF detection (15+ solutions)
│   │   └── origin.py       # Origin discovery behind CDN/WAF
│   ├── utils/
│   │   ├── validators.py   # Domain/IP validation, input sanitization
│   │   ├── helpers.py      # save_json_file, truncate_list utilities
│   │   └── rate_limiter.py # Request rate limiting
│   └── reports/            # Report generation
├── config/
│   ├── settings.py         # Centralized configuration (timeouts, UA, DNS)
│   ├── patterns.py         # Cloud providers, subdomains, ASN patterns
│   └── tech_signatures.json # Technology detection signatures
├── tests/                  # Unit tests (pytest)
├── examples/               # Integration scripts
└── output/                 # Generated scan results
```

---

## Design Principles

### 1. Modular Architecture

Each module has a single, well-defined responsibility:
- `dns.py` - DNS queries only
- `ssl.py` - TLS certificate analysis only
- `scanner.py` - Orchestration only

**Benefits:**
- Easy to test individual components
- Simple to add new features
- Clear code organization
- Minimal coupling between modules

### 2. Lazy Initialization

Modules are initialized only when needed:

```python
class RankleScanner:
    def __init__(self, domain: str):
        self._dns_analyzer: DNSAnalyzer | None = None

    @property
    def dns_analyzer(self) -> DNSAnalyzer:
        if self._dns_analyzer is None:
            self._dns_analyzer = DNSAnalyzer(self.domain)
        return self._dns_analyzer
```

**Benefits:**
- Faster startup time
- Reduced memory usage
- Only pay for what you use

### 3. Centralized Configuration

All configuration in `config/` directory:
- `settings.py` - Timeouts, User-Agent, DNS servers
- `patterns.py` - Cloud providers, ASN patterns
- `tech_signatures.json` - CMS/framework signatures

**Benefits:**
- Single source of truth
- Easy to maintain and update
- Clear separation of code and data

### 4. Context Manager Support

Automatic resource cleanup:

```python
with RankleScanner(domain) as scanner:
    results = scanner.run_full_scan()
# Session automatically closed
```

### 5. Type Safety

Full type hints throughout codebase:

```python
# Modern Python 3.11+ syntax
def analyze(self) -> dict[str, Any]:  # ✅
def query(self) -> str | None:        # ✅

# Deprecated (not used in Rankle)
def analyze(self) -> Dict[str, Any]:  # ❌
def query(self) -> Optional[str]:     # ❌
```

---

## Core Components

### RankleScanner

**File:** `rankle/core/scanner.py:15`

Main orchestrator class that coordinates all reconnaissance modules.

**Key Features:**
- Context manager support (`with` statement)
- Lazy initialization of modules
- Centralized result aggregation
- Automatic resource cleanup

**Example Usage:**

```python
from rankle.core.scanner import RankleScanner

# With context manager (recommended)
with RankleScanner("example.com", verbose=True) as scanner:
    results = scanner.run_full_scan()
    print(results)

# Manual management
scanner = RankleScanner("example.com")
try:
    results = scanner.run_full_scan()
finally:
    scanner.close()
```

**Key Methods:**
- `run_full_scan() -> dict[str, Any]` - Execute all modules
- `close()` - Cleanup resources

### SessionManager

**File:** `rankle/core/session.py`

HTTP session manager with automatic retry logic and connection pooling.

**Features:**
- Automatic retry with exponential backoff (429, 500, 502, 503, 504)
- Connection pooling (10 connections, 20 max pool size)
- Realistic browser headers
- Configurable timeouts and retries
- Context manager support

**Example Usage:**

```python
from rankle.core.session import SessionManager

with SessionManager(timeout=45, retries=3) as session:
    response = session.get("https://example.com")
    if response:
        print(response.status_code)
        print(response.text)
```

**Retry Strategy:**
- Max retries: 3 (configurable)
- Backoff factor: 0.5s (exponential)
- Retry on: 429, 500, 502, 503, 504
- Allowed methods: HEAD, GET, OPTIONS, PUT, DELETE, TRACE, PATCH

---

## Module System

### DNSAnalyzer

**File:** `rankle/modules/dns.py:23`

**Purpose:** DNS enumeration using dnspython

**Queries:**
- A (IPv4 addresses)
- AAAA (IPv6 addresses)
- MX (Mail servers)
- NS (Name servers)
- TXT (Text records, SPF, DMARC)
- SOA (Start of Authority)
- CNAME (Canonical names)

**Custom Resolver:**
- Configurable nameservers (default: 8.8.8.8, 1.1.1.1)
- 10-second timeout per query
- NXDOMAIN and NoAnswer handling

### SSLAnalyzer

**File:** `rankle/modules/ssl.py`

**Purpose:** TLS/SSL certificate analysis

**Extracts:**
- Subject (CN, O, OU)
- Issuer information
- Validity dates
- Subject Alternative Names (SANs)
- TLS version support
- Cipher suites

### SubdomainDiscovery

**File:** `rankle/modules/subdomains.py`

**Purpose:** Subdomain discovery via Certificate Transparency logs

**Data Source:** crt.sh (public CT log database)

**Method:**
1. Query crt.sh API for domain certificates
2. Extract SANs from certificates
3. Deduplicate and filter results
4. Return unique subdomain list

### WHOISLookup

**File:** `rankle/modules/whois.py`

**Purpose:** Domain registration information

**Features:**
- Primary: python-whois library
- Fallback: Raw socket queries (port 43)
- Handles multiple WHOIS server responses

### GeolocationLookup

**File:** `rankle/modules/geolocation.py`

**Purpose:** IP geolocation and cloud provider detection

**Detects:**
- Country, city
- ISP/Organization
- ASN (Autonomous System Number)
- Cloud provider (14+ providers)
- Confidence scoring (low/medium/high)

### HTTPFingerprinter

**File:** `rankle/modules/http_fingerprint.py`

**Purpose:** HTTP fingerprinting with concurrent scanning

**Features:**
- 8 fingerprinting techniques
- ThreadPoolExecutor for parallel requests
- Server version extraction
- HTTP methods testing
- API endpoint discovery
- Cookie analysis

### SecurityHeadersAuditor

**File:** `rankle/modules/security_headers.py`

**Purpose:** HTTP security headers audit

**Checks:**
- X-Frame-Options
- Content-Security-Policy
- Strict-Transport-Security
- X-Content-Type-Options
- X-XSS-Protection
- Referrer-Policy
- Permissions-Policy

---

## Detector System

### TechnologyDetector

**File:** `rankle/detectors/technology.py`

**Purpose:** CMS, frameworks, and library detection

**Features:**
- Signature-based matching
- Confidence scoring (0-100%)
- Version detection
- 30+ technologies supported

**Detection Methods:**
1. HTML pattern matching
2. JavaScript library detection
3. Meta tags analysis
4. Response headers
5. Cookie analysis

### CDNDetector

**File:** `rankle/detectors/cdn.py`

**Purpose:** CDN provider detection

**Providers:** 20+ including:
- TransparentEdge
- Cloudflare
- Akamai
- Fastly
- Amazon CloudFront
- Azure CDN
- Google Cloud CDN
- And more...

**Detection Methods:**
- HTTP headers (X-Cache, Server, Via)
- CNAME records
- Server response patterns

### WAFDetector

**File:** `rankle/detectors/waf.py`

**Purpose:** Web Application Firewall detection

**Solutions:** 15+ including:
- Cloudflare WAF
- Imperva/Incapsula
- PerimeterX
- DataDome
- Sucuri
- ModSecurity
- AWS WAF
- F5 BIG-IP ASM
- And more...

**Detection Methods:**
- Challenge pages
- Cookies (_px, visid_incap, etc.)
- HTTP headers
- Response patterns

### OriginDiscovery

**File:** `rankle/detectors/origin.py`

**Purpose:** Origin infrastructure discovery behind CDN/WAF

**Methods:**
1. Subdomain analysis (origin.*, direct.*, admin.*)
2. MX records (mail servers reveal origin network)
3. SPF/TXT records (authorized IP ranges)
4. SSL certificate SANs (direct-access domains)
5. Common patterns (api.*, backend.*, etc.)

**Output:**
- Origin IP addresses
- Direct-access domains
- Cloud provider identification
- Detection methods used

---

## Configuration Management

### settings.py

**File:** `config/settings.py`

**Global Configuration:**

```python
# HTTP Configuration
DEFAULT_TIMEOUT = 45        # Seconds (10-60 recommended)
MAX_RETRIES = 3             # Retry attempts
RATE_LIMIT_DELAY = 0.5      # Seconds between requests
MAX_CONCURRENT_REQUESTS = 5 # Parallel requests

# DNS Configuration
DNS_TIMEOUT = 10            # Seconds
DNS_NAMESERVERS = ["8.8.8.8", "1.1.1.1"]

# User-Agent
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36..."
```

### patterns.py

**File:** `config/patterns.py`

**Cloud Provider Patterns:**

```python
CLOUD_PROVIDERS = {
    "AWS": {
        "asns": [16509, 14618, 8987],
        "domains": [".amazonaws.com", ".aws.amazon.com"],
        "name_patterns": ["amazon", "aws"]
    },
    "Azure": {
        "asns": [8075, 8068],
        "domains": [".azure.com", ".microsoft.com"],
        "name_patterns": ["microsoft", "azure"]
    },
    # ... more providers
}
```

**Subdomain Patterns:**

```python
COMMON_SUBDOMAINS = [
    "www", "mail", "ftp", "admin",
    "origin", "direct", "api", "backend"
]
```

### tech_signatures.json

**File:** `config/tech_signatures.json`

**Technology Detection Signatures:**

```json
{
  "cms": {
    "WordPress": {
      "patterns": ["/wp-content/", "/wp-includes/", "/wp-json/"],
      "headers": {"X-Powered-By": "WordPress"},
      "confidence": 90
    },
    "Drupal": {
      "patterns": ["/core/misc/drupal.js", "/user/login"],
      "html_attributes": ["data-drupal-", "views-", "block-"],
      "confidence": 85
    }
  }
}
```

---

## API Reference

### Main Classes

#### `RankleScanner`

```python
class RankleScanner:
    def __init__(self, domain: str, verbose: bool = False):
        """
        Initialize scanner.

        Args:
            domain: Target domain to scan
            verbose: Enable verbose output
        """

    def run_full_scan(self) -> dict[str, Any]:
        """
        Execute all reconnaissance modules.

        Returns:
            Dictionary with complete scan results
        """

    def close(self) -> None:
        """Cleanup resources."""
```

#### `SessionManager`

```python
class SessionManager:
    def __init__(
        self,
        timeout: int = 45,
        retries: int = 3,
        backoff_factor: float = 0.5
    ):
        """
        Initialize HTTP session.

        Args:
            timeout: Request timeout in seconds
            retries: Maximum retry attempts
            backoff_factor: Exponential backoff factor
        """

    def get(self, url: str, **kwargs) -> requests.Response | None:
        """
        HTTP GET request with retry logic.

        Args:
            url: Target URL
            **kwargs: Additional requests parameters

        Returns:
            Response object or None on failure
        """
```

#### `DNSAnalyzer`

```python
class DNSAnalyzer:
    def __init__(
        self,
        domain: str,
        timeout: int = 10,
        nameservers: list[str] | None = None
    ):
        """
        Initialize DNS analyzer.

        Args:
            domain: Target domain
            timeout: Query timeout in seconds
            nameservers: Custom DNS servers (default: 8.8.8.8, 1.1.1.1)
        """

    def analyze(self) -> dict[str, Any]:
        """
        Perform complete DNS analysis.

        Returns:
            Dictionary with DNS records
        """
```

### Utility Functions

**File:** `rankle/utils/validators.py`

```python
def validate_domain(domain: str) -> bool:
    """
    Validate domain format.

    Args:
        domain: Domain name to validate

    Returns:
        True if valid, False otherwise
    """

def extract_domain(url: str) -> str:
    """
    Extract domain from URL.

    Args:
        url: Full URL or domain

    Returns:
        Clean domain name
    """

def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename for safe filesystem operations.

    Args:
        filename: Original filename

    Returns:
        Sanitized filename
    """
```

**File:** `rankle/utils/helpers.py`

```python
def save_json_file(data: dict[str, Any], filepath: str) -> None:
    """
    Save dictionary as formatted JSON.

    Args:
        data: Data to save
        filepath: Output file path
    """

def truncate_list(items: list, max_items: int = 3) -> str:
    """
    Truncate list for display with ellipsis.

    Args:
        items: List to truncate
        max_items: Maximum items to show

    Returns:
        Formatted string
    """
```

---

## Adding New Modules

### Step-by-Step Guide

#### 1. Create the Module

```python
# rankle/modules/new_module.py
from config.settings import DEFAULT_TIMEOUT

class NewModule:
    """
    Brief description of module purpose.

    Attributes:
        domain: Target domain
        timeout: Request timeout
    """

    def __init__(self, domain: str, timeout: int = DEFAULT_TIMEOUT):
        """
        Initialize module.

        Args:
            domain: Target domain
            timeout: Timeout in seconds
        """
        self.domain = domain
        self.timeout = timeout

    def analyze(self) -> dict[str, Any]:
        """
        Perform analysis.

        Returns:
            Analysis results
        """
        results = {
            "status": "success",
            "data": []
        }
        # Implementation here
        return results
```

#### 2. Add Lazy Initialization in Scanner

```python
# rankle/core/scanner.py
class RankleScanner:
    def __init__(self, domain: str):
        self._new_module: NewModule | None = None

    @property
    def new_module(self) -> NewModule:
        """Lazy initialization of NewModule."""
        if self._new_module is None:
            self._new_module = NewModule(self.domain)
        return self._new_module
```

#### 3. Integrate in run_full_scan()

```python
def run_full_scan(self) -> dict[str, Any]:
    """Execute all modules."""
    self.results["dns"] = self.dns_analyzer.analyze()
    self.results["ssl"] = self.ssl_analyzer.analyze()
    self.results["new_module"] = self.new_module.analyze()  # Add here
    return self.results
```

#### 4. Add Tests

```python
# tests/test_new_module.py
import pytest
from rankle.modules.new_module import NewModule

def test_new_module_initialization():
    """Test module initialization."""
    module = NewModule("example.com")
    assert module.domain == "example.com"

def test_new_module_analyze():
    """Test analyze method."""
    module = NewModule("example.com")
    results = module.analyze()
    assert "status" in results
    assert results["status"] == "success"
```

---

## Design Patterns

### 1. Lazy Initialization Pattern

**When:** Resource-intensive objects that may not be used

```python
@property
def expensive_analyzer(self) -> ExpensiveAnalyzer:
    if self._expensive_analyzer is None:
        self._expensive_analyzer = ExpensiveAnalyzer(self.domain)
    return self._expensive_analyzer
```

### 2. Context Manager Pattern

**When:** Resources that need cleanup (network connections, files)

```python
class ResourceManager:
    def __enter__(self):
        # Setup
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Cleanup
        self.close()
```

### 3. Strategy Pattern

**When:** Multiple algorithms for the same task

```python
class Detector:
    def detect(self, strategy: str) -> dict:
        strategies = {
            "headers": self._detect_via_headers,
            "content": self._detect_via_content,
            "cookies": self._detect_via_cookies
        }
        return strategies[strategy]()
```

### 4. Guard Clauses

**When:** Early validation and error handling

```python
def analyze(self, data: str | None) -> dict:
    # Guard clauses
    if not data:
        return {"error": "No data provided"}
    if not self.is_valid(data):
        return {"error": "Invalid data format"}

    # Main logic
    return self.process(data)
```

---

## Performance Optimizations

### 1. Connection Pooling

```python
# SessionManager uses connection pooling
session = requests.Session()
adapter = HTTPAdapter(
    pool_connections=10,
    pool_maxsize=20,
    max_retries=retry_strategy
)
```

### 2. Concurrent Scanning

```python
from concurrent.futures import ThreadPoolExecutor

with ThreadPoolExecutor(max_workers=5) as executor:
    futures = [executor.submit(check_path, path) for path in paths]
    results = [f.result() for f in futures]
```

### 3. Lazy Evaluation

Only initialize modules when actually used, saving startup time and memory.

---

**Next:** [Detection Capabilities](detection-capabilities.md)
