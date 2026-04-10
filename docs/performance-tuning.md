# Rankle Performance Tuning Guide

**Purpose:** Optimize Rankle for speed, efficiency, and resource usage
**Last Updated:** 2026-01-20

---

## Table of Contents

1. [Performance Overview](#performance-overview)
2. [Timeout Configuration](#timeout-configuration)
3. [Rate Limiting](#rate-limiting)
4. [Concurrent Scanning](#concurrent-scanning)
5. [DNS Optimization](#dns-optimization)
6. [Memory Optimization](#memory-optimization)
7. [Network Optimization](#network-optimization)
8. [Detection Trade-offs](#detection-trade-offs)
9. [Batch Scanning](#batch-scanning)
10. [Profiling & Benchmarking](#profiling--benchmarking)

---

## Performance Overview

### Default Performance Characteristics

**Single Domain Scan:**

- **Traditional Detection:** 15-25 seconds
- **Enhanced Detection (v2.0):** 30-45 seconds
- **With Subdomain Enum:** 45-120 seconds (depends on subdomain count)

**Breakdown by Module:**

| Module | Time | Optimization Potential |
|--------|------|----------------------|
| DNS Analysis | 2-3s | Low (network bound) |
| HTTP Fetch | 1-2s | Medium (timeout tuning) |
| SSL Analysis | 1-2s | Low (TLS handshake) |
| Technology Detection | 2-3s | Low |
| Enhanced Detection (v2.0) | +15-25s | Medium (selective modules) |
| CDN/WAF Detection | 1-2s | Low |
| Security Headers | <1s | None |
| Origin Discovery | 5-10s | Medium (parallel DNS) |
| Subdomain Discovery | 30-90s | High (limit results) |

### Performance Tuning Philosophy

**Trade-offs:**

1. **Speed vs. Completeness** - Faster scans may miss some detections
2. **Timeout vs. Reliability** - Shorter timeouts may fail on slow targets
3. **Concurrency vs. Rate Limiting** - More parallel requests = higher chance of blocking

---

## Timeout Configuration

### Understanding Timeouts

**Location:** `config/settings.py`

```python
# Global timeout for all HTTP requests
DEFAULT_TIMEOUT = 15  # seconds
```

### Timeout Tuning Strategies

**Fast Scanning (Aggressive):**

```python
# Optimized for speed, may miss slow targets
DEFAULT_TIMEOUT = 10

# Trade-off:
# ✅ 30-40% faster scans
# ❌ May fail on slow servers
# ❌ Higher error rate
```

**Balanced (Default):**

```python
# Good balance between speed and reliability
DEFAULT_TIMEOUT = 15

# Trade-off:
# ✅ Reliable for most targets
# ✅ Reasonable speed
# ⚖️ Standard approach
```

**Thorough Scanning (Conservative):**

```python
# Prioritizes completeness over speed
DEFAULT_TIMEOUT = 30

# Trade-off:
# ✅ Catches slow-responding targets
# ✅ Lower error rate
# ❌ 50-100% slower scans
```

### Per-Module Timeout Tuning

**Advanced:** Different timeouts for different operations

```python
# In rankle/core/session.py
class SessionManager:
    def __init__(self, timeout: int = DEFAULT_TIMEOUT):
        self.timeout = timeout
        self.dns_timeout = timeout * 0.5  # DNS should be faster
        self.ssl_timeout = timeout * 0.75  # TLS handshake
        self.http_timeout = timeout  # Full HTTP request
```

---

## Rate Limiting

### Purpose

**Why Rate Limit:**

- Avoid triggering WAF/IDS
- Respect target resources
- Prevent IP blocking
- Ethical scanning practices

### Configuration

**Location:** `config/settings.py`

```python
# Delay between requests (seconds)
RATE_LIMIT_DELAY = 1.0
```

### Tuning Strategies

**Fast Scanning (Use with caution):**

```python
RATE_LIMIT_DELAY = 0.5  # Half second between requests

# Risk:
# ⚠️ Higher chance of rate limiting (HTTP 429)
# ⚠️ May trigger WAF blocks
# ⚠️ Unethical for production sites
```

**Standard Scanning:**

```python
RATE_LIMIT_DELAY = 1.0  # 1 second (default)

# Balanced approach for most targets
```

**Polite Scanning:**

```python
RATE_LIMIT_DELAY = 2.0  # 2 seconds

# Recommended for:
# ✅ Production sites
# ✅ Sites with strict rate limiting
# ✅ Bug bounty programs (be respectful)
```

**Stealth Scanning:**

```python
RATE_LIMIT_DELAY = 5.0  # 5 seconds

# Ultra-conservative, blends with normal traffic
# Use for sensitive engagements
```

### Adaptive Rate Limiting

**Idea:** Adjust rate based on responses

```python
# Pseudo-code for future implementation
if response.status_code == 429:
    RATE_LIMIT_DELAY *= 2  # Back off
elif response.status_code == 200:
    RATE_LIMIT_DELAY *= 0.9  # Speed up gradually
```

---

## Concurrent Scanning

### Current Implementation

Rankle uses sequential scanning (one request at a time) for safety.

### Why Not Concurrent by Default?

**Reasons:**

1. **Rate limiting** - Harder to control with concurrency
2. **Target courtesy** - Avoid overwhelming servers
3. **Blocking risk** - Parallel requests = more suspicious
4. **Simplicity** - Easier to debug sequential scans

### Future Concurrent Scanning

**Planned for v2.1:**

```python
# --concurrent flag (future)
python main.py example.com --concurrent 5

# Runs up to 5 modules simultaneously
# Example: DNS + SSL + HTTP fetch in parallel
```

**Safe Concurrency:**

- Parallel module execution (DNS while fetching HTTP)
- NOT parallel requests to same domain
- Respects rate limiting between all requests

---

## DNS Optimization

### DNS Server Selection

**Impact:** DNS is often the slowest part of reconnaissance

**Configuration:** `config/settings.py`

```python
DNS_SERVERS = [
    "1.1.1.1",     # Cloudflare (very fast)
    "8.8.8.8",     # Google (reliable)
    "9.9.9.9",     # Quad9 (privacy-focused)
]
```

### Fastest DNS Servers (2026)

**Performance Ranking:**

1. **Cloudflare (1.1.1.1)** - ~14ms average
2. **Google (8.8.8.8)** - ~20ms average
3. **Quad9 (9.9.9.9)** - ~25ms average
4. **OpenDNS (208.67.222.222)** - ~30ms average

**Recommendation:** Use Cloudflare DNS for fastest queries

### DNS Caching

**Local DNS Cache:**

```bash
# Install systemd-resolved (Ubuntu/Debian)
sudo apt install systemd-resolved
sudo systemctl enable --now systemd-resolved

# Performance gain: 10-50ms per repeated query
```

**Rankle DNS Cache:**
Future feature - cache DNS responses during scan session

---

## Memory Optimization

### Memory Usage Profile

**Typical Memory Usage:**

- **Basic Scan:** 50-150 MB
- **With Subdomains:** 200-500 MB (depends on subdomain count)
- **Enhanced Detection:** 150-300 MB (Wappalyzer database)

### Optimization Strategies

**1. Limit Subdomain Results:**

```python
# In rankle/modules/subdomains.py
# Future: Add MAX_SUBDOMAINS configuration
MAX_SUBDOMAINS = 100  # Stop after 100 subdomains found
```

**2. Stream Large Responses:**

```python
# For very large HTML pages (future optimization)
response = session.get(url, stream=True)
# Process in chunks instead of loading full page
```

**3. Clear Results Between Batch Scans:**

```python
# When scanning multiple domains
for domain in domains:
    scanner = RankleScanner(domain)
    results = scanner.run_full_scan()
    # Save results
    save_results(results)
    # Scanner is garbage collected, memory freed
    del scanner
```

### Docker Memory Limits

```bash
# Limit Rankle container to 512MB
docker run --memory="512m" --memory-swap="512m" rankle example.com

# Monitor memory usage
docker stats
```

---

## Network Optimization

### Connection Pooling

**Rankle uses requests.Session()** - Automatic connection pooling

**Benefits:**

- Reuses TCP connections
- Faster subsequent requests (no handshake)
- Lower latency

**Configuration:**

```python
# In rankle/core/session.py
# Adjust pool size for future concurrent scanning
adapter = HTTPAdapter(
    pool_connections=10,  # Connection pools
    pool_maxsize=20,      # Max connections per pool
    max_retries=Retry(...)
)
```

### Retry Logic

**Current Implementation:**

```python
# Exponential backoff retry
retries = Retry(
    total=3,                    # Max 3 retries
    backoff_factor=1,           # Wait 1s, 2s, 4s
    status_forcelist=[429, 500, 502, 503, 504],
)
```

**Tuning for Speed:**

```python
# Aggressive (faster but less reliable)
retries = Retry(
    total=2,              # Only 2 retries
    backoff_factor=0.5,   # Shorter waits
)
```

**Tuning for Reliability:**

```python
# Conservative (slower but more complete)
retries = Retry(
    total=5,              # More retries
    backoff_factor=2,     # Longer waits (2s, 4s, 8s, 16s, 32s)
)
```

### Network Latency

**Test Latency:**

```bash
# Ping target
ping example.com

# If latency > 200ms, expect slower scans
# If latency > 500ms, consider increasing timeouts
```

**Solutions for High Latency:**

```python
# Adjust timeout based on latency
DEFAULT_TIMEOUT = base_latency * 3

# Example: 200ms latency = 0.6s minimum, use 20s timeout
```

---

## Detection Trade-offs

### Traditional vs. Enhanced Detection

**Traditional Detection (Fast):**

- **Time:** 15-25 seconds
- **Technologies:** 50-100
- **Methods:** Headers, cookies, HTML patterns
- **Use When:** Speed is priority, basic detection sufficient

**Enhanced Detection v2.0 (Thorough):**

- **Time:** 30-45 seconds
- **Technologies:** 3000+
- **Methods:** + Wappalyzer, favicon, error pages, JS analysis
- **Use When:** Completeness is priority, detailed inventory needed

### Selective Enhanced Detection

**Future Feature:** Enable only specific v2.0 modules

```python
# Pseudo-code for future implementation
results = detector.detect_enhanced(
    enable_wappalyzer=True,      # +3s, +2950 technologies
    enable_favicon_hash=False,   # Skip (saves ~1s)
    enable_error_fingerprint=False,  # Skip (saves ~1s)
    enable_js_analysis=True,     # +3s, API endpoint discovery
    enable_wordpress_scan=False, # Skip (saves ~2s)
    enable_cve_mapping=True,     # +1s, vulnerability URLs
)
```

### Smart Detection

**Idea:** Only run relevant modules based on initial detection

```python
# If WordPress detected in traditional scan
if "WordPress" in initial_results:
    # Then run WordPress plugin enumeration
    run_wordpress_deep_scan()

# If JS framework detected
if any_js_framework_detected:
    # Then run JS endpoint extraction
    run_js_analysis()
```

---

## Batch Scanning

### Scanning Multiple Domains

**Sequential (Current):**

```bash
# Scan multiple domains one by one
for domain in $(cat domains.txt); do
    python main.py "$domain" -o json > "${domain}.json"
done
```

**Performance:** N domains × ~30 seconds = total time

### Parallel Batch Scanning

**Using GNU Parallel:**

```bash
# Install
sudo apt install parallel

# Scan 5 domains concurrently
cat domains.txt | parallel -j 5 'python main.py {} -o json > {}.json'

# Performance: N domains ÷ 5 × ~30 seconds
# Example: 100 domains in ~10 minutes vs 50 minutes
```

**Using Bash Background Jobs:**

```bash
# Scan up to 5 at a time
while read domain; do
    python main.py "$domain" -o json > "${domain}.json" &

    # Limit to 5 concurrent
    if (( $(jobs -r | wc -l) >= 5 )); then
        wait -n  # Wait for any job to finish
    fi
done < domains.txt

wait  # Wait for all remaining jobs
```

### Considerations for Batch Scanning

**Rate Limiting:**

- Each scan makes ~10-20 requests
- 5 parallel scans = 50-100 requests across different domains
- Generally safe (different targets)

**Resource Usage:**

- 5 parallel scans = ~1GB RAM total
- Monitor with `htop` or `docker stats`

**Network:**

- May saturate connection on slow networks
- Consider reducing concurrency on mobile/slow connections

---

## Profiling & Benchmarking

### Built-in Timing

**Rankle shows timing per module:**

```
[1/8] DNS Analysis... (2.3s)
[2/8] Fetching HTTP Response... (1.5s)
[3/8] Analyzing SSL/TLS Certificate... (1.2s)
...
```

### Detailed Profiling

**Using Python cProfile:**

```bash
# Profile a scan
python -m cProfile -s cumtime main.py example.com

# Output shows time spent in each function
```

**Using time:**

```bash
# Simple timing
time python main.py example.com

# Output:
# real    0m32.450s  # Total wall-clock time
# user    0m2.130s   # CPU time
# sys     0m0.340s   # System time
```

### Benchmarking Script

**Create benchmark.sh:**

```bash
#!/bin/bash
# Benchmark Rankle performance

domains=("example.com" "google.com" "github.com")

echo "Domain,Time(s)" > benchmark.csv

for domain in "${domains[@]}"; do
    start=$(date +%s.%N)
    python main.py "$domain" > /dev/null 2>&1
    end=$(date +%s.%N)

    runtime=$(echo "$end - $start" | bc)
    echo "$domain,$runtime" >> benchmark.csv
done

# Calculate average
awk -F',' 'NR>1 {sum+=$2; count++} END {print "Average:", sum/count, "seconds"}' benchmark.csv
```

### Bottleneck Identification

**Common Bottlenecks:**

1. **Subdomain Enumeration** (30-90s) - Largest time sink
2. **Enhanced Detection** (+15-25s) - Wappalyzer + all v2.0 modules
3. **DNS Queries** (2-5s) - Network latency
4. **HTTP Requests** (1-3s per request) - Target response time

**Optimization Priority:**

1. Skip subdomain enum if not needed
2. Use traditional detection if sufficient
3. Optimize DNS (use fast servers, caching)
4. Tune timeouts appropriately

---

## Performance Monitoring

### Real-time Monitoring

**During Scan:**

```bash
# Monitor CPU/memory
htop

# Monitor network
iftop

# Monitor specific process
watch -n 1 'ps aux | grep python'
```

### Logging Performance Metrics

**Add to scanner.py:**

```python
import time

start_time = time.time()
results = module.analyze()
end_time = time.time()

print(f"[DEBUG] {module_name} took {end_time - start_time:.2f}s")
```

---

## Performance Best Practices Summary

### For Speed

✅ Use traditional detection (skip enhanced)
✅ Reduce timeout to 10-12 seconds
✅ Use Cloudflare DNS (1.1.1.1)
✅ Skip subdomain enumeration if not needed
✅ Use batch scanning with parallel for multiple domains
✅ Reduce rate limit delay to 0.5s (if target allows)

### For Completeness

✅ Use enhanced detection v2.0
✅ Increase timeout to 20-30 seconds
✅ Use conservative rate limit (2-5s delay)
✅ Enable all subdomain sources
✅ Scan during target's off-peak hours

### For Reliability

✅ Use default timeouts (15s)
✅ Conservative retry logic (5 attempts)
✅ Rate limit at 1-2s
✅ Monitor for 429/403 responses
✅ Use realistic User-Agent

### Resource Constraints

✅ Limit subdomain results
✅ Use Docker with memory limits
✅ Clear results between batch scans
✅ Reduce concurrent batch scanning

---

## Quick Reference

**Scan Profiles:**

```bash
# Fast Scan (15-20s)
# config/settings.py:
DEFAULT_TIMEOUT = 10
RATE_LIMIT_DELAY = 0.5

# Balanced Scan (25-35s) - DEFAULT
DEFAULT_TIMEOUT = 15
RATE_LIMIT_DELAY = 1.0

# Thorough Scan (40-60s)
DEFAULT_TIMEOUT = 30
RATE_LIMIT_DELAY = 2.0

# Stealth Scan (60-120s)
DEFAULT_TIMEOUT = 30
RATE_LIMIT_DELAY = 5.0
```

---

**Last Updated:** 2026-01-20
**Maintained By:** Rankle Development Team

**See Also:**

- [Troubleshooting Guide](troubleshooting.md) - Common issues and solutions
- [Detection Capabilities](detection-capabilities.md) - Feature documentation
- [Development Guide](development.md) - Contributing and development setup
