![Rankle](img/rankle.png)

# 🃏 Rankle - Web Infrastructure Reconnaissance Tool

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/downloads/)
[![Docker](https://img.shields.io/badge/docker-ready-blue.svg)](https://www.docker.com/)
[![GitHub Actions](https://github.com/javicosvml/rankle/workflows/Docker%20Build%20Test/badge.svg)](https://github.com/javicosvml/rankle/actions)

Named after **Rankle, Master of Pranks** from Magic: The Gathering - a legendary faerie who excels at uncovering secrets.

A comprehensive web infrastructure analyzer using 100% Open Source Python libraries with **no API keys required**.

> **Features**: Modular architecture with **centralized configuration**, **retry logic**, and **concurrent scanning**!

---

## 🚀 Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run scan
python main.py example.com

# Save results
python main.py example.com -o json
```

**Docker:**

```bash
docker build -t rankle .
docker run --rm rankle example.com
```

---

## 📚 Documentation

**Complete documentation is now available in the [`docs/`](docs/) directory:**

### Getting Started

- **[Installation & Quick Start](docs/getting-started.md)** - Install Rankle and run your first scan
- **[Usage Guide](docs/getting-started.md#usage)** - Command-line options and output formats

### Technical Documentation

- **[Architecture](docs/architecture.md)** - Modular design, key classes, and patterns
- **[Detection Capabilities](docs/detection-capabilities.md)** - CMS, CDN, WAF, cloud providers
- **[API Reference](docs/architecture.md#api-reference)** - Core classes and modules

### Development

- **[Contributing Guide](docs/development.md)** - How to contribute to Rankle
- **[Development Setup](docs/development.md#development-setup)** - Environment configuration
- **[Testing](docs/development.md#testing)** - pytest, coverage, pre-commit hooks
- **[Utility Scripts](scripts/README.md)** - Demo and diagnostic scripts

### Claude Code Skills

- **[Skills Overview](docs/skills/index.md)** - Custom Claude Code skills for development
- **[Workflows](docs/skills/workflows.md)** - Common development patterns

### Additional Resources

- **[CHANGELOG.md](CHANGELOG.md)** - Version history and release notes
- **[SECURITY.md](SECURITY.md)** - Security policy and vulnerability reporting

---

## 🎯 Key Features

- **Enhanced Technology Detection** - Confidence scoring (0-100%), version detection, 30+ technologies
- **CMS Detection** - 16+ systems including enhanced Drupal detection (15+ patterns)
- **Cloud Provider Detection** - 14+ providers with ASN matching and confidence scoring
- **CDN Detection** - 20+ providers including TransparentEdge, Cloudflare, Akamai
- **WAF Detection** - 15+ solutions including Imperva, Sucuri, ModSecurity
- **Origin Discovery** - Find real infrastructure behind WAF/CDN (5 passive techniques)
- **Advanced Fingerprinting** - 8 techniques: HTTP methods, API discovery, exposed files
- **DNS Enumeration** - Complete analysis (A, AAAA, MX, NS, TXT, SOA, CNAME)
- **Subdomain Discovery** - Via Certificate Transparency logs (crt.sh)
- **JavaScript Libraries** - Detect 15+ libraries: jQuery, React, Vue, Angular

---

## 📦 Installation

### Requirements

- Python 3.11 or higher
- Docker (optional)

### Python Installation

```bash
# Required dependencies
pip install requests dnspython beautifulsoup4

# Or install all at once
pip install -r requirements.txt

# For development
pip install -e ".[dev]"
pre-commit install
```

### Docker Installation

```bash
git clone https://github.com/javicosvml/rankle.git
cd rankle
docker build -t rankle .
```

**See [Installation Guide](docs/getting-started.md) for detailed instructions.**

---

## 💻 Usage

```bash
# Basic scan (terminal output only)
python main.py example.com

# Save as JSON (for automation)
python main.py example.com -o json

# Save as text report (human-readable)
python main.py example.com -o text

# Save both formats
python main.py example.com -o both

# Verbose output
python main.py example.com -v
```

### Docker Usage

```bash
# Basic scan
docker run --rm rankle example.com

# Save output
docker run --rm -v $(pwd)/output:/output rankle example.com -o json
```

**See [Usage Guide](docs/getting-started.md#usage) for more examples.**

---

## 🔍 Detection Capabilities

Rankle can detect and analyze:

- **16+ CMS** - WordPress, Drupal, Joomla, Magento, Shopify, and more
- **20+ CDN Providers** - TransparentEdge, Cloudflare, Akamai, Fastly, AWS CloudFront
- **15+ WAF Solutions** - Imperva, Sucuri, ModSecurity, PerimeterX, DataDome
- **14+ Cloud Providers** - AWS, Azure, GCP, DigitalOcean, OVH, Hetzner
- **15+ JavaScript Libraries** - jQuery, Bootstrap, React, Vue, Angular
- **API Endpoints** - 15+ common paths including GraphQL, Swagger, health checks
- **Exposed Files** - Version control, backups, config files, development files
- **Security Headers** - X-Frame-Options, CSP, HSTS, and more

**See [Detection Capabilities](docs/detection-capabilities.md) for complete details.**

---

## 🔗 Integration Examples

### Nuclei

```bash
# Direct subdomain pipe
python main.py example.com -o json | jq -r '.subdomains[]' | nuclei -l -
```

### Nmap

```bash
# Scan discovered IPs
cat scan.json | jq -r '.dns.A[]' | nmap -iL - -sV
```

### httpx

```bash
# Verify live hosts
cat scan.json | jq -r '.subdomains[]' | httpx -silent | nuclei -l -
```

**See [Integration Examples](docs/detection-capabilities.md#integration-examples) for complete pipelines.**

---

## 🏗️ Architecture

Rankle follows **Python 3.11+ best practices** with modern packaging:

```text
rankle/
├── pyproject.toml          # Modern Python packaging (PEP 621)
├── main.py                 # Entry point
├── rankle/                 # Main package
│   ├── core/              # Scanner & session management
│   ├── modules/           # Reconnaissance modules (DNS, SSL, etc.)
│   ├── detectors/         # Technology detectors (CMS, CDN, WAF)
│   └── utils/             # Utilities and helpers
├── config/                 # Configuration & patterns
└── tests/                  # Unit tests (pytest)
```

**Key Features:**

- ✅ Modular architecture with lazy initialization
- ✅ Centralized configuration in `config/`
- ✅ Automatic retry logic with exponential backoff
- ✅ Concurrent scanning with ThreadPoolExecutor
- ✅ Connection pooling for HTTP sessions
- ✅ Full type hints (Python 3.11+)

**See [Architecture Documentation](docs/architecture.md) for details.**

---

## 🤝 Contributing

Contributions are welcome! Please see [Contributing Guide](docs/development.md) for detailed guidelines.

### Quick Contribution Guide

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes
4. Test: `python main.py example.com`
5. Commit: `git commit -m "Add: Amazing feature"`
6. Push: `git push origin feature/amazing-feature`
7. Open a Pull Request

### Areas for Contribution

**High Priority:**

- Additional CMS fingerprints (Django, Laravel, Rails)
- More CDN providers (regional CDNs)
- Enhanced WAF detection patterns
- Version detection improvements

**See [Development Guide](docs/development.md) for complete details.**

---

## 🛡️ Security & Best Practices

**Authorized Use Only:**

- ✅ Authorized penetration testing
- ✅ Bug bounty programs (with permission)
- ✅ Security research (on your own systems)
- ✅ Educational purposes

**Prohibited Use:**

- ❌ Unauthorized access attempts
- ❌ Malicious reconnaissance
- ❌ Illegal activities

**Security Features:**

- No shell injection (never uses `shell=True`)
- Input validation with regex
- Timeout controls
- Graceful error handling
- Realistic User-Agent headers

**See [SECURITY.md](SECURITY.md) for responsible use guidelines.**

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

### Disclaimer

This tool is provided for **educational and authorized security testing purposes only**.

Users must:

- Obtain proper authorization before scanning any target
- Comply with all applicable laws and regulations
- Use the tool responsibly and ethically

The authors and contributors are not responsible for any misuse or damage caused by this software.

---

## 🙏 Acknowledgments

- Named after **Rankle, Master of Pranks** from Magic: The Gathering
- Built with 100% Open Source libraries
- No API keys required
- Community-driven development

---

## 📞 Support & Contact

- **Documentation:** [docs/](docs/)
- **Issues:** [GitHub Issues](https://github.com/javicosvml/rankle/issues)
- **Discussions:** [GitHub Discussions](https://github.com/javicosvml/rankle/discussions)
- **Security:** [SECURITY.md](SECURITY.md)

---

## 🔗 Links

- **Repository:** <https://github.com/javicosvml/rankle>
- **Documentation:** [docs/](docs/)
- **Changelog:** [CHANGELOG.md](CHANGELOG.md)

---

<div align="center">

**🃏 Rankle: Master of Pranks knows all your secrets**

Made with ❤️ by the security community

[![GitHub stars](https://img.shields.io/github/stars/javicosvml/rankle?style=social)](https://github.com/javicosvml/rankle/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/javicosvml/rankle?style=social)](https://github.com/javicosvml/rankle/network/members)

</div>
