# Rankle

Passive web infrastructure reconnaissance tool — DNS analysis, technology detection, and CDN/WAF fingerprinting with 100% open-source Python libraries.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/downloads/)
[![Docker](https://img.shields.io/badge/docker-ready-blue.svg)](https://www.docker.com/)

---

## Quick Start

```bash
# Install dependencies with uv
uv sync

# Run a basic scan
python main.py example.com

# Save output as JSON for automation
python main.py example.com -o json
```

See [docs/getting-started.md](docs/getting-started.md) for full installation and usage options.

---

## Key Features

- **Technology detection** — CMS, frameworks, libraries with confidence scores and version extraction (3000+ signatures via Wappalyzer + favicon hashing)
- **Infrastructure mapping** — Identify CDN (20+ providers), WAF (15+ solutions), and cloud providers (14+ vendors) behind target domains
- **Origin discovery** — 5 passive techniques to uncover real infrastructure IP behind CDN/WAF proxies
- **DNS enumeration** — Complete A, AAAA, MX, NS, TXT, SOA, CNAME record analysis plus Certificate Transparency subdomain discovery
- **HTTP fingerprinting** — API endpoint extraction, exposed file discovery, security header audit, HTTP method detection

---

## Tech Stack

| Component | Technology | Version |
|-----------|-----------|---------|
| Language | Python | 3.11+ |
| HTTP | requests + urllib3 | 2.x |
| DNS | dnspython | 2.x |
| HTML parsing | BeautifulSoup4 | 4.x |
| Favicon hashing | mmh3 | 4.x |
| Linting | ruff | 0.x |
| Type checking | mypy | 1.x |
| Testing | pytest + pytest-cov | 8.x |
| Package manager | uv | 0.x |

---

## Project Structure

```
rankle/
├── main.py                     # CLI entry point
├── config/
│   ├── settings.py             # Timeouts, DNS servers, rate limits
│   ├── patterns.py             # CDN/WAF/cloud ASN patterns
│   └── tech_signatures.json    # 3000+ detection signatures
├── rankle/
│   ├── core/
│   │   ├── scanner.py          # RankleScanner orchestrator (lazy-init pattern)
│   │   └── session.py          # HTTP session with retry + connection pooling
│   ├── modules/                # dns, ssl, whois, subdomains, http_fingerprint
│   ├── detectors/              # technology, cdn, waf, origin
│   ├── utils/                  # validators, confidence, rate_limiter, cve_mapper
│   └── reports/                # JSON and text report generators
├── tests/                      # pytest test suite (70%+ coverage target)
└── docs/                       # Full documentation (MkDocs format)
```

---

## Usage Examples

```bash
# Scan all modules, print to terminal
python main.py example.com

# Save JSON output (machine-readable for automation)
python main.py example.com -o json

# Save text report (human-readable)
python main.py example.com -o text

# Save both JSON and text simultaneously
python main.py example.com -o both

# Verbose output with debug information
python main.py example.com -v

# Docker: basic scan
docker build -t rankle .
docker run --rm rankle example.com

# Docker: save output with persistent volume
docker run --rm -v $(pwd)/output:/output rankle example.com -o json
```

Output files are saved to `output/` with timestamp: `output/example.com_20260410_143022.json`

Full documentation: [docs/getting-started.md](docs/getting-started.md)

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
| [Changelog](docs/changelog.md) | Version history and release notes |
| [Security Policy](docs/security.md) | Vulnerability reporting, responsible disclosure |
| [Integration Examples](docs/examples/README.md) | Ready-to-use examples for tool integration |

---

## Contributing & License

See [docs/development.md](docs/development.md) for contribution guidelines and code standards.

```bash
# Setup development environment
pre-commit install
uv sync

# Code quality checks
ruff check . --fix && ruff format .
mypy rankle/
pytest --cov=rankle
```

Licensed under the [MIT License](LICENSE).
