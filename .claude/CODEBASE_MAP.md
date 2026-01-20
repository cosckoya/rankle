# Rankle Codebase Map (Token-Optimized)

**Purpose:** Quick reference for Claude Code to understand codebase structure without reading all files.

**Version:** 2.0 (Enhanced Detection)
**Last Updated:** 2026-01-20

---

## 📁 Directory Structure

```
rankle/
├── main.py                      # CLI entry point (argparse, output formatters)
├── rankle/
│   ├── __init__.py             # Package exports: RankleScanner
│   ├── core/                   # Core orchestration
│   │   ├── scanner.py          # RankleScanner class (795 lines) - main orchestrator
│   │   └── session.py          # SessionManager (195 lines) - HTTP client with retry
│   ├── modules/                # Reconnaissance modules
│   │   ├── dns.py              # DNS queries (191 lines)
│   │   ├── ssl.py              # TLS/SSL analysis (402 lines)
│   │   ├── subdomains.py       # Subdomain discovery (543 lines) - crt.sh integration
│   │   ├── whois.py            # WHOIS lookups (480 lines)
│   │   ├── geolocation.py      # IP geolocation (202 lines)
│   │   ├── http_fingerprint.py # HTTP fingerprinting (573 lines)
│   │   └── security_headers.py # Security header auditing (513 lines)
│   ├── detectors/              # Detection engines
│   │   ├── technology.py       # Technology detection (1179 lines) ⚠️ LARGE
│   │   ├── cdn.py              # CDN detection (549 lines)
│   │   ├── waf.py              # WAF detection (496 lines)
│   │   └── origin.py           # Origin IP discovery (447 lines)
│   ├── utils/                  # Utility functions
│   │   ├── validators.py       # Input validation (160 lines)
│   │   ├── confidence.py       # Confidence scoring (148 lines)
│   │   ├── rate_limiter.py     # Rate limiting (323 lines)
│   │   ├── favicon_hash.py     # Favicon fingerprinting (NEW v2.0)
│   │   ├── error_fingerprint.py # Error page analysis (NEW v2.0)
│   │   ├── js_extractor.py     # JS endpoint extraction (NEW v2.0)
│   │   ├── wordpress_plugins.py # WordPress detection (NEW v2.0)
│   │   └── cve_mapper.py       # CVE mapping (NEW v2.0)
│   └── reports/                # Output formatting
│       ├── text_report.py      # Human-readable output
│       └── json_report.py      # Machine-readable output
├── config/                     # Configuration files
│   ├── settings.py             # Global configuration
│   ├── patterns.py             # Cloud/ASN patterns
│   └── tech_signatures.json    # Technology signatures database
├── scripts/                    # Utility and demo scripts
│   ├── demo_enhanced_detection.py  # v2.0 feature demonstration
│   ├── verify_dependencies.py      # Dependency verification tool
│   └── README.md                   # Scripts documentation
├── tests/                      # Unit tests (pytest)
└── docs/                       # Documentation
    └── TECHNOLOGY_DETECTION_ENHANCEMENT.md  # v2.0 enhancement details
```

---

## 🎯 Key Classes and Their Locations

### Core Orchestration
- **RankleScanner** (`rankle/core/scanner.py:15`)
  - Lines: 795
  - Purpose: Main orchestrator, lazy module initialization
  - Key Methods: `run_full_scan()`, `run_basic_scan()`

- **SessionManager** (`rankle/core/session.py`)
  - Lines: 195
  - Purpose: HTTP client with retry logic and connection pooling
  - Key Methods: `get()`, `head()`, `options()`

### Detection Engines
- **TechnologyDetector** (`rankle/detectors/technology.py:647`)
  - Lines: 1179 total (class starts at 647)
  - Purpose: Multi-technique technology detection
  - Key Methods:
    - `detect()` - Traditional detection (headers, cookies, HTML)
    - `detect_enhanced()` - NEW v2.0: Wappalyzer, favicon, error pages, JS analysis
  - Detection Techniques:
    1. HTML pattern matching (800+ signatures)
    2. HTTP headers analysis
    3. Cookie analysis
    4. Meta tags parsing
    5. JavaScript globals detection
    6. Wappalyzer (3000+ signatures) - NEW v2.0
    7. Favicon hashing (mmh3) - NEW v2.0
    8. Error page fingerprinting - NEW v2.0
    9. JavaScript endpoint extraction - NEW v2.0
    10. WordPress plugin/theme detection - NEW v2.0

- **CDNDetector** (`rankle/detectors/cdn.py`)
  - Lines: 549
  - Purpose: Detect CDN providers (20+ supported)

- **WAFDetector** (`rankle/detectors/waf.py`)
  - Lines: 496
  - Purpose: Detect WAF solutions (15+ supported)

- **OriginDiscovery** (`rankle/detectors/origin.py`)
  - Lines: 447
  - Purpose: Find origin IPs behind CDN/WAF

### Utility Modules (NEW in v2.0)
- **Favicon Hashing** (`rankle/utils/favicon_hash.py`)
  - Purpose: Calculate mmh3 hash, map to known technologies
  - Database: 25+ known favicon hashes

- **Error Fingerprinting** (`rankle/utils/error_fingerprint.py`)
  - Purpose: Analyze 404/error pages for framework detection
  - Supports: Django, Laravel, Rails, Flask, FastAPI, etc.

