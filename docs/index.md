# Rankle Documentation

![Rankle](../img/rankle.png)

**Version:** 2.0.0 Enhanced
**Last Updated:** 2026-01-20

---

## Overview

**Rankle** is a comprehensive web infrastructure reconnaissance tool for authorized security testing. Named after "Rankle, Master of Pranks" from Magic: The Gathering, it analyzes DNS, detects technologies (CMS, CDN, WAF), inspects TLS certificates, and discovers subdomains via Certificate Transparency.

**Key Features:**
- **Enhanced Technology Detection (v2.0)** - 3000+ signatures via Wappalyzer, favicon hashing, error page fingerprinting
- **Advanced Fingerprinting** - JavaScript endpoint extraction, WordPress plugin detection, CVE mapping
- 100% Open Source Python libraries with **no API keys required**
- Modular architecture with centralized configuration
- Automatic retry logic with exponential backoff
- Concurrent scanning for optimal performance
- Docker support with security best practices

---

## Documentation Navigation

### Getting Started
- [Installation & Quick Start](getting-started.md) - Install Rankle and run your first scan
- [Usage Guide](getting-started.md#usage) - Command-line options and output formats
- [Docker Usage](getting-started.md#docker-usage) - Container deployment

### Technical Documentation
- [Architecture](architecture.md) - Modular design, key classes, and patterns
- [Detection Capabilities](detection-capabilities.md) - CMS, CDN, WAF, cloud providers, and more
- [Enhanced Detection (v2.0)](TECHNOLOGY_DETECTION_ENHANCEMENT.md) - Wappalyzer, favicon hashing, CVE mapping
- [Type Checking Guide](MYPY_GUIDE.md) - mypy configuration and best practices
- [API Usage Examples](api-usage-examples.md) - Using Rankle as a Python library
- [Troubleshooting](troubleshooting.md) - Common issues and solutions
- [Performance Tuning](performance-tuning.md) - Optimization strategies
- [API Reference](architecture.md#api-reference) - Core classes and modules
- [Configuration](architecture.md#configuration) - Settings and pattern management

### Development
- [Contributing Guide](development.md) - How to contribute to Rankle
- [Development Setup](development.md#development-setup) - Environment configuration
- [Testing](development.md#testing) - pytest, coverage, pre-commit hooks
- [Coding Standards](development.md#coding-standards) - Python best practices
- [Utility Scripts](../scripts/README.md) - Demo and diagnostic tools

### Additional Resources
- [CHANGELOG.md](../CHANGELOG.md) - Version history and release notes
- [SECURITY.md](../SECURITY.md) - Security policy and vulnerability reporting
- [LICENSE](../LICENSE) - MIT License

### Claude Code Configuration
- [CLAUDE.md](../CLAUDE.md) - Claude Code quick reference
- [Complete Claude Documentation](../.claude/README.claude.md) - Consolidated Claude Code documentation (architecture, skills, configuration)

---

## Quick Links

### Common Tasks
- **Run a scan:** `python main.py example.com`
- **Save JSON output:** `python main.py example.com -o json`
- **Docker scan:** `docker run --rm rankle example.com`
- **Run tests:** `pytest`
- **Lint code:** `ruff check . && ruff format .`

### Integration Examples
- [Nuclei Integration](detection-capabilities.md#integration-with-nuclei) - Subdomain scanning
- [Nmap Integration](detection-capabilities.md#integration-with-nmap) - Port scanning
- [Full Reconnaissance Pipeline](detection-capabilities.md#full-reconnaissance-pipeline) - Complete workflow

### Development Tools
- [Pre-commit Setup](development.md#pre-commit-hooks) - Automated code quality
- [Adding New Modules](architecture.md#adding-new-modules) - Extension guide
- [Testing Guide](development.md#testing) - Unit tests and coverage

---

## Project Information

**Repository:** https://github.com/javicosvml/rankle
**License:** MIT
**Python Version:** 3.11+
**Standards:** PEP 621 (pyproject.toml), PEP 517/518, Ruff formatting

**Compliance:**
- ✅ Python 3.11-3.14 compatible
- ✅ Full type hints support
- ✅ Modern packaging with pyproject.toml
- ✅ Pre-commit hooks for code quality
- ✅ Docker support with security hardening

---

## Support

- **Issues:** [GitHub Issues](https://github.com/javicosvml/rankle/issues)
- **Discussions:** [GitHub Discussions](https://github.com/javicosvml/rankle/discussions)
- **Security:** See [SECURITY.md](../SECURITY.md)

---

## Ethical Use

**Authorized Use Only:**
- ✅ Authorized penetration testing
- ✅ Bug bounty programs (with permission)
- ✅ Security research (on your own systems)
- ✅ Auditing purposes

**Prohibited Use:**
- ❌ Unauthorized access attempts
- ❌ Malicious reconnaissance
- ❌ Illegal activities
- ❌ Violating terms of service

Always obtain proper authorization before scanning any target.

---

**Made with ❤️ by the security community**
