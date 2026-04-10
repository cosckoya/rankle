# Rankle

Passive web infrastructure reconnaissance tool — no API keys required.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/downloads/)
[![Docker](https://img.shields.io/badge/docker-ready-blue.svg)](https://www.docker.com/)

---

## Quick Start

```bash
# Install with uv (recommended)
uv sync

# Run a scan
python main.py example.com

# Save as JSON
python main.py example.com -o json
```

**Docker:**

```bash
docker build -t rankle .
docker run --rm rankle example.com
```

---

## Key Features

- **Technology detection** — CMS, frameworks, libraries with confidence scores (0-100%) and version extraction
- **Infrastructure mapping** — CDN (20+ providers), WAF (15+ solutions), cloud provider (14+ vendors) fingerprinting
- **Origin discovery** — 5 passive techniques to find real infrastructure behind CDN/WAF layers
- **DNS enumeration** — A, AAAA, MX, NS, TXT, SOA, CNAME records with subdomain discovery via Certificate Transparency
- **HTTP fingerprinting** — API endpoint discovery, exposed files, security header audit, allowed method detection

---

## Tech Stack

| Component | Technology | Version |
|-----------|-----------|---------|
| Language | Python | 3.11+ |
| HTTP client | requests + urllib3 | 2.x |
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
├── main.py                   # Entry point
├── config/
│   ├── settings.py           # Timeouts, DNS servers, rate limits
│   ├── patterns.py           # CDN/WAF/cloud ASN patterns
│   └── tech_signatures.json  # 3000+ detection signatures
├── rankle/
│   ├── core/
│   │   ├── scanner.py        # RankleScanner orchestrator (lazy-init)
│   │   └── session.py        # HTTP session with retry + pooling
│   ├── modules/              # dns, ssl, whois, subdomains, http_fingerprint
│   ├── detectors/            # technology, cdn, waf, origin
│   ├── utils/                # validators, confidence, rate_limiter, cve_mapper
│   └── reports/              # JSON and text report generators
├── tests/                    # pytest test suite
└── docs/                     # Full documentation
```

---

## Usage

```bash
# Scan with all modules
python main.py example.com

# Save JSON (machine-readable, suitable for automation)
python main.py example.com -o json

# Save text report (human-readable)
python main.py example.com -o text

# Save both formats simultaneously
python main.py example.com -o both

# Verbose output with debug information
python main.py example.com -v

# Docker with persistent output volume
docker run --rm -v $(pwd)/output:/output rankle example.com -o json
```

**Output files** are saved to `output/` with timestamp: `output/example.com_20260410_143022.json`

---

## Documentation

| Document | Description |
|----------|-------------|
| [Getting Started](docs/getting-started.md) | Installation, requirements, first scan |
| [Architecture](docs/architecture.md) | Module design, lazy-init pattern, request flow |
| [Detection Capabilities](docs/detection-capabilities.md) | Full list of detected technologies, CDNs, WAFs |
| [API Usage Examples](docs/api-usage-examples.md) | Programmatic usage, type hints |
| [Development Guide](docs/development.md) | Contributing, testing, pre-commit hooks |
| [Performance Tuning](docs/performance-tuning.md) | Timeouts, rate limiting, concurrency |
| [Troubleshooting](docs/troubleshooting.md) | Common issues and solutions |
| [Changelog](docs/changelog.md) | Version history and release notes |
| [Security Policy](docs/security.md) | Vulnerability reporting, responsible disclosure |

---

## Contributing & License

See [docs/development.md](docs/development.md) for contribution guidelines, code style, and testing requirements.

```bash
pre-commit install          # Install git hooks
ruff check . --fix          # Lint and auto-fix
pytest --cov=rankle         # Run tests with coverage
```

Licensed under the [MIT License](LICENSE).