- **JS Extractor** (`rankle/utils/js_extractor.py`)
  - Purpose: LinkFinder-style endpoint extraction
  - Detects: React, Vue, Angular, Next.js, Nuxt.js, etc.

- **WordPress Detection** (`rankle/utils/wordpress_plugins.py`)
  - Purpose: Passive plugin/theme enumeration
  - Database: 60+ plugins, 20+ themes

- **CVE Mapper** (`rankle/utils/cve_mapper.py`)
  - Purpose: Generate CPE identifiers and CVE search URLs
  - Sources: NVD, MITRE, CVEDetails, Vulners, Exploit-DB

---

## 🔍 Common Tasks and File Locations

### Adding New Technology Signatures
1. **JSON Signatures:** `config/tech_signatures.json`
2. **Runtime Signatures:** `rankle/detectors/technology.py` (line 42-646)
3. **Modern JS Frameworks:** `rankle/detectors/technology.py` (line 571-646)

### Adding New CDN/WAF Detection
1. **CDN Patterns:** `rankle/detectors/cdn.py` (class CDNDetector)
2. **WAF Patterns:** `rankle/detectors/waf.py` (class WAFDetector)

### Adding New Module to Scanner
1. Create module in `rankle/modules/` or `rankle/detectors/`
2. Add lazy property to `RankleScanner` (scanner.py)
3. Integrate in `run_full_scan()` method

### Modifying HTTP Behavior
- **Timeout/Retry:** `rankle/core/session.py` + `config/settings.py`
- **User-Agent:** `config/settings.py` (DEFAULT_USER_AGENT)
- **Rate Limiting:** `rankle/utils/rate_limiter.py`

### Input Validation
- **Domain Validation:** `rankle/utils/validators.py` (`validate_domain()`)
- **URL Sanitization:** `rankle/utils/validators.py` (`extract_domain()`)

---

## 🚀 Quick Reference: Where Things Happen

| Feature | Primary File | Secondary Files |
|---------|-------------|----------------|
| DNS Enumeration | modules/dns.py | config/settings.py (DNS_SERVERS) |
| Technology Detection | detectors/technology.py | config/tech_signatures.json, utils/* |
| CDN Detection | detectors/cdn.py | - |
| WAF Detection | detectors/waf.py | - |
| Origin Discovery | detectors/origin.py | modules/dns.py, detectors/cdn.py |
| SSL/TLS Analysis | modules/ssl.py | - |
| Security Headers | modules/security_headers.py | - |
| Subdomain Discovery | modules/subdomains.py | - |
| HTTP Fingerprinting | modules/http_fingerprint.py | core/session.py |
| WHOIS Lookups | modules/whois.py | - |
| Output Formatting | reports/* | main.py |

---

## 🎨 Code Patterns Used

### Lazy Initialization (Scanner)
```python
@property
def module_name(self) -> ModuleClass:
    if self._module_name is None:
        self._module_name = ModuleClass(self.domain)
    return self._module_name
```

### Detection Results Structure
```python
{
    "detected": bool,
    "technologies": [
        {
            "name": str,
            "category": str,
            "confidence": float,  # 0.0-1.0
            "version": str | None,
            "evidence": list[dict]
        }
    ]
}
```

### Confidence Scoring
- 0.9-1.0: High confidence (explicit signature match)
- 0.6-0.8: Medium confidence (multiple weak signals)
- 0.3-0.5: Low confidence (single weak signal)
- < 0.3: Filtered out (below MINIMUM_DETECTION_CONFIDENCE)

---

## 📊 Performance Characteristics

### File Sizes (Lines of Code)
- **Large (>500 lines):** technology.py (1179), scanner.py (795), http_fingerprint.py (573), cdn.py (549), subdomains.py (543), security_headers.py (513), waf.py (496)
- **Medium (200-500):** origin.py (447), ssl.py (402), rate_limiter.py (323), js_extractor.py (323), wordpress_plugins.py (300), cve_mapper.py (282), error_fingerprint.py (269), geolocation.py (202), session.py (195), dns.py (191)
- **Small (<200):** All other files

### Token Optimization Tips
1. For technology detection changes, read `technology.py` in chunks (file is 1179 lines)
2. Scanner orchestration: Start with `scanner.py:15-100` for class definition
3. For adding modules: Read `scanner.py:700-795` for integration patterns
4. Configuration changes: Read `config/settings.py` (usually <200 lines)

---

## 🔐 Security Considerations

### Input Validation
- All domains pass through `validators.validate_domain()`
- Regex-based, prevents injection attacks

### Network Safety
- All HTTP requests have timeouts
- Rate limiting between requests
- Realistic User-Agent
- No `shell=True` in subprocess calls

### Ethical Constraints
- ONLY passive reconnaissance
- NO active exploitation
- All data from public sources (DNS, SSL, CT logs)

---

## 🧪 Testing Approach

### Test Files
- `tests/` directory (pytest framework)
- Coverage target: Core modules > 80%

### Pre-commit Hooks
1. Trailing whitespace/EOF fixes
2. Black formatting (88 char line length)
3. isort import sorting
4. Ruff linting
5. Bandit security checks
6. mypy type checking

### Manual Testing
```bash
# Basic functionality
python main.py avanis.es

# Enhanced detection (v2.0)
python test_enhanced_detection.py avanis.es

# Dependencies verification
python verify_dependencies.py
```

---

**Note:** This map is optimized for token efficiency. For detailed implementation, refer to specific files.
