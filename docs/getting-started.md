# Getting Started with Rankle

This guide will help you install Rankle and run your first reconnaissance scan.

---

## Table of Contents

- [Requirements](#requirements)
- [Installation](#installation)
  - [Python Installation](#python-installation)
  - [From Source](#from-source)
- [Quick Start](#quick-start)
- [Usage](#usage)
  - [Command-Line Options](#command-line-options)
  - [Output Formats](#output-formats)
- [Next Steps](#next-steps)

---

## Requirements

**Minimum Requirements:**

- Python 3.13 or higher

**Supported Operating Systems:**

- Linux (Ubuntu, Debian, Fedora, etc.)
- macOS
- Windows (via WSL2 or native Python)

---

## Installation

### Python Installation

**Option 1: Install dependencies only**

```bash
# Required libraries
pip install requests dnspython beautifulsoup4

# Optional (enhanced features)
pip install python-whois

# Or install all at once
pip install -r requirements.txt
```

**Option 2: Modern editable installation** (recommended for development)

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install Rankle in editable mode
pip install -e ".[dev]"

# Install pre-commit hooks (for contributors)
pre-commit install
```

### From Source

```bash
# Clone repository
git clone https://github.com/javicosvml/rankle.git
cd rankle

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run your first scan
python main.py example.com
```

---

## Quick Start

### Run Your First Scan

```bash
# Basic scan (prints to terminal only)
python main.py example.com

# Expected output:
DOMAIN: example.com
SCAN_TIME: 2026-01-19 12:00:00
STATUS: 200

[INFRASTRUCTURE]
  IPv4:              93.184.216.34
  IPv6:              2606:2800:220:1:248:1893:25c8:1946
  Hosting Provider:  Edgecast (AS15133)

[TECHNOLOGY]
  CMS:               Not detected
  CDN:               Edgecast CDN
  WAF:               Not detected

[SECURITY]
  HTTPS:             ✓ Enabled
  TLS Version:       TLSv1.3
  Certificate:       Valid (expires: 2027-03-13)
```

### Save Results to File

```bash
# Save as JSON (machine-readable)
python main.py example.com -o json

# Save as text report (human-readable)
python main.py example.com -o text

# Save both formats
python main.py example.com -o both
```

### Verbose Output

```bash
# Enable verbose mode for debugging
python main.py example.com -v
```

---

## Usage

### Command-Line Options

```
python main.py <domain> [options]

Required:
  domain              Target domain to scan (e.g., example.com)

Options:
  -o, --output TYPE   Save output to file (json/text/both)
                      If not specified, only prints to terminal
  -v, --verbose       Enable verbose output with debug info
  --output-dir PATH   Output directory (default: ./output)
  --version           Show version number
  -h, --help          Show help message

Examples:
  python main.py example.com                    # Basic scan
  python main.py example.com -o json            # JSON output
  python main.py example.com -o both -v         # Both formats, verbose
  python main.py example.com --output-dir /tmp  # Custom output directory
```

### Output Formats

#### JSON Output

**Purpose:** Machine-readable structured data for automation and integration

**File Location:** `output/<domain>_rankle.json`

**Use Cases:**

- Automated processing with `jq`
- Integration with security tools (Nuclei, Nmap, Metasploit)
- Database storage (PostgreSQL JSONB, Elasticsearch)
- Comparison and monitoring (diff between scans)
- Pipeline integration (SIEM/SOAR)

**Example Usage:**

```bash
# Extract IPs
cat scan.json | jq -r '.dns.A[]'

# Count subdomains
cat scan.json | jq '.subdomains | length'

# Get detected CMS
cat scan.json | jq -r '.technologies_web.cms'

# Feed subdomains to other tools
cat scan.json | jq -r '.subdomains[]' | nuclei -l -
```

#### Text Output

**Purpose:** Human-readable technical report

**File Location:** `output/<domain>_report.txt`

**Characteristics:**

- Compact, technical format
- Section-based layout
- grep/awk friendly
- Quick manual review

**Structure:**

```text
DOMAIN: example.com
SCAN_TIME: 2026-01-19 12:00:00
STATUS: 200

[INFRASTRUCTURE]  - IPs, DNS, geolocation, ISP
[TECHNOLOGY]      - CMS, frameworks, server software
[SECURITY]        - TLS, certificates, headers, CDN/WAF
[SUBDOMAINS]      - Certificate transparency results
[WHOIS]           - Registration information
[DNS_RECORDS]     - TXT, SPF records
```

**Example Usage:**

```bash
# Extract security section
grep -A 10 "^\[SECURITY\]" report.txt

# Filter subdomains
awk '/^\[SUBDOMAINS\]/,/^\[/' report.txt | grep -v "^\["
```

---

## Next Steps

After installing and running your first scan:

1. **Explore Detection Capabilities**
   - Read [Detection Capabilities](detection-capabilities.md) to understand what Rankle can find
   - Learn about CMS, CDN, WAF, and cloud provider detection

2. **Integration with Other Tools**
   - See [Integration Examples](detection-capabilities.md#integration-examples) for Nuclei, Nmap, httpx
   - Use ready-to-run scripts in [docs/examples/](examples/README.md)
   - Build reconnaissance pipelines

3. **Development Setup**
   - Read [Development Guide](development.md) if you want to contribute
   - Learn about the modular architecture in [Architecture](architecture.md)

4. **Security Best Practices**
   - Always obtain proper authorization before scanning
   - Review [Security Policy](security.md) for responsible use guidelines

---

## Troubleshooting

### Python Import Errors

**Problem:** `ModuleNotFoundError: No module named 'requests'`

**Solution:**

```bash
pip install -r requirements.txt
```

### DNS Resolution Failures

**Problem:** "DNS query failed" or "No answer"

**Solution:**

- Check your internet connection
- Try with a different domain
- Configure custom DNS servers in `config/settings.py`:

  ```python
  DNS_NAMESERVERS = ["8.8.8.8", "1.1.1.1"]
  ```

### Timeout Errors

**Problem:** "Request timeout" or slow scans

**Solution:**

- Increase timeout in `config/settings.py`:

  ```python
  DEFAULT_TIMEOUT = 60  # Increase from 45
  ```

- Use verbose mode to see which operations are slow: `python main.py example.com -v`

---

## Support

- **Documentation:** [Full Documentation](index.md)
- **Issues:** [GitHub Issues](https://github.com/javicosvml/rankle/issues)
- **Security:** [Security Policy](security.md)

---

**Next:** [Architecture Documentation](architecture.md)
