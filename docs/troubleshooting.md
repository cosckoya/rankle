# Rankle Troubleshooting Guide

**Purpose:** Solutions to common issues, error messages, and debugging strategies
**Last Updated:** 2026-01-20

---

## Table of Contents

1. [Installation Issues](#installation-issues)
2. [Dependency Problems](#dependency-problems)
3. [Network & Connection Errors](#network--connection-errors)
4. [DNS Resolution Failures](#dns-resolution-failures)
5. [SSL/TLS Certificate Errors](#ssltls-certificate-errors)
6. [Rate Limiting & Blocking](#rate-limiting--blocking)
7. [Timeout Errors](#timeout-errors)
8. [Detection Issues](#detection-issues)
9. [Output & Formatting Problems](#output--formatting-problems)
10. [Performance Issues](#performance-issues)
11. [Type Checking Errors](#type-checking-errors)
12. [Getting Help](#getting-help)

---

## Installation Issues

### Problem: `uv pip install` fails with "externally-managed-environment"

**Error Message:**

```
error: externally-managed-environment
× This environment is externally managed
```

**Cause:** Python 3.13+ on Debian/Ubuntu uses externally managed environments

**Solution 1 (Recommended):** Use uv sync

```bash
uv sync
```

**Solution 2:** Use a virtual environment explicitly

```bash
# Create venv and install
uv venv
source .venv/bin/activate
uv sync
```

---

### Problem: `ModuleNotFoundError: No module named 'Wappalyzer'`

**Error Message:**

```
ModuleNotFoundError: No module named 'Wappalyzer'
```

**Cause:** python-Wappalyzer package not installed or missing dependency

**Solution:**

```bash
# Install Wappalyzer and its dependencies
uv pip install python-Wappalyzer setuptools

# Verify installation
python -c "import Wappalyzer; print('OK')"
```

**Note:** Wappalyzer requires `setuptools` for `pkg_resources` (will be deprecated but currently needed)

---

### Problem: `ModuleNotFoundError: No module named 'pkg_resources'`

**Error Message:**

```
File ".../Wappalyzer.py", line 5, in <module>
    import pkg_resources
ModuleNotFoundError: No module named 'pkg_resources'
```

**Cause:** Missing setuptools package (required by python-Wappalyzer)

**Solution:**

```bash
uv pip install setuptools
```

**Workaround for Deprecation Warning:**
The warning about `pkg_resources` being deprecated is expected and can be ignored. It comes from the Wappalyzer library itself.

---

---

## Dependency Problems

### Problem: "Some core dependencies are missing"

**Error Message:**

```
❌ Some core dependencies are missing!
   Missing packages: python-Wappalyzer, mmh3
```

**Diagnosis:** Check if dependencies are installed

```bash
uv pip list | grep -i wappalyzer
uv pip list | grep -i mmh3
```

**Solution:** Install missing packages

```bash
uv pip install python-Wappalyzer mmh3 setuptools
```

---

### Problem: ImportError for rankle modules

**Error Message:**

```
ImportError: cannot import name 'RankleScanner' from 'rankle'
```

**Cause:** Rankle not installed in development mode

**Solution:**

```bash
# Install in development mode
uv pip install -e .

# Or install in editable mode with dev dependencies
uv pip install -e ".[dev]"
```

---

### Problem: Version conflicts between dependencies

**Error Message:**

```
ERROR: pip's dependency resolver does not currently take into account all the packages that are installed.
```

**Solution:** Clean install

```bash
# Remove old venv
rm -rf .venv

# Create fresh environment and install
uv sync
```

---

## Network & Connection Errors

### Problem: Connection refused or connection timeout

**Error Message:**

```
requests.exceptions.ConnectionError: ('Connection aborted.', ConnectionRefusedError(111, 'Connection refused'))
```

**Possible Causes:**

1. Target domain is down
2. Firewall blocking outbound connections
3. Network connectivity issues
4. Target blocking your IP

**Diagnosis:**

```bash
# Test basic connectivity
ping example.com

# Test HTTP connectivity
curl -I https://example.com

# Check DNS resolution
nslookup example.com

# Test from different network
# (mobile hotspot, VPN, etc.)
```

**Solutions:**

**1. Increase timeout:**

```python
# In src/config/settings.py
DEFAULT_TIMEOUT = 30  # Increase from default 15
```

**2. Add retry logic:**

```bash
# Rankle already has retry logic built-in
# But you can adjust retries in session.py
```

**3. Check firewall:**

```bash
# Linux: Check iptables
sudo iptables -L

# Allow outbound HTTPS
sudo ufw allow out 443/tcp
```

---

### Problem: SSL verification failed

**Error Message:**

```
requests.exceptions.SSLError: HTTPSConnectionPool(host='example.com', port=443):
Max retries exceeded with url: / (Caused by SSLError(SSLCertVerificationError(...)))
```

**Cause:** Invalid/expired SSL certificate on target

**Solution 1:** This is expected behavior for security

```bash
# Rankle correctly reports this as:
# "SSL Grade: F - Certificate verification failed"
```

**Solution 2:** If you need to scan anyway (dev/testing)

```python
# Edit src/config/settings.py
VERIFY_SSL = False  # Use with caution!
```

**Note:** Only disable SSL verification for testing purposes. Production scans should always verify certificates.

---

### Problem: "Name or service not known"

**Error Message:**

```
socket.gaierror: [Errno -2] Name or service not known
```

**Cause:** DNS resolution failure

**Solutions:**

**1. Check domain spelling:**

```bash
# Make sure domain is correct
uv run python main.py example.com  # Not "exmaple.com"
```

**2. Try different DNS server:**

```python
# Edit src/config/settings.py
DNS_SERVERS = [
    "1.1.1.1",     # Cloudflare
    "8.8.8.8",     # Google
    "9.9.9.9",     # Quad9
]
```

**3. Check system DNS:**

```bash
# Test DNS resolution
nslookup example.com

# Check /etc/resolv.conf
cat /etc/resolv.conf
```

---

## DNS Resolution Failures

### Problem: No DNS records found

**Error Message:**

```
[!] No A records found for example.com
```

**Possible Causes:**

1. Domain doesn't exist
2. DNS server timeout
3. Domain has no A records (only AAAA, CNAME, etc.)

**Diagnosis:**

```bash
# Check all record types
dig example.com ANY

# Check specific records
dig example.com A
dig example.com AAAA
dig example.com CNAME
```

**Solution:** Domain may be valid but have unusual DNS setup

```bash
# Try scanning with IP directly
uv run python main.py 93.184.216.34

# Or use --ip flag if implemented
```

---

### Problem: DNS timeout

**Error Message:**

```
dns.exception.Timeout: The DNS query timed out
```

**Solutions:**

**1. Increase DNS timeout:**

```python
# In src/rankle/modules/dns.py
resolver.timeout = 10  # Increase from default
resolver.lifetime = 30  # Increase from default
```

**2. Use reliable DNS servers:**

```python
# src/config/settings.py
DNS_SERVERS = ["1.1.1.1", "8.8.8.8"]  # Fast, reliable
```

**3. Check network:**

```bash
# Test DNS connectivity
dig @1.1.1.1 example.com
dig @8.8.8.8 example.com
```

---

## SSL/TLS Certificate Errors

### Problem: Certificate verification error

**Error Message:**

```
[SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed
```

**Expected Behavior:** Rankle reports this correctly

```
SSL Grade: F
Issue: Certificate verification failed
```

**If you need details:**

```bash
# Use openssl to inspect
openssl s_client -connect example.com:443 -servername example.com

# Check expiration
echo | openssl s_client -connect example.com:443 2>/dev/null | openssl x509 -noout -dates
```

---

### Problem: Unable to extract certificate info

**Error Message:**

```
[!] SSL analysis failed: [SSL] record layer failure
```

**Cause:** SSL/TLS connection issues

**Diagnosis:**

```bash
# Test SSL/TLS versions
nmap --script ssl-enum-ciphers -p 443 example.com

# Check certificate chain
openssl s_client -showcerts -connect example.com:443
```

**Solution:** Target may have strict TLS requirements

```python
# Rankle uses requests library defaults (TLS 1.2+)
# This is generally sufficient for modern sites
```

---

## Rate Limiting & Blocking

### Problem: HTTP 429 (Too Many Requests)

**Error Message:**

```
HTTP 429: Too Many Requests
```

**Cause:** Target rate limiting your requests

**Solutions:**

**1. Increase delay between requests:**

```python
# src/config/settings.py
RATE_LIMIT_DELAY = 2.0  # Seconds between requests (increase from 1.0)
```

**2. Use slower scan mode:**

```bash
# If implemented, use --slow flag
uv run python main.py example.com --slow
```

**3. Scan fewer subdomains:**

```python
# Reduce subdomain wordlist size
# Or skip subdomain enumeration
```

**4. Wait and retry:**

```bash
# Rate limits often reset after time period
sleep 3600  # Wait 1 hour
uv run python main.py example.com
```

---

### Problem: HTTP 403 (Forbidden)

**Error Message:**

```
HTTP 403: Forbidden
```

**Possible Causes:**

1. WAF blocking your IP
2. Geographic restrictions
3. User-Agent filtering
4. IP-based blocking

**Solutions:**

**1. Check User-Agent:**

```python
# src/config/settings.py - Ensure realistic User-Agent
DEFAULT_USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64)..."
```

**2. Try from different network:**

```bash
# Use VPN or different IP
# Mobile hotspot, cloud VM, etc.
```

**3. Respect blocks:**

```
If consistently blocked, the target may not want scanning.
Consider reaching out for authorization.
```

---

### Problem: Cloudflare challenge page

**Error Message:**

```
Detected: Cloudflare (100%)
But page shows: "Checking your browser before accessing..."
```

**Cause:** Cloudflare JavaScript challenge or CAPTCHA

**Solution:** Rankle focuses on passive reconnaissance

```
Cloudflare challenges cannot be bypassed with passive tools.
This is working as intended - Rankle detects Cloudflare correctly.

For authorized testing, contact site owner for API access or WAF whitelist.
```

---

## Timeout Errors

### Problem: Request timeout

**Error Message:**

```
requests.exceptions.Timeout: HTTPSConnectionPool(host='example.com', port=443):
Read timed out. (read timeout=15)
```

**Solutions:**

**1. Increase global timeout:**

```python
# src/config/settings.py
DEFAULT_TIMEOUT = 30  # Increase from 15 seconds
```

**2. Check target responsiveness:**

```bash
# Measure response time
time curl -I https://example.com
```

**3. Network issues:**

```bash
# Check latency
ping example.com

# Trace route
traceroute example.com
```

**4. Scan during off-peak hours:**

```
Target may be slow during high traffic periods.
Try scanning at night or weekends.
```

---

## Detection Issues

### Problem: No technologies detected

**Error Message:**

```
Technologies Detected: 0
```

**Diagnosis:**

```bash
# Check if site is accessible
curl -I https://example.com

# Verify HTML is returned
curl https://example.com | head -50
```

**Possible Causes:**

1. Site uses uncommon technologies
2. Heavily minified/obfuscated code
3. SPA (Single Page Application) with late-loading content
4. WAF/CDN stripping identifying headers

**Solutions:**

**1. Try enhanced detection:**

```bash
uv run python main.py example.com
```

**2. Manual inspection:**

```bash
# Save full HTML
curl https://example.com > page.html

# Search for technology indicators
grep -i "generator\|powered\|built" page.html
```

**3. Check headers:**

```bash
curl -I https://example.com | grep -i "x-\|server"
```

---

### Problem: Wrong technology detected

**Example:** Reports "WordPress" but site is not WordPress

**Cause:** False positive from pattern matching

**Diagnosis:**

```bash
# Check confidence score
# Low confidence (< 50%) = likely false positive
```

**Solutions:**

**1. Check evidence:**

```json
// Look at detection evidence
{
  "name": "WordPress",
  "confidence": 0.3,  // LOW confidence
  "evidence": ["wp-includes"]  // May be coincidental match
}
```

**2. Report false positive:**

```
If consistently wrong, report issue with:
- Target domain
- Detected technology
- Actual technology
- Detection confidence
```

---

### Problem: Version not detected

**Message:**

```
Django detected (80%) - Version: Unknown
```

**Cause:** Version string not exposed in headers/HTML

**This is normal:**

```
Many production sites intentionally hide version info for security.
Rankle can only detect versions when explicitly exposed.
```

**Try:**

- Enhanced detection (may find versions in asset filenames)
- Error page fingerprinting (debug pages sometimes show versions)
- Favicon hashing (some versions have unique favicons)

---

## Output & Formatting Problems

### Problem: JSON output malformed

**Error Message:**

```
json.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)
```

**Solution:**

```bash
# Ensure using --output json flag
uv run python main.py example.com --output json > results.json

# Validate JSON
python -m json.tool results.json
```

---

### Problem: Unicode/emoji display issues

**Error Message:**

```
UnicodeEncodeError: 'ascii' codec can't encode character
```

**Solution:**

```bash
# Set UTF-8 encoding
export PYTHONIOENCODING=utf-8

# Or run with UTF-8
uv run python main.py example.com | iconv -f utf-8
```

---

### Problem: Output too verbose

**Solution:**

```bash
# Reduce verbosity (if --verbose flag used)
uv run python main.py example.com  # Without --verbose

# Redirect to file
uv run python main.py example.com > scan.txt 2>&1
```

---

## Performance Issues

### Problem: Scan very slow

**Symptoms:** Scan takes > 5 minutes

**Diagnosis:**

```bash
# Time the scan
time uv run python main.py example.com
```

**Common Causes & Solutions:**

**1. Network latency:**

```bash
# Check ping
ping example.com

# If > 200ms, expect slower scans
```

**2. Many subdomains:**

```
Subdomain enumeration can be slow.
Certificate Transparency logs may have thousands of entries.
```

**Solution:**

```python
# Limit subdomain results in future version
# Or skip subdomain enumeration
```

**3. Timeout settings too high:**

```python
# src/config/settings.py
DEFAULT_TIMEOUT = 15  # Don't set too high (e.g., 60)
```

---

### Problem: High memory usage

**Symptom:** Python process using > 1GB RAM

**Cause:** Large HTML responses or many subdomains

**Solutions:**

**1. Limit subdomain scanning:**

```python
# Reduce Certificate Transparency results
```

**2. Clear results between scans:**

```bash
# Don't accumulate scan results in memory
# Save to file after each scan
```

---

## Type Checking Errors

### Problem: pyright reports type errors

**Error Message:**

```
error: Incompatible types in assignment (expression has type "str | None", variable has type "str")
```

**Solution:** Run `pyright src/rankle/` for detailed type checking output

**Quick fixes:**

**1. Use type guards:**

```python
if result is not None:
    # Now pyright knows result is str, not str | None
    print(result.upper())
```

**2. Add type annotations:**

```python
def analyze(domain: str) -> dict[str, Any]:  # Not Dict[str, Any]
    ...
```

**3. Update imports:**

```python
# Python 3.13+ - No typing imports needed for built-ins
data: dict[str, list[int]] = {}  # Not Dict[str, List[int]]
```

---

## Getting Help

### Before Reporting Issues

**1. Check this troubleshooting guide**

**2. Test with known-good domain:**

```bash
# Should always work
uv run python main.py example.com
uv run python main.py google.com
```

**4. Check for updates:**

```bash
git pull
uv sync
```

### Reporting Issues

**Include in bug reports:**

1. Rankle version (`git log -1 --oneline`)
2. Python version (`python --version`)
3. Operating system
4. Full error message (use `--verbose` flag)
5. Target domain (if not sensitive)
6. Steps to reproduce
7. Expected vs actual behavior

**GitHub Issues:** <https://github.com/javicosvml/rankle/issues>

**Format:**

```markdown
**Environment:**
- Rankle version: 2.0.0
- Python: 3.13.x
- OS: Ubuntu 22.04

**Command:**
`uv run python main.py example.com --verbose`

**Error:**
```

[Full error message here]

```

**Expected:** Should detect technologies
**Actual:** No technologies detected

**Additional Context:** [Any other relevant info]
```

### Community Support

- **GitHub Discussions:** <https://github.com/javicosvml/rankle/discussions>
- **Documentation:** <https://github.com/javicosvml/rankle/tree/main/docs>
- **Examples:** See `docs/examples/` directory

### Emergency Workarounds

**If Rankle completely broken:**

**1. Use individual tools:**

```bash
# DNS enumeration
dig example.com ANY

# Technology detection
whatweb example.com

# Subdomain enumeration
subfinder -d example.com
```

**2. Fresh installation:**

```bash
# Nuclear option: start over
cd ..
rm -rf rankle
git clone https://github.com/javicosvml/rankle.git
cd rankle
uv sync
uv run python main.py example.com
```

---

## Debugging Tips

### Enable Debug Mode

```python
# In main.py or scanner.py, add:
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Verbose Output

```bash
# Use verbose flag if available
uv run python main.py example.com --verbose
```

### Isolate Components

```python
# Test individual modules
from src.rankle.modules.dns import DNSAnalyzer
analyzer = DNSAnalyzer("example.com")
print(analyzer.analyze())
```

### Check Configuration

```python
# Verify settings loaded correctly
from src.config.settings import *
print(f"Timeout: {DEFAULT_TIMEOUT}")
print(f"DNS Servers: {DNS_SERVERS}")
print(f"User-Agent: {DEFAULT_USER_AGENT}")
```

---

## Still Having Issues?

If this guide doesn't solve your problem:

1. **Search existing issues:** <https://github.com/javicosvml/rankle/issues>
2. **Ask in discussions:** <https://github.com/javicosvml/rankle/discussions>
3. **Open new issue:** <https://github.com/javicosvml/rankle/issues/new>

**Always include:**

- Rankle version
- Python version
- Operating system
- Full error message
- Steps to reproduce

---

**Last Updated:** 2026-01-20
**Maintained By:** Rankle Development Team
