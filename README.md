# Rankle

Passive web infrastructure reconnaissance tool — DNS analysis, technology detection, and CDN/WAF fingerprinting with 100% open-source Python libraries.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)
[![Python 3.13+](https://img.shields.io/badge/python-3.13%2B-blue.svg)](https://www.python.org/downloads/)

![Rankle](img/rankle.png)

---

## Quick Start

```bash
# Install dependencies
uv sync

# Run a scan
uv run python main.py example.com

# Save results as JSON
uv run python main.py example.com -o
```

---

## Key Features

- **Technology detection** — CMS, frameworks, libraries with confidence scores (3000+ signatures via Wappalyzer + favicon hashing)
- **Infrastructure mapping** — CDN (20+ providers), WAF (15+ solutions), and cloud provider detection
- **Origin discovery** — 5 passive techniques to uncover real IPs behind CDN/WAF proxies
- **DNS enumeration** — A, AAAA, MX, NS, TXT, SOA, CNAME records plus Certificate Transparency subdomain discovery
- **HTTP fingerprinting** — Security header audit, exposed file discovery, HTTP method detection

---

## Tech Stack

| Component | Technology | Version |
|-----------|-----------|---------|
| Language | Python | 3.13+ |
| Package manager | uv | latest |
| HTTP | requests | 2.31+ |
| DNS | dnspython | 2.4+ |
| HTML parsing | BeautifulSoup4 | 4.12+ |
| Tech detection | python-wappalyzer | 0.3.1+ |
| Favicon hashing | mmh3 | 5.0+ |
| Linting | ruff | latest |
| Type checking | pyright | strict |
| Testing | pytest | 8.x |

---

## Project Structure

```
rankle/
├── main.py                    # CLI entry point
├── src/
│   ├── rankle/
│   │   ├── core/
│   │   │   ├── scanner.py     # RankleScanner orchestrator (lazy-init pattern)
│   │   │   └── session.py     # HTTP session with retry + connection pooling
│   │   ├── modules/           # dns, ssl, whois, subdomains, http_fingerprint
│   │   ├── detectors/         # technology, cdn, waf, origin
│   │   ├── utils/             # validators, confidence, rate_limiter, cve_mapper
│   │   └── types.py           # TypeAlias definitions
│   └── config/
│       ├── settings.py        # Timeouts, DNS servers, rate limits, REPORTS_DIR
│       └── patterns.py        # CDN/WAF/cloud ASN patterns
├── tests/                     # pytest test suite (85%+ coverage target)
├── reports/                   # JSON scan output (gitignored)
└── docs/                      # Full documentation
```

---

## Usage

```bash
# Scan and print to terminal
uv run python main.py example.com

# Save JSON report to reports/
uv run python main.py example.com -o

# Verbose output (debug information)
uv run python main.py example.com -v

# Show all options
uv run python main.py --help
```

Output files are saved to `reports/rankle_<domain>_<timestamp>.json`.

---

## Development

```bash
# Install with dev dependencies
uv sync

# Code quality
ruff check . --fix && ruff format .
pyright src/
pytest --cov=src/rankle

# Pre-commit hooks
pre-commit install
pre-commit run --all-files
```

---

## Documentation

| Document | Description |
|----------|-------------|
| [Getting Started](docs/getting-started.md) | Installation, requirements, first scan |
| [Architecture](docs/architecture.md) | Module design, lazy-init pattern, request flow |
| [Detection Capabilities](docs/detection-capabilities.md) | Full list of detected technologies, CDNs, WAFs |
| [API Usage Examples](docs/api-usage-examples.md) | Programmatic usage with type hints |
| [Development Guide](docs/development.md) | Contributing, testing, pre-commit hooks |
| [Performance Tuning](docs/performance-tuning.md) | Optimization, timeouts, rate limiting |
| [Troubleshooting](docs/troubleshooting.md) | Common issues and solutions |

---

## Contributing and License

See [docs/development.md](docs/development.md) for contribution guidelines and code standards.

Licensed under the [MIT License](LICENSE).
