# Rankle API Usage Examples

**Purpose:** Use Rankle as a Python library in your own projects
**Last Updated:** 2026-01-20

---

## Table of Contents

1. [Installation as Library](#installation-as-library)
2. [Basic Usage](#basic-usage)
3. [Module-by-Module Examples](#module-by-module-examples)
4. [Complete Integration Examples](#complete-integration-examples)
5. [Custom Detection Logic](#custom-detection-logic)
6. [Error Handling](#error-handling)
7. [Async/Concurrent Usage](#asyncconcurrent-usage)
8. [Integration Patterns](#integration-patterns)

---

## Installation as Library

### Install Rankle Package

```bash
# Install as editable package
uv pip install -e /path/to/rankle

# Or add to requirements.txt
# -e git+https://github.com/javicosvml/rankle.git@main#egg=rankle
```

### Verify Installation

```python
# Test import
import rankle
from rankle import RankleScanner
from rankle.detectors.technology import TechnologyDetector

print("Rankle imported successfully!")
```

---

## Basic Usage

### Simple Scan

```python
from rankle import RankleScanner

# Create scanner instance
scanner = RankleScanner("example.com", verbose=False)

# Run full scan
results = scanner.run_full_scan()

# Access results
print(f"Domain: {results['domain']}")
print(f"Technologies: {len(results['technologies'])} detected")
print(f"CDN: {results.get('cdn', {}).get('detected', False)}")
```

### Basic Scan (Fewer Modules)

```python
from rankle import RankleScanner

scanner = RankleScanner("example.com")

# Run only basic scan (DNS + HTTP + SSL)
results = scanner.run_basic_scan()

# results contains:
# - domain
# - dns
# - http
# - ssl
```

---

## Module-by-Module Examples

### DNS Analysis

```python
from rankle.modules.dns import DNSAnalyzer

# Initialize DNS analyzer
dns = DNSAnalyzer("example.com")

# Perform DNS analysis
results = dns.analyze()

# Access DNS records
print(f"A Records: {results['A']}")
print(f"MX Records: {results['MX']}")
print(f"NS Records: {results['NS']}")
print(f"TXT Records: {results['TXT']}")

# Check if domain exists
if results['exists']:
    print(f"Domain resolves to: {results['A']}")
```

**Output Structure:**

```python
{
    'exists': True,
    'A': ['93.184.216.34'],
    'AAAA': ['2606:2800:220:1:248:1893:25c8:1946'],
    'MX': ['10 mail.example.com.'],
    'NS': ['ns1.example.com.', 'ns2.example.com.'],
    'TXT': ['v=spf1 include:_spf.example.com ~all'],
    'SOA': {...},
    'CNAME': []
}
```

---

### Technology Detection

```python
from rankle.detectors.technology import TechnologyDetector
import requests

# Fetch page
response = requests.get("https://example.com")
headers = dict(response.headers)
cookies = [cookie.name for cookie in response.cookies]
html = response.text

# Traditional detection
detector = TechnologyDetector("example.com")
results = detector.detect(
    headers=headers,
    cookies=cookies,
    body=html
)

# Access detected technologies
for tech in results['technologies']:
    print(f"- {tech['name']} ({tech['confidence']*100}%)")
    if tech.get('version'):
        print(f"  Version: {tech['version']}")
```

**Enhanced Detection (v2.0):**

```python
# Use enhanced detection
enhanced_results = detector.detect_enhanced(
    headers=headers,
    cookies=cookies,
    body=html,
    base_url="https://example.com"
)

# Additional v2.0 features:
print(f"API Endpoints: {enhanced_results.get('api_endpoints', [])}")
print(f"WordPress: {enhanced_results.get('wordpress', {}).get('detected', False)}")
print(f"CVE Mappings: {len(enhanced_results.get('cve_mappings', []))}")
```

---

### CDN Detection

```python
from rankle.detectors.cdn import CDNDetector

detector = CDNDetector("example.com")
results = detector.detect(headers=headers, body=html)

if results['detected']:
    print(f"CDN: {results['provider']} ({results['confidence']*100}%)")
    print(f"Evidence: {results['evidence']}")
else:
    print("No CDN detected")
```

---

### WAF Detection

```python
from rankle.detectors.waf import WAFDetector

detector = WAFDetector("example.com")
results = detector.detect(headers=headers, body=html)

if results['detected']:
    print(f"WAF: {results['provider']} ({results['confidence']*100}%)")
    print("Target is protected by WAF")
else:
    print("No WAF detected")
```

---

### SSL/TLS Analysis

```python
from rankle.modules.ssl import SSLAnalyzer

analyzer = SSLAnalyzer("example.com")
results = analyzer.analyze()

print(f"SSL Grade: {results['grade']}")
print(f"Issuer: {results['issuer']}")
print(f"Valid Until: {results['valid_until']}")
print(f"Subject Alternative Names: {results['san']}")
```

---

### Subdomain Discovery

```python
from rankle.modules.subdomains import SubdomainEnumerator

enumerator = SubdomainEnumerator("example.com")
results = enumerator.discover()

print(f"Found {results['total']} subdomains")
for subdomain in results['subdomains']:
    print(f"- {subdomain['domain']} (Source: {subdomain['source']})")
    if subdomain['live']:
        print(f"  Status: LIVE")
```

---

### Security Headers

```python
from rankle.modules.security_headers import SecurityHeadersAnalyzer

analyzer = SecurityHeadersAnalyzer("example.com")
results = analyzer.analyze(headers=headers)

print(f"Security Grade: {results['grade']}")
print(f"Score: {results['score']}/100")
print(f"Present: {results['headers_present']}")
print(f"Missing: {results['headers_missing']}")
```

---

### Origin Discovery

```python
from rankle.detectors.origin import OriginDiscovery

discovery = OriginDiscovery("example.com")
results = discovery.discover(dns_results=dns_data, subdomain_results=subdomain_data)

print(f"Found {len(results['origins'])} potential origin IPs:")
for origin in results['origins']:
    print(f"- {origin['ip']} via {origin['method']}")
    if origin.get('cloud_provider'):
        print(f"  Provider: {origin['cloud_provider']}")
```

---

## Complete Integration Examples

### Example 1: Custom Security Audit Script

```python
#!/usr/bin/env python3
"""
Custom security audit script using Rankle as library.
"""

from rankle import RankleScanner
from rankle.modules.security_headers import SecurityHeadersAnalyzer
import json

def audit_website(domain: str) -> dict:
    """Perform security audit on domain."""

    print(f"[*] Auditing {domain}...")

    # Full scan
    scanner = RankleScanner(domain, verbose=False)
    results = scanner.run_full_scan()

    # Analyze security
    audit_report = {
        'domain': domain,
        'security_score': 0,
        'issues': [],
        'recommendations': []
    }

    # Check SSL
    if results['ssl']['grade'] in ['F', 'E']:
        audit_report['issues'].append({
            'severity': 'HIGH',
            'category': 'SSL/TLS',
            'issue': f"Poor SSL grade: {results['ssl']['grade']}",
            'recommendation': 'Update SSL certificate and configuration'
        })
    else:
        audit_report['security_score'] += 25

    # Check Security Headers
    if results['security_headers']['grade'] in ['F', 'E']:
        audit_report['issues'].append({
            'severity': 'HIGH',
            'category': 'Security Headers',
            'issue': f"Missing critical headers: {results['security_headers']['headers_missing']}",
            'recommendation': 'Implement security headers (CSP, HSTS, X-Frame-Options)'
        })
    else:
        audit_report['security_score'] += 25

    # Check WAF
    if not results['waf']['detected']:
        audit_report['issues'].append({
            'severity': 'MEDIUM',
            'category': 'WAF',
            'issue': 'No Web Application Firewall detected',
            'recommendation': 'Consider implementing WAF (Cloudflare, AWS WAF, etc.)'
        })
    else:
        audit_report['security_score'] += 25

    # Check CDN
    if results['cdn']['detected']:
        audit_report['security_score'] += 25

    # Calculate final score
    audit_report['security_score'] = min(audit_report['security_score'], 100)

    return audit_report


if __name__ == "__main__":
    domain = "example.com"
    report = audit_website(domain)

    # Save report
    with open(f"{domain}_security_audit.json", "w") as f:
        json.dump(report, f, indent=2)

    print(f"\n[+] Security Score: {report['security_score']}/100")
    print(f"[+] Issues Found: {len(report['issues'])}")
```

---

### Example 2: Technology Stack Inventory

```python
#!/usr/bin/env python3
"""
Generate technology stack inventory for multiple domains.
"""

from rankle.detectors.technology import TechnologyDetector
import requests
import pandas as pd

def inventory_technology_stack(domains: list[str]) -> pd.DataFrame:
    """Create inventory of all technologies across domains."""

    inventory = []

    for domain in domains:
        print(f"[*] Analyzing {domain}...")

        try:
            # Fetch page
            response = requests.get(f"https://{domain}", timeout=15)
            headers = dict(response.headers)
            cookies = [c.name for c in response.cookies]
            html = response.text

            # Detect technologies
            detector = TechnologyDetector(domain)
            results = detector.detect_enhanced(
                headers=headers,
                cookies=cookies,
                body=html,
                base_url=f"https://{domain}"
            )

            # Add to inventory
            for tech in results['technologies']:
                inventory.append({
                    'domain': domain,
                    'technology': tech['name'],
                    'category': tech.get('category', 'Unknown'),
                    'version': tech.get('version', 'Unknown'),
                    'confidence': tech['confidence']
                })

        except Exception as e:
            print(f"[!] Error analyzing {domain}: {e}")

    # Convert to DataFrame
    df = pd.DataFrame(inventory)
    return df


if __name__ == "__main__":
    domains = ["example.com", "github.com", "python.org"]

    # Generate inventory
    inventory_df = inventory_technology_stack(domains)

    # Save to CSV
    inventory_df.to_csv("technology_inventory.csv", index=False)

    # Print summary
    print("\nTechnology Summary:")
    print(inventory_df.groupby('technology').size().sort_values(ascending=False))
```

---

### Example 3: Continuous Monitoring

```python
#!/usr/bin/env python3
"""
Monitor domain for changes over time.
"""

import time
import json
from datetime import datetime
from rankle import RankleScanner

def monitor_domain(domain: str, interval: int = 3600):
    """Monitor domain and detect changes."""

    previous_results = None

    while True:
        print(f"[{datetime.now()}] Scanning {domain}...")

        # Scan
        scanner = RankleScanner(domain, verbose=False)
        current_results = scanner.run_full_scan()

        # Compare with previous
        if previous_results:
            changes = detect_changes(previous_results, current_results)

            if changes:
                print(f"[!] Changes detected!")
                for change in changes:
                    print(f"  - {change}")

                # Alert (email, webhook, etc.)
                alert_on_changes(domain, changes)

        # Save snapshot
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        with open(f"snapshots/{domain}_{timestamp}.json", "w") as f:
            json.dump(current_results, f, indent=2)

        previous_results = current_results

        # Wait
        print(f"[*] Waiting {interval} seconds...")
        time.sleep(interval)


def detect_changes(old: dict, new: dict) -> list[str]:
    """Detect changes between scans."""
    changes = []

    # Check technology changes
    old_techs = set(t['name'] for t in old.get('technologies', []))
    new_techs = set(t['name'] for t in new.get('technologies', []))

    added = new_techs - old_techs
    removed = old_techs - new_techs

    if added:
        changes.append(f"Technologies added: {', '.join(added)}")
    if removed:
        changes.append(f"Technologies removed: {', '.join(removed)}")

    # Check CDN changes
    if old['cdn']['detected'] != new['cdn']['detected']:
        changes.append(f"CDN status changed")

    # Check SSL changes
    if old['ssl']['grade'] != new['ssl']['grade']:
        changes.append(f"SSL grade changed: {old['ssl']['grade']} → {new['ssl']['grade']}")

    return changes


def alert_on_changes(domain: str, changes: list[str]):
    """Send alerts on detected changes."""
    # Implement: Email, Slack, webhook, etc.
    pass


if __name__ == "__main__":
    monitor_domain("example.com", interval=3600)  # Check hourly
```

---

## Custom Detection Logic

### Add Custom Technology Signatures

```python
from rankle.detectors.technology import TechnologyDetector

# Extend TechnologyDetector
class CustomTechnologyDetector(TechnologyDetector):
    """Custom detector with additional signatures."""

    def detect_custom_cms(self, body: str) -> dict:
        """Detect custom/proprietary CMS."""

        custom_signatures = {
            "MyCustomCMS": {
                "patterns": ["mycms-admin", "mycms.js"],
                "confidence": 0.9
            }
        }

        for cms, signature in custom_signatures.items():
            for pattern in signature['patterns']:
                if pattern in body.lower():
                    return {
                        'name': cms,
                        'confidence': signature['confidence'],
                        'evidence': f"Pattern: {pattern}"
                    }

        return None

    def detect(self, headers, cookies, body):
        """Override detect to include custom logic."""

        # Run standard detection
        results = super().detect(headers, cookies, body)

        # Add custom detection
        custom_result = self.detect_custom_cms(body)
        if custom_result:
            results['technologies'].append(custom_result)

        return results


# Usage
detector = CustomTechnologyDetector("example.com")
results = detector.detect(headers, cookies, html)
```

---

## Error Handling

### Robust Scanning with Error Handling

```python
from rankle import RankleScanner
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def safe_scan(domain: str) -> dict | None:
    """Scan domain with comprehensive error handling."""

    try:
        scanner = RankleScanner(domain, verbose=False)
        results = scanner.run_full_scan()
        logger.info(f"Successfully scanned {domain}")
        return results

    except ConnectionError as e:
        logger.error(f"Connection error for {domain}: {e}")
        return None

    except TimeoutError as e:
        logger.error(f"Timeout scanning {domain}: {e}")
        return None

    except Exception as e:
        logger.error(f"Unexpected error scanning {domain}: {e}")
        return None


# Usage
domains = ["example.com", "invalid-domain.xyz", "timeout-site.com"]

for domain in domains:
    results = safe_scan(domain)
    if results:
        print(f"✅ {domain}: {len(results['technologies'])} technologies")
    else:
        print(f"❌ {domain}: Scan failed")
```

---

## Async/Concurrent Usage

### Concurrent Scanning with asyncio

```python
import asyncio
from concurrent.futures import ThreadPoolExecutor
from rankle import RankleScanner

def scan_domain(domain: str) -> dict:
    """Synchronous scan function."""
    scanner = RankleScanner(domain, verbose=False)
    return scanner.run_full_scan()


async def scan_domains_async(domains: list[str]) -> list[dict]:
    """Scan multiple domains concurrently."""

    loop = asyncio.get_event_loop()

    # Use thread pool for I/O-bound tasks
    with ThreadPoolExecutor(max_workers=5) as executor:
        # Submit all tasks
        tasks = [
            loop.run_in_executor(executor, scan_domain, domain)
            for domain in domains
        ]

        # Wait for all to complete
        results = await asyncio.gather(*tasks, return_exceptions=True)

    return results


# Usage
async def main():
    domains = ["example.com", "google.com", "github.com"]

    print(f"Scanning {len(domains)} domains concurrently...")
    results = await scan_domains_async(domains)

    for domain, result in zip(domains, results):
        if isinstance(result, Exception):
            print(f"❌ {domain}: Error - {result}")
        else:
            print(f"✅ {domain}: {len(result['technologies'])} technologies")


if __name__ == "__main__":
    asyncio.run(main())
```

---

## Integration Patterns

### Flask API Wrapper

```python
from flask import Flask, jsonify, request
from rankle import RankleScanner

app = Flask(__name__)

@app.route('/scan', methods=['POST'])
def scan_endpoint():
    """API endpoint to scan a domain."""

    data = request.get_json()
    domain = data.get('domain')

    if not domain:
        return jsonify({'error': 'Domain required'}), 400

    try:
        scanner = RankleScanner(domain, verbose=False)
        results = scanner.run_full_scan()
        return jsonify(results)

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

**Usage:**

```bash
curl -X POST http://localhost:5000/scan \
  -H "Content-Type: application/json" \
  -d '{"domain": "example.com"}'
```

---

### Django Integration

```python
# views.py
from django.http import JsonResponse
from rankle import RankleScanner

def scan_view(request):
    """Django view to scan domain."""

    domain = request.GET.get('domain')

    if not domain:
        return JsonResponse({'error': 'Domain required'}, status=400)

    try:
        scanner = RankleScanner(domain, verbose=False)
        results = scanner.run_full_scan()
        return JsonResponse(results)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
```

---

### Celery Background Tasks

```python
from celery import Celery
from rankle import RankleScanner

app = Celery('tasks', broker='redis://localhost:6379/0')

@app.task
def scan_domain_task(domain: str):
    """Background task to scan domain."""

    scanner = RankleScanner(domain, verbose=False)
    results = scanner.run_full_scan()

    # Save to database, send notification, etc.
    save_results(results)

    return results


# Usage
result = scan_domain_task.delay("example.com")
print(f"Task ID: {result.id}")
```

---

## Best Practices

### 1. Always Use Virtual Environments

```bash
uv sync
```

### 2. Handle Errors Gracefully

```python
try:
    results = scanner.run_full_scan()
except Exception as e:
    logger.error(f"Scan failed: {e}")
    # Fallback logic
```

### 3. Rate Limit Your Scans

```python
import time

for domain in domains:
    scan_domain(domain)
    time.sleep(5)  # Respectful delay
```

### 4. Cache Results

```python
import functools
from datetime import datetime, timedelta

@functools.lru_cache(maxsize=100)
def cached_scan(domain: str, cache_time: int = 3600):
    """Cache scan results for 1 hour."""
    return scan_domain(domain)
```

### 5. Use Type Hints

```python
from typing import Any

def process_results(results: dict[str, Any]) -> None:
    """Process scan results with type hints."""
    ...
```

---

## See Also

- **[Architecture](architecture.md)** - Understanding Rankle's structure
- **[Detection Capabilities](detection-capabilities.md)** - Available detection modules
- **[Troubleshooting](troubleshooting.md)** - Common issues and solutions
- **[Performance Tuning](performance-tuning.md)** - Optimization strategies

---

**Last Updated:** 2026-01-20
**Maintained By:** Rankle Development Team

**Questions?** Open an issue on GitHub: <https://github.com/javicosvml/rankle/issues>
