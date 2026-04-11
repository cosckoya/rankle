# Rankle - Web Infrastructure Reconnaissance Tool

![Rankle](rankle.png)

**Passive reconnaissance. Zero API keys. 100% open source.**

Rankle is a comprehensive web infrastructure analyzer that performs **passive reconnaissance** on target domains, collecting DNS records, SSL certificates, technology stack, CDN/WAF detection, and more.

Named after *Rankle, Master of Pranks* from Magic: The Gathering.

## Quick Start

**Requirements:** Python 3.13+, uv

```bash
# Clone and setup
git clone https://github.com/javicosvml/rankle.git && cd rankle
uv sync

# Basic scan (console output)
uv run python main.py example.com

# Save to SQLite database
uv run python main.py example.com --backend sqlite

# Export to JSON
uv run python main.py example.com --backend json
```

## Features

- **DNS Analysis** — A, AAAA, MX, NS, TXT, CNAME, SOA, CAA, SRV records
- **SSL/TLS Inspection** — certificate chain, SANs, cipher suites, protocols
- **Technology Detection** — 3000+ signatures (CMS, frameworks, libraries)
- **CDN/WAF Detection** — 20+ CDN + 15+ WAF providers
- **Security Headers Audit** — comprehensive header analysis with severity scoring
- **Subdomain Discovery** — Certificate Transparency + DNS enumeration
- **HTTP Fingerprinting** — server detection, allowed methods, exposed paths
- **Geolocation & Hosting** — IP geolocation and cloud provider detection
- **WHOIS Lookup** — registration data and domain information
- **Scan History** — track changes across multiple scans
- **REST API** — FastAPI with real-time WebSocket progress
- **Multiple Outputs** — console, JSON files, SQLite database

## Commands

```bash
# Core scanning
uv run python main.py DOMAIN                 # Scan to console
uv run python main.py DOMAIN --backend json  # Export JSON
uv run python main.py DOMAIN --backend sqlite  # Save to DB

# Database queries
uv run python main.py history DOMAIN         # Scan history
uv run python main.py diff DOMAIN            # Compare last 2 scans
uv run python main.py list                   # All scans

# Web API
uv run python api.py                         # Start API server (port 8000)
```

## Tech Stack

| Component | Technology | Version |
|-----------|-----------|---------|
| Language | Python | 3.13+ |
| Database | SQLAlchemy 2.x + SQLite | 2.0+ |
| Web Framework | FastAPI | 0.104+ |
| Package Manager | uv | Latest |
| Linting | ruff | 0.15+ |
| Type Checking | pyright | strict |
| Testing | pytest | 8.4+ |

## Project Structure

```
rankle/
├── main.py                 # CLI entry point (scan, history, diff, list)
├── api.py                  # FastAPI entry point (http://localhost:8000)
├── src/
│   ├── rankle/            # Core package
│   │   ├── core/          # Scanner orchestration
│   │   ├── modules/       # Reconnaissance modules (DNS, SSL, etc)
│   │   ├── detectors/     # Detection modules (CDN, WAF, etc)
│   │   ├── db/            # Database (ORM, engine, repository)
│   │   ├── output/        # Output backends (console, JSON, SQLite)
│   │   ├── api/           # FastAPI application
│   │   └── utils/         # Utilities (validators, helpers, etc)
│   └── config/            # Configuration and settings
├── tests/                 # Test suite
├── docs/                  # Documentation
└── rankle.db             # SQLite database (created at runtime)
```

## Documentation

| Guide | Purpose |
|-------|---------|
| [Getting Started](docs/getting-started.md) | Installation and first scan |
| [Architecture](docs/architecture.md) | Design and module structure |
| [Detection Capabilities](docs/detection-capabilities.md) | What each module finds |
| [API Reference](docs/api-usage-examples.md) | API endpoints and WebSocket |
| [Development](docs/development.md) | Contributing and testing |
| [Troubleshooting](docs/troubleshooting.md) | Common issues and fixes |

## Configuration

Create a `.env` file to customize behavior:

```bash
# Database
DATABASE_URL=sqlite:///rankle.db      # SQLite (default) or PostgreSQL
OUTPUT_BACKEND=console                # console | json | sqlite
LOG_LEVEL=INFO                        # DEBUG | INFO | WARNING | ERROR
```

See `.env.example` for all options.

## API Usage

### Start Server
```bash
uv run python api.py
# API at http://localhost:8000
# Docs at http://localhost:8000/docs (Swagger UI)
```

### Create Scan
```bash
curl -X POST http://localhost:8000/api/v1/scans \
  -H "Content-Type: application/json" \
  -d '{"domain": "example.com", "scan_type": "full"}'
```

### Real-Time Progress
```bash
# WebSocket: ws://localhost:8000/ws/progress/{scan_id}
wscat -c "ws://localhost:8000/ws/progress/1"
```

See [API Examples](docs/api-usage-examples.md) for full reference.

## Testing

```bash
# All tests with coverage
uv run pytest --cov=src/rankle -v

# Run specific test file
uv run pytest tests/test_modules/test_dns.py -v

# Skip slow tests
uv run pytest -m "not slow" -v
```

**Coverage Target:** 85% minimum (enforced)

## Code Quality

```bash
# Linting + formatting
ruff check src/ --fix && ruff format src/

# Type checking (strict mode)
pyright src/rankle/

# Pre-commit hooks
pre-commit run --all-files
```

## Security & Ethics

Rankle performs **passive reconnaissance only** — no active attacks, brute force, or exploitation.

- ✅ DNS queries (public nameservers)
- ✅ SSL certificate inspection
- ✅ HTTP GET/HEAD/OPTIONS requests
- ✅ Public Certificate Transparency logs
- ❌ NO credential brute-force
- ❌ NO SQL injection, XSS, or exploitation
- ❌ NO active WAF/WAF bypassing
- ❌ NO intrusion detection triggers

**Always obtain authorization before scanning any domain.**

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/my-feature`)
3. Make changes and run tests (`uv run pytest`)
4. Ensure linting passes (`ruff check . --fix`)
5. Type check passes (`pyright src/rankle/`)
6. Commit with conventional format (`feat:`, `fix:`, `docs:`, etc)
7. Push and open a pull request

See [CONTRIBUTING.md](docs/development.md) for full guidelines.

## License

MIT License — see [LICENSE](LICENSE) for details.

## Roadmap

- [ ] Redis caching for scan results
- [ ] GraphQL API
- [ ] React web dashboard
- [ ] PostgreSQL production support
- [ ] Docker Compose deployment
- [ ] CI/CD integration
- [ ] Webhook notifications
- [ ] User authentication

## Support

- 📖 [Documentation](docs/)
- 🐛 [Issue Tracker](https://github.com/javicosvml/rankle/issues)
- 💬 [Discussions](https://github.com/javicosvml/rankle/discussions)

---

**Rankle v0.1-alpha** | Built with ❤️ by the security community | Passive reconnaissance, zero limitations
