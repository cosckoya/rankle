# Rankle Integration Examples

This directory contains ready-to-use integration scripts that demonstrate how to chain Rankle with other reconnaissance and security tools.

---

## 📋 Available Scripts

### 1. **full_recon_chain.sh** - Complete Reconnaissance Pipeline

**Purpose:** Automated end-to-end reconnaissance workflow combining Rankle, httpx, Nuclei, and Nmap.

**Tools Required:**
- Docker (for Rankle)
- httpx - Fast HTTP toolkit
- Nuclei - Template-based vulnerability scanner
- Nmap - Network port scanner
- jq - JSON processor

**Usage:**
```bash
./docs/examples/full_recon_chain.sh example.com
```

**Output:**
- Rankle JSON and text reports
- Subdomain list (deduplicated)
- Live host detection results
- Nuclei vulnerability findings
- Nmap port scan results
- Summary report (REPORT.txt)

**Workflow:**
```
Rankle (DNS + Subdomains + Tech Detection)
    ↓
Extract & Deduplicate Subdomains
    ↓
httpx (Live Host Detection)
    ↓
Nuclei (Vulnerability Scanning - Medium/High/Critical)
    ↓
Nmap (Port Scanning on Discovered IPs)
    ↓
Generate Summary Report
```

---

### 2. **nuclei_pipeline.sh** - Rankle to Nuclei Integration

**Purpose:** Discover subdomains with Rankle and scan them for vulnerabilities using Nuclei.

**Tools Required:**
- Docker (for Rankle)
- httpx
- Nuclei
- jq

**Usage:**
```bash
./docs/examples/nuclei_pipeline.sh example.com
```

**Output:**
- Rankle scan results (JSON)
- Subdomain list
- Live hosts (httpx results)
- Nuclei vulnerability findings

**Focus:**
- High and critical severity CVEs
- Vulnerability templates
- Live host validation before scanning

---

### 3. **nmap_pipeline.sh** - Rankle to Nmap Integration

**Purpose:** Extract IPs from Rankle DNS results and perform detailed port scanning.

**Tools Required:**
- Docker (for Rankle)
- Nmap
- jq

**Usage:**
```bash
./docs/examples/nmap_pipeline.sh example.com
```

**Output:**
- Rankle scan results (JSON)
- IP address list
- Service detection on common ports (80, 443, 8080, 8443, 22, 21, 3306, 5432)
- Full port scan on first discovered IP

**Nmap Scripts Used:**
- `banner` - Service banner grabbing
- `http-title` - HTTP page titles
- `ssl-cert` - SSL certificate information

---

## 🔧 Installation Requirements

### Install Required Tools

**Debian/Ubuntu:**
```bash
# Docker (for Rankle)
sudo apt install docker.io

# httpx
go install -v github.com/projectdiscovery/httpx/cmd/httpx@latest

# Nuclei
go install -v github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest

# Nmap
sudo apt install nmap

# jq
sudo apt install jq
```

**macOS:**
```bash
# Homebrew
brew install docker httpx nuclei nmap jq
```

**Arch Linux:**
```bash
sudo pacman -S docker nmap jq
go install -v github.com/projectdiscovery/httpx/cmd/httpx@latest
go install -v github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest
```

---

## 🚀 Quick Start

**1. Make scripts executable:**
```bash
chmod +x docs/examples/*.sh
```

**2. Build Rankle Docker image:**
```bash
docker build -t rankle .
```

**3. Run a complete reconnaissance:**
```bash
./docs/examples/full_recon_chain.sh target.com
```

**4. Check results:**
```bash
ls -lh recon_*_target.com/
cat recon_*_target.com/REPORT.txt
```

---

## 📊 Expected Output Structure

**full_recon_chain.sh output:**
```
recon_20260120_013000_example.com/
├── example_com_rankle.json           # Full Rankle results
├── example_com_rankle_report.txt     # Human-readable report
├── subdomains.txt                    # Discovered subdomains
├── live_hosts.txt                    # Verified live hosts
├── nuclei_vulns.txt                  # Vulnerability findings
├── nmap_scan.xml                     # Nmap results (XML)
├── nmap_scan.nmap                    # Nmap results (text)
├── nmap_scan.gnmap                   # Nmap results (greppable)
└── REPORT.txt                        # Summary report
```

---

## 🔐 Security & Ethics

**IMPORTANT:** These scripts are for **authorized security testing only**.

**Authorized Use Cases:**
- Penetration testing engagements (with written permission)
- Bug bounty programs (within scope)
- Your own infrastructure
- Security research (authorized targets)

**Unauthorized Use:**
- Scanning targets without permission is **illegal**
- Rate limiting and aggressive scanning may violate terms of service
- Always obtain explicit authorization before scanning

**Rate Limiting:**
The scripts include reasonable delays, but you should:
- Adjust scanning speed based on target infrastructure
- Respect robots.txt and security.txt
- Monitor your network traffic
- Use VPN/authorized networks only

---

## 🛠️ Customization

### Adjust Nuclei Severity

**Scan all severities:**
```bash
# In nuclei_pipeline.sh or full_recon_chain.sh, change:
-severity high,critical
# To:
-severity info,low,medium,high,critical
```

### Modify Nmap Port Range

**Scan more ports:**
```bash
# In nmap_pipeline.sh, change:
-p 80,443,8080,8443,22,21,3306,5432
# To:
-p- # (all ports, slower)
# Or:
-p 1-1000 # (first 1000 ports)
```

### Add Timeout Controls

**For slow targets:**
```bash
# Add to httpx commands:
cat subdomains.txt | httpx -timeout 30 -retries 3
```

---

## 🐛 Troubleshooting

**Issue: "Docker: command not found"**
- Install Docker and ensure it's in PATH
- Run: `docker --version` to verify

**Issue: "httpx/nuclei: command not found"**
- Install Go: `sudo apt install golang-go`
- Add `~/go/bin` to PATH: `export PATH=$PATH:~/go/bin`
- Reinstall tools with go install

**Issue: "Permission denied"**
- Make scripts executable: `chmod +x docs/examples/*.sh`
- Run Docker commands with sudo or add user to docker group

**Issue: "jq: command not found"**
- Install: `sudo apt install jq` (Debian/Ubuntu)
- Or: `brew install jq` (macOS)

**Issue: "Nuclei templates not found"**
- Update templates: `nuclei -update-templates`
- Verify location: `nuclei -templates-version`

---

## 📚 Additional Resources

**Rankle Documentation:**
- [Getting Started](../getting-started.md)
- [Detection Capabilities](../detection-capabilities.md)
- [Architecture](../architecture.md)

**Tool Documentation:**
- [httpx](https://github.com/projectdiscovery/httpx)
- [Nuclei](https://github.com/projectdiscovery/nuclei)
- [Nmap](https://nmap.org/book/man.html)

**Security Testing:**
- [OWASP Testing Guide](https://owasp.org/www-project-web-security-testing-guide/)
- [Bug Bounty Platforms](https://www.bugcrowd.com/resources/guides/bug-bounty-platforms/)

---

## 🤝 Contributing

Found a bug or have an improvement?

1. Test your changes with multiple targets
2. Update this README if adding new scripts
3. Ensure scripts follow bash best practices
4. Submit a PR with clear description

**Script Guidelines:**
- Use `set -e` for error handling
- Validate input parameters
- Provide clear progress messages
- Create timestamped output directories
- Include usage instructions in script comments

---

**Last Updated:** January 20, 2026
**Maintained By:** Rankle Project Contributors
