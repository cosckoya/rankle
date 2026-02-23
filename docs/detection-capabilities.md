# Detection Capabilities Reference

> **Rankle**: Comprehensive web infrastructure reconnaissance using 100% passive techniques

This document provides a complete reference for Rankle's detection capabilities, including signatures, patterns, and integration examples.

## Table of Contents

1. [CMS Detection (16+)](#cms-detection)
2. [Cloud Provider Detection (14+)](#cloud-provider-detection)
3. [CDN Detection (20+)](#cdn-detection)
4. [WAF Detection (20+)](#waf-detection)
5. [JavaScript Library Detection (15+)](#javascript-library-detection)
6. [Advanced Technology Detection (50+)](#advanced-technology-detection)
7. **[Enhanced Detection v2.0 (3000+ Technologies)](#enhanced-detection-v20)** ⭐ NEW
8. [Origin Infrastructure Discovery](#origin-infrastructure-discovery)
9. [Advanced HTTP Fingerprinting](#advanced-http-fingerprinting)
10. [Integration Examples](#integration-examples)
11. [Full Reconnaissance Pipeline](#full-reconnaissance-pipeline)

---

## CMS Detection

Rankle detects **16+ Content Management Systems** using multiple passive techniques.

### Detection Methods

- **HTML Pattern Matching**: Unique strings, CSS classes, JavaScript references
- **Meta Generator Tags**: `<meta name="generator" content="...">`
- **Cookie Analysis**: Framework-specific session cookies
- **HTTP Headers**: Server-specific headers (e.g., `X-Drupal-Cache`)
- **Exposed Files**: Configuration files, admin panels, API endpoints
- **Version Extraction**: Regex patterns for version numbers

### Drupal (Enhanced Detection)

Rankle includes **15+ detection patterns** specifically for Drupal:

#### Core Patterns
```
/core/misc/drupal.js          # Drupal 8+ core JavaScript
/misc/drupal.js               # Drupal 7 core JavaScript
/sites/default/               # Default site directory
/modules/                     # Modules directory
/themes/                      # Themes directory
```

#### HTML Attributes
```html
data-drupal-*                 # Drupal data attributes
views-                        # Views module classes
block-                        # Block system classes
node-                         # Node type classes
region-                       # Region classes
```

#### API Endpoints
```
/user/login                   # Login form
/admin                        # Admin interface
/node/add                     # Content creation
/?q=admin                     # Drupal 7 admin path
/jsonapi                      # JSON:API (Drupal 8+)
```

#### robots.txt Analysis
```
# Drupal-specific entries in robots.txt:
/admin/
/user/register/
/user/password/
/user/login/
/core/
```

#### Meta Tags
```html
<meta name="Generator" content="Drupal 8" />
<meta name="Generator" content="Drupal 9" />
<meta name="Generator" content="Drupal 10" />
```

**Confidence Scoring**:
- **High (90-100%)**: Multiple patterns + meta generator + cookies
- **Medium (70-89%)**: 2-3 patterns + HTML attributes
- **Low (50-69%)**: Single pattern match

### Other CMS Platforms

#### WordPress
```
Patterns:
  - /wp-content/              # Content directory
  - /wp-includes/             # Core includes
  - /wp-json/                 # REST API
  - /wp-admin/                # Admin panel
  - /xmlrpc.php               # XML-RPC endpoint

Cookies:
  - wordpress_*               # Session cookies
  - wp-settings-*             # User settings

Headers:
  - Link: <...wp-json...>     # REST API discovery

Version Detection:
  - Pattern: /wp-includes/js/jquery/jquery.js?ver=([\d.]+)
```

#### Joomla
```
Patterns:
  - /administrator/           # Admin interface
  - /components/              # Components directory
  - /modules/                 # Modules directory
  - /templates/               # Template directory
  - option=com_               # Component parameter

Meta:
  - <meta name="generator" content="Joomla!" />

JavaScript:
  - /media/jui/js/
  - Joomla.JText
```

#### Magento
```
Patterns:
  - /skin/frontend/           # Frontend skins
  - /js/mage/                 # Magento JavaScript
  - /catalogsearch/           # Catalog search
  - Mage.Cookies              # JavaScript object

Cookies:
  - frontend                  # Session cookie

Headers:
  - X-Magento-*              # Magento-specific headers
```

#### Shopify
```
Patterns:
  - cdn.shopify.com           # CDN resources
  - myshopify.com             # Platform domain
  - /cart/add                 # Cart API
  - Shopify.theme             # JavaScript object

Cookies:
  - _shopify_*                # Session cookies

Headers:
  - X-ShopId                  # Shop identifier
```

#### TYPO3
```
Patterns:
  - /typo3/                   # Backend directory
  - /typo3conf/               # Configuration directory
  - /fileadmin/               # File storage
  - TYPO3.                    # JavaScript namespace

Meta:
  - <meta name="generator" content="TYPO3" />
```

#### Concrete5
```
Patterns:
  - /concrete/                # Core directory
  - /application/             # Application directory
  - ccm_                      # CSS/JavaScript prefix
  - CCM_IMAGE_PATH            # JavaScript constant
```

#### Ghost
```
Patterns:
  - ghost-                    # CSS/JavaScript prefix
  - /ghost/api/               # Admin API

Headers:
  - X-Ghost-*                 # Ghost-specific headers

Meta:
  - <meta name="generator" content="Ghost" />
```

#### Wix, Squarespace, Webflow (Hosted Platforms)
```
Wix:
  - static.wixstatic.com
  - wix.com domain references
  - _wix_browser_sess cookie

Squarespace:
  - static.squarespace.com
  - X-ServedBy: squarespace

Webflow:
  - webflow.com references
  - .webflow.io domains
```

### Complete CMS List

1. **Drupal** - Enhanced detection with 15+ patterns
2. **WordPress** - Most comprehensive, wp-content/wp-includes/wp-json
3. **Joomla** - option=com_, administrator directory
4. **Magento** - E-commerce, skin/frontend
5. **Shopify** - Hosted e-commerce, cdn.shopify.com
6. **TYPO3** - Enterprise CMS, typo3conf
7. **Concrete5** - ccm_ prefix
8. **ModX** - Modular CMS
9. **Wix** - Website builder
10. **Squarespace** - Hosted platform
11. **Ghost** - Modern publishing platform
12. **Hugo** - Static site generator
13. **Jekyll** - Static site generator
14. **Webflow** - Visual web design platform
15. **PrestaShop** - E-commerce CMS
16. **OpenCart** - E-commerce platform

---

## Cloud Provider Detection

Rankle detects **14+ cloud providers** using multiple methods.

### Detection Methods

1. **ASN Matching**: Autonomous System Number lookup
2. **IP Range Analysis**: Check against known CIDR blocks
3. **Reverse DNS (rDNS)**: Hostname pattern matching
4. **ISP/Organization Name**: WHOIS data analysis

### Confidence Levels

- **High (90-100%)**: ASN match + rDNS pattern + IP range
- **Medium (70-89%)**: ASN match + IP range OR rDNS pattern
- **Low (50-69%)**: Single indicator (ISP name or IP range only)

### Supported Cloud Providers

#### AWS (Amazon Web Services)
```
ASN: AS16509, AS14618, AS8987
IP Ranges: 3.0.0.0/8, 13.0.0.0/8, 18.0.0.0/8, 52.0.0.0/8, 54.0.0.0/8
rDNS Patterns:
  - \.amazonaws\.com$
  - \.aws\.amazon\.com$
  - ec2.*\.compute

Example: ec2-54-123-45-67.compute-1.amazonaws.com
```

#### Microsoft Azure
```
ASN: AS8075, AS8068
IP Ranges: 13.64.0.0/11, 20.0.0.0/8, 40.64.0.0/10, 52.96.0.0/12
rDNS Patterns:
  - \.azure\.com$
  - \.cloudapp\.net$
  - \.windows\.net$
  - \.microsoft\.com$

Example: myapp.eastus.cloudapp.azure.com
```

#### Google Cloud Platform (GCP)
```
ASN: AS15169, AS19527, AS396982
IP Ranges: 34.64.0.0/10, 35.184.0.0/13, 35.192.0.0/11, 104.154.0.0/15
rDNS Patterns:
  - \.googleusercontent\.com$
  - \.google\.com$
  - \.1e100\.net$

Example: 123.45.67.89.bc.googleusercontent.com
```

#### DigitalOcean
```
ASN: AS14061
IP Ranges: 104.131.0.0/16, 134.122.0.0/15, 137.184.0.0/14, 159.65.0.0/16
rDNS Patterns:
  - \.digitalocean\.com$

Example: droplet-123.digitalocean.com
```

#### OVH
```
ASN: AS16276
IP Ranges: 5.39.0.0/17, 5.135.0.0/16, 51.38.0.0/15, 54.36.0.0/14
rDNS Patterns:
  - \.ovh\.
  - \.kimsufi\.
  - \.soyoustart\.

Example: vps-123456.vps.ovh.net
```

#### Hetzner
```
ASN: AS24940
IP Ranges: 5.9.0.0/16, 78.46.0.0/15, 88.198.0.0/16, 95.216.0.0/15
rDNS Patterns:
  - \.hetzner\.
  - \.your-server\.de$

Example: static.123-45-67-89.clients.your-server.de
```

#### Linode (Akamai)
```
ASN: AS63949
IP Ranges: 45.33.0.0/17, 139.144.0.0/15, 172.104.0.0/15
rDNS Patterns:
  - \.linode\.com$
  - \.linodeobjects\.com$

Example: li123-45.members.linode.com
```

#### Vultr
```
ASN: AS20473
IP Ranges: 45.32.0.0/15, 45.76.0.0/15, 108.61.0.0/16, 149.28.0.0/16
rDNS Patterns:
  - \.vultr\.com$
  - \.vultrusercontent\.com$
```

#### Cloudflare (Workers/Pages)
```
ASN: AS13335
IP Ranges: 104.16.0.0/13, 104.24.0.0/14, 172.64.0.0/13
rDNS Patterns:
  - \.cloudflare\.com$
  - \.cloudflare\.net$
```

#### Akamai
```
ASN: AS20940, AS16625
IP Ranges: 23.0.0.0/12, 104.64.0.0/10, 184.24.0.0/13
rDNS Patterns:
  - \.akamai\.com$
  - \.akamaiedge\.net$
  - \.akamaitechnologies\.com$
```

### Additional Providers

11. **Alibaba Cloud** - AS45102, AS37963
12. **Oracle Cloud** - AS31898, AS792
13. **IBM Cloud/Softlayer** - AS36351
14. **Scaleway** - AS12876

---

## CDN Detection

Rankle detects **20+ CDN providers** using multi-factor analysis.

### Detection Methods

1. **HTTP Headers**: CDN-specific response headers
2. **DNS CNAME Records**: CDN delegation patterns
3. **Nameserver Analysis**: CDN-managed DNS
4. **IP Range Matching**: Known CDN network blocks
5. **ASN Identification**: CDN autonomous system numbers
6. **TLS Certificate Analysis**: CDN SSL providers

### CDN Signatures

#### Akamai
```
Headers:
  - Server-Timing: ak_p, akamai
  - X-Akamai-*: (any Akamai header)
  - Akamai-Origin-Hop: (hop count)
  - X-Cache: TCP.*from.*akamai

CNAME Patterns:
  - *.akamai.net
  - *.akamaiedge.net
  - *.edgekey.net
  - *.edgesuite.net

Nameservers:
  - akam.net
  - akamai.com

ASN: AS20940, AS16625
IP Ranges: 23.32.0.0/11, 104.64.0.0/10, 184.24.0.0/13
```

#### Cloudflare
```
Headers:
  - CF-Ray: (unique request ID)
  - CF-Cache-Status: HIT/MISS/EXPIRED
  - Server: cloudflare
  - CF-Request-ID: (request identifier)

CNAME Patterns:
  - *.cdn.cloudflare.net
  - *.cloudflare.com

Nameservers:
  - *.ns.cloudflare.com

ASN: AS13335
IP Ranges: 104.16.0.0/13, 172.64.0.0/13, 162.158.0.0/15
```

#### Fastly
```
Headers:
  - X-Served-By: cache-*
  - X-Cache: HIT/MISS
  - X-Cache-Hits: (cache hit count)
  - X-Fastly-Request-ID: (request ID)
  - Fastly-Debug-Digest: (debug info)
  - Via: varnish

CNAME Patterns:
  - *.fastly.net
  - *.fastlylb.net

ASN: AS54113
IP Ranges: 151.101.0.0/16, 199.232.0.0/16
```

#### AWS CloudFront
```
Headers:
  - X-Amz-Cf-Id: (CloudFront ID)
  - X-Amz-Cf-Pop: (edge location)
  - X-Cache: CloudFront
  - Via: CloudFront
  - Server: CloudFront

CNAME Patterns:
  - *.cloudfront.net

ASN: AS16509 (AWS)
```

#### Azure CDN
```
Headers:
  - X-Azure-Ref: (reference ID)
  - X-MS-Ref: (Microsoft reference)
  - X-Cache: TCP_HIT/TCP_MISS
  - X-EC-Custom-Error: (error handling)

CNAME Patterns:
  - *.azureedge.net
  - *.afd.azureedge.net
  - *.trafficmanager.net

ASN: AS8075 (Azure)
```

#### Google Cloud CDN
```
Headers:
  - X-Goog-*: (Google headers)
  - Via: google
  - Server: gws, gse
  - X-Guploader-UploadID: (upload tracking)

CNAME Patterns:
  - *.storage.googleapis.com
  - *.c.storage.googleapis.com

ASN: AS15169, AS396982
```

#### Imperva/Incapsula
```
Headers:
  - X-Iinfo: (Imperva info)
  - X-CDN: Incapsula/Imperva
  - X-Protected-By: Sqreen

CNAME Patterns:
  - *.incapdns.net
  - *.impervadns.net

Cookies:
  - visid_incap_*
  - incap_ses_*

ASN: AS19551
IP Ranges: 45.64.64.0/22, 199.83.128.0/21
```

#### KeyCDN
```
Headers:
  - Server: keycdn
  - X-Cache: HIT/MISS
  - X-Shield: (shield info)

CNAME Patterns:
  - *.kxcdn.com
```

#### BunnyCDN
```
Headers:
  - Server: BunnyCDN
  - CDN-PullZone: (zone ID)
  - CDN-UID: (unique ID)
  - CDN-RequestID: (request tracking)

CNAME Patterns:
  - *.b-cdn.net
```

#### Netlify
```
Headers:
  - Server: Netlify
  - X-NF-Request-ID: (request ID)

CNAME Patterns:
  - *.netlify.app
  - *.netlify.com

Nameservers:
  - dns*.p*.nsone.net
```

#### Vercel
```
Headers:
  - Server: Vercel
  - X-Vercel-ID: (deployment ID)
  - X-Vercel-Cache: HIT/MISS

CNAME Patterns:
  - *.vercel.app
  - cname.vercel-dns.com

IP Ranges: 76.76.21.0/24
```

### Complete CDN List

1. Akamai
2. Cloudflare
3. Fastly
4. AWS CloudFront
5. Azure CDN
6. Google Cloud CDN
7. Imperva/Incapsula
8. Sucuri
9. KeyCDN
10. StackPath/MaxCDN
11. Limelight
12. CDNetworks
13. Edgecast/Verizon
14. ArvanCloud
15. BunnyCDN
16. Netlify
17. Vercel
18. CDN77
19. jsDelivr
20. Varnish (Cache)

---

## WAF Detection

Rankle detects **20+ Web Application Firewalls** using passive analysis.

### Detection Methods

1. **HTTP Headers**: WAF-specific response headers
2. **Cookie Analysis**: WAF session/tracking cookies
3. **Response Body Patterns**: Error page signatures
4. **Challenge Detection**: Bot detection mechanisms

### WAF Signatures

#### Cloudflare WAF
```
Headers:
  - CF-Ray: (request ID)
  - CF-Chl-Bypass: (challenge bypass)
  - Server: cloudflare

Cookies:
  - __cfruid
  - cf_clearance
  - __cf_bm

Body Patterns:
  - "Attention Required! | Cloudflare"
  - "cloudflare.com/cdn-cgi/"
  - "Ray ID:"
  - "cf-error-details"
```

#### AWS WAF
```
Headers:
  - X-Amzn-WAF-*
  - X-Amzn-RequestId

Cookies:
  - awswaf
  - aws-waf-token

Body Patterns:
  - "Request blocked"
  - "awswaf"
```

#### Akamai Kona
```
Headers:
  - Server: AkamaiGHost
  - X-Akamai-*
  - Akamai-Origin-Hop

Cookies:
  - ak_bmsc (Bot Manager)
  - bm_sv, bm_sz
  - _abck (Anti-Bot Challenge Key)

Body Patterns:
  - "Access Denied"
  - "Reference #[0-9a-f.]+"
  - "AkamaiGHost"
```

#### Imperva/Incapsula
```
Headers:
  - X-Iinfo
  - X-CDN: Incapsula/Imperva

Cookies:
  - visid_incap_*
  - incap_ses_*
  - nlbi_*
  - reese84

Body Patterns:
  - "incapsula"
  - "/_Incapsula_Resource"
  - "Request unsuccessful"
```

#### Sucuri CloudProxy
```
Headers:
  - X-Sucuri-ID
  - X-Sucuri-Cache
  - Server: Sucuri

Cookies:
  - sucuri_cloudproxy_uuid

Body Patterns:
  - "Access Denied - Sucuri"
  - "Sucuri WebSite Firewall"
```

#### ModSecurity
```
Headers:
  - Server: ModSecurity, NOYB

Body Patterns:
  - "ModSecurity"
  - "mod_security"
  - "This error was generated by Mod_Security"
  - "NOYB"
```

#### F5 BIG-IP ASM
```
Headers:
  - X-WA-Info
  - X-Cnection: close (typo is intentional)
  - Server: BigIP, BIG-IP

Cookies:
  - TS (transaction ID)
  - BIGipServer*
  - F5_ST, F5_HT_shrinked

Body Patterns:
  - "The requested URL was rejected"
  - "BIG-IP"
  - "F5 Networks"
```

#### Fortinet FortiWeb
```
Headers:
  - Server: FortiWeb

Cookies:
  - FORTIWAFSID

Body Patterns:
  - "FortiWeb"
  - ".fgd_icon"
  - "Server unavailable"
```

#### PerimeterX
```
Cookies:
  - _px, _pxvid, _pxhd

Body Patterns:
  - "PerimeterX"
  - "blocked.*perimeterx"
  - "www.perimeterx.com/whywasiblocked"
```

#### DataDome
```
Headers:
  - X-DataDome

Cookies:
  - datadome
  - datadome-_zldp

Body Patterns:
  - "DataDome"
  - "datadome.co"
```

#### Wordfence (WordPress)
```
Cookies:
  - wfwaf-authcookie

Body Patterns:
  - "Generated by Wordfence"
  - "This response was generated by Wordfence"
```

### Complete WAF List

1. Cloudflare WAF
2. AWS WAF
3. Akamai Kona
4. Imperva/Incapsula
5. Sucuri CloudProxy
6. ModSecurity
7. F5 BIG-IP ASM
8. Fortinet FortiWeb
9. Barracuda
10. Citrix NetScaler
11. DenyAll
12. Palo Alto Next-Gen Firewall
13. Wallarm
14. Reblaze
15. PerimeterX
16. DataDome
17. Shape Security
18. StackPath WAF
19. Wordfence (WordPress)
20. Comodo WAF

---

## JavaScript Library Detection

Rankle detects **15+ JavaScript libraries and frameworks**.

### Detection Techniques

1. **Script Source Analysis**: CDN URLs and file names
2. **Global Object Detection**: `window.jQuery`, `window.React`
3. **HTML Patterns**: Framework-specific markup
4. **Version Extraction**: Regex patterns in source URLs

### Popular Libraries

#### jQuery
```
Patterns:
  - jquery.js, jquery.min.js
  - jquery-[0-9.]+.js
  - /jquery/

Global: window.jQuery, window.$
Version: jquery-([0-9.]+).min.js
```

#### Bootstrap
```
Patterns:
  - bootstrap.css, bootstrap.min.css
  - bootstrap.js, bootstrap.min.js
  - bootstrap/[0-9.]+/

Classes: .container, .row, .col-*
Version: bootstrap@([0-9.]+)
```

#### React
```
Patterns:
  - react.js, react.min.js
  - react-dom.js
  - /_next/ (Next.js)

Global: window.React
Attributes: data-reactroot, data-reactid
```

#### Vue.js
```
Patterns:
  - vue.js, vue.min.js
  - vue@[0-9.]+

Global: window.Vue
Attributes: v-if, v-for, v-bind, v-model
```

#### Angular
```
Patterns:
  - angular.js, angular.min.js
  - @angular/

Global: window.angular
Attributes: ng-*, [ng*, *ngIf, *ngFor
```

#### D3.js
```
Patterns:
  - d3.js, d3.min.js
  - d3-[0-9.]+.js

Global: window.d3
Version: d3[.-]([0-9.]+)
```

### Complete Library List

1. jQuery
2. Bootstrap
3. React (+ Next.js, Gatsby)
4. Vue.js (+ Nuxt.js)
5. Angular (+ AngularJS)
6. D3.js
7. Three.js
8. Chart.js
9. Axios
10. Lodash
11. Moment.js
12. Swiper
13. Slick Carousel
14. AOS (Animate On Scroll)
15. GSAP (GreenSock Animation)
16. Modernizr
17. Popper.js

---

## Advanced Technology Detection

Rankle detects **50+ web technologies** across multiple categories.

### Technology Categories

#### Web Frameworks
- Django (Python)
- Laravel (PHP)
- Ruby on Rails
- Express.js (Node.js)
- Flask (Python)
- FastAPI (Python)
- ASP.NET (.NET)
- Spring (Java)
- Svelte
- Next.js
- Nuxt.js
- Gatsby

#### CSS Frameworks
- Tailwind CSS
- Bootstrap
- Foundation
- Bulma
- Semantic UI
- Material UI
- Chakra UI
- Ant Design

#### E-commerce Platforms
- WooCommerce
- PrestaShop
- Magento
- Shopify
- OpenCart

#### Analytics & Tracking
- Google Analytics
- Google Tag Manager
- Hotjar
- Segment
- Mixpanel

#### Customer Support
- Intercom
- Zendesk
- Drift
- Crisp

#### Marketing Tools
- Mailchimp
- HubSpot

#### Security & Bot Detection
- reCAPTCHA
- hCaptcha
- Cloudflare Turnstile

#### Caching Solutions
- Varnish
- Redis

#### Web Servers
- Nginx
- Apache
- IIS
- LiteSpeed
- OpenResty

#### Proxies & Load Balancers
- Envoy
- Traefik
- HAProxy
- Varnish

#### Error Tracking & APM
- Sentry
- New Relic
- Datadog

#### Payment Gateways
- Stripe
- PayPal
- Braintree

### Confidence Scoring System

Rankle uses weighted confidence scoring (0-100%):

```python
Confidence Calculation:
  - Header Match: 40-70% weight
  - Cookie Match: 30-50% weight
  - HTML Pattern: 30-40% weight
  - Meta Tag: 40-50% weight
  - JS Global: 40-60% weight

Multiple evidence types increase confidence with diminishing returns.
```

**Example Output**:
```json
{
  "detected": true,
  "technologies": [
    {
      "name": "Nginx",
      "category": "Web Server",
      "confidence": 0.80,
      "version": "1.21.6",
      "evidence": [
        {"type": "header", "detail": "Server: nginx/1.21.6", "weight": 0.8}
      ]
    },
    {
      "name": "React",
      "category": "JavaScript Framework",
      "confidence": 0.65,
      "version": null,
      "evidence": [
        {"type": "html_pattern", "detail": "Pattern: data-reactroot", "weight": 0.4},
        {"type": "js_global", "detail": "JS Global: React", "weight": 0.6}
      ]
    }
  ],
  "categories": {
    "Web Server": [
      {"name": "Nginx", "confidence": 0.80, "version": "1.21.6"}
    ],
    "JavaScript Framework": [
      {"name": "React", "confidence": 0.65, "version": null}
    ]
  }
}
```

---

## Enhanced Detection v2.0

**Status:** ⭐ **NEW in v2.0** - Massive detection capability upgrade
**Coverage:** 3000+ technologies via Wappalyzer integration + 7 new detection modules

Rankle v2.0 introduces enhanced technology detection capabilities, expanding from ~50 technologies to **3000+ technologies** with advanced fingerprinting techniques.

### What's New in v2.0?

**Detection Expansion:**
- **3000+ Technology Signatures** via Wappalyzer database integration
- **Favicon Hashing** (mmh3) for infrastructure fingerprinting
- **Error Page Analysis** for framework identification
- **JavaScript Code Analysis** for endpoint extraction and framework detection
- **WordPress Deep Scanning** for plugin/theme enumeration
- **Asset Version Extraction** from filenames
- **CVE Vulnerability Mapping** with search URLs

**Performance:**
- Traditional detection: ~2-3 seconds
- Enhanced detection: ~5-8 seconds (2-3x slower but 10x more comprehensive)

### 1. Wappalyzer Integration (3000+ Technologies)

**Implementation:** `python-Wappalyzer>=0.3.1`

The Wappalyzer database provides signatures for 3000+ technologies across categories:

**Technology Categories:**
- Web frameworks (Django, Laravel, Rails, Flask, FastAPI, Spring Boot)
- JavaScript frameworks (React, Vue, Angular, Next.js, Nuxt.js, Svelte)
- CMS platforms (WordPress, Drupal, Joomla, Shopify, Magento)
- E-commerce (WooCommerce, PrestaShop, OpenCart, Shopify)
- Analytics (Google Analytics, Matomo, Hotjar, Mixpanel)
- CDN/hosting (Cloudflare, Fastly, Netlify, Vercel, AWS CloudFront)
- Marketing tools (HubSpot, Mailchimp, Intercom, Drift)
- Payment processors (Stripe, PayPal, Square, Braintree)
- Server software (Apache, Nginx, IIS, LiteSpeed)
- Databases (MySQL, PostgreSQL, MongoDB, Redis)
- And 2000+ more...

**Usage Example:**
```python
from rankle.detectors.technology import TechnologyDetector

detector = TechnologyDetector("example.com")
results = detector.detect_enhanced(
    headers=headers,
    cookies=cookies,
    body=html,
    base_url="https://example.com"
)

# Results include:
print(f"Detected: {len(results['technologies'])} technologies")
for tech in results['technologies']:
    print(f"  - {tech['name']} ({tech['confidence']*100}%)")
```

**Detection Methods:**
- HTML pattern matching (meta tags, scripts, comments)
- HTTP header analysis (X-Powered-By, Server, custom headers)
- Cookie patterns (framework-specific session cookies)
- JavaScript global variable detection (window objects)
- DOM analysis (specific CSS classes, data attributes)

**Output Format:**
```json
{
  "name": "Django",
  "category": "Web Framework",
  "confidence": 0.9,
  "version": "4.2",
  "evidence": [
    {"type": "header", "detail": "X-Frame-Options: SAMEORIGIN", "weight": 0.3},
    {"type": "cookie", "detail": "csrftoken", "weight": 0.4},
    {"type": "html_pattern", "detail": "csrfmiddlewaretoken", "weight": 0.2}
  ]
}
```

### 2. Favicon Hashing (mmh3)

**Implementation:** `rankle/utils/favicon_hash.py`

Calculates MurmurHash3 (mmh3) hash of favicon.ico to fingerprint infrastructure.

**Why Favicon Hashing?**
- Survives CDN/proxy obfuscation
- Unique per technology/platform
- Passive and undetectable
- Works even when other methods fail

**Known Favicon Hashes:**
```python
KNOWN_FAVICONS = {
    "116323821": "Atlassian Jira",
    "-235701012": "Atlassian Confluence",
    "-1506567754": "GitLab",
    "81586312": "Plex Media Server",
    "999357577": "Grafana",
    "1485257654": "Jenkins",
    "-305179312": "WordPress",
    "1733285952": "pfSense",
    "-1541626999": "Fortinet",
    # ... 25+ more
}
```

**Usage:**
```python
from rankle.utils.favicon_hash import analyze_favicon

result = analyze_favicon("example.com", "https://example.com")

if result['matched']:
    print(f"Identified: {result['technology']} (hash: {result['hash']})")
else:
    print(f"Unknown favicon hash: {result['hash']}")
```

**Example Output:**
```
Hash: 116323821
Match: Atlassian Jira
Confidence: 95%
Evidence: Exact favicon hash match
```

### 3. Error Page Fingerprinting

**Implementation:** `rankle/utils/error_fingerprint.py`

Analyzes 404 and error pages to identify web frameworks by their error page signatures.

**Supported Frameworks:**
- Django (DisallowedHost, CSRF verification failed)
- Laravel (Whoops! error page, Ignition traces)
- Spring Boot (Whitelabel Error Page)
- Rails (Routing Error, AbstractController)
- Express.js (Cannot GET, Express stack traces)
- ASP.NET (Server Error, Stack Trace)
- Flask (Werkzeug Debugger, traceback)
- FastAPI (Swagger UI /docs, validation errors)
- Phoenix (Elixir stack traces)
- Symfony (Symfony Exception, profiler)

**Detection Method:**
```python
from rankle.utils.error_fingerprint import fingerprint_error_page

# Triggers 404 to analyze error response
results = fingerprint_error_page("example.com")

for framework in results:
    print(f"{framework['framework']}: {framework['confidence']*100}%")
    print(f"  Evidence: {framework['patterns_matched']}")
```

**Example Django Detection:**
```
Framework: Django
Confidence: 95%
Patterns Matched:
  - "DisallowedHost at /"
  - "DEBUG = True"
  - "Request Method: GET"
  - "Django version: 4.2"
```

**Ethical Note:** Only triggers single 404 request with unique UUID path, fully passive.

### 4. JavaScript Analysis & Endpoint Extraction

**Implementation:** `rankle/utils/js_extractor.py`

Extracts and analyzes JavaScript files using LinkFinder-style patterns.

**Capabilities:**
1. **Extract JS file URLs** from HTML
2. **Discover API endpoints** using regex patterns
3. **Detect frameworks** from JS code patterns
4. **Extract asset versions** from filenames

**API Endpoint Extraction:**
```python
from rankle.utils.js_extractor import analyze_javascript

results = analyze_javascript("https://example.com", html_content)

print(f"Discovered {len(results['endpoints'])} API endpoints:")
for endpoint in results['endpoints']:
    print(f"  - {endpoint}")
```

**Regex Patterns Used:**
```python
patterns = [
    r'["\']((https?:)?//[^"\']+)["\']',              # Full URLs
    r'["\']([/][^"\']*)["\']',                        # Absolute paths
    r'["\'](\.\./[^"\']+)["\']',                      # Relative paths
    r'["\']([a-zA-Z0-9_\-/]+\.(?:php|asp|aspx|jsp|json|xml|do|action))["\']',  # API extensions
]
```

**Framework Detection from JS:**
- **React:** `React.createElement`, `ReactDOM.render`
- **Vue.js:** `Vue.config`, `new Vue(`
- **Angular:** `ng-`, `angular.module`
- **Next.js:** `__NEXT_DATA__`, `_next/static/`
- **Nuxt.js:** `__NUXT__`, `_nuxt/`
- **jQuery:** `jQuery`, `$(`

**Example Output:**
```json
{
  "js_files": 3,
  "frameworks_detected": ["React", "Next.js"],
  "endpoints": [
    "/api/users",
    "/api/products",
    "/graphql"
  ],
  "versions": {
    "react": "18.2.0"
  }
}
```

### 5. WordPress Plugin & Theme Detection

**Implementation:** `rankle/utils/wordpress_plugins.py`

Passive WordPress plugin and theme enumeration via HTML parsing.

**Detection Method:**
- Parse HTML for `/wp-content/plugins/{slug}/` paths
- Parse HTML for `/wp-content/themes/{slug}/` paths
- Map slugs to friendly names using 60+ plugin database
- Map slugs to friendly names using 20+ theme database

**Known Plugins:**
```python
KNOWN_PLUGINS = {
    "contact-form-7": "Contact Form 7",
    "woocommerce": "WooCommerce",
    "yoast-seo": "Yoast SEO",
    "elementor": "Elementor Page Builder",
    "wordfence": "Wordfence Security",
    "akismet": "Akismet Anti-Spam",
    # ... 60+ plugins
}
```

**Usage:**
```python
from rankle.utils.wordpress_plugins import analyze_wordpress

results = analyze_wordpress(html_content, "https://example.com")

if results['is_wordpress']:
    print(f"WordPress Detected")
    print(f"Plugins: {results['plugin_count']}")
    for plugin in results['plugins']:
        print(f"  - {plugin['name']}")
    print(f"Themes: {results['theme_count']}")
    for theme in results['themes']:
        print(f"  - {theme['name']}")
```

**Example Output:**
```
WordPress: Yes
Version: 6.4.2
Plugins (5):
  - Contact Form 7
  - Yoast SEO
  - WooCommerce
  - Elementor Page Builder
  - Wordfence Security
Active Theme: Astra
```

### 6. Asset Version Extraction

**Implementation:** Built into `js_extractor.py`

Extracts version numbers from asset filenames using regex patterns.

**Patterns:**
```python
# Common versioning patterns:
jquery-3.6.0.min.js       → jQuery 3.6.0
react.production.18.2.0.js → React 18.2.0
bootstrap@5.3.0.min.css    → Bootstrap 5.3.0
vue-2.7.14.js             → Vue.js 2.7.14
```

**Usage:**
```python
from rankle.utils.js_extractor import extract_version_from_assets

versions = extract_version_from_assets(html_content)

for tech, version in versions.items():
    print(f"{tech}: {version}")
```

### 7. CVE Vulnerability Mapping

**Implementation:** `rankle/utils/cve_mapper.py`

Generates CPE identifiers and CVE search URLs for detected technologies.

**CPE 2.3 Format:**
```
cpe:2.3:a:vendor:product:version:*:*:*:*:*:*:*
```

**Generated Search URLs:**
- **NVD (NIST):** https://nvd.nist.gov/vuln/search/results?query=...
- **CVE MITRE:** https://cve.mitre.org/cgi-bin/cvekey.cgi?keyword=...
- **CVEDetails:** https://www.cvedetails.com/google-search-results.php?q=...
- **Vulners:** https://vulners.com/search?query=...
- **Exploit-DB:** https://www.exploit-db.com/search?q=...

**Usage:**
```python
from rankle.utils.cve_mapper import map_technology_to_cve_urls

cve_info = map_technology_to_cve_urls("Django", "4.2")

print(f"Technology: {cve_info['technology']}")
print(f"CPE: {cve_info['cpe']}")
print("CVE Search URLs:")
for source, url in cve_info['cve_search_urls'].items():
    print(f"  - {source}: {url}")
```

**Example Output:**
```
Technology: Django 4.2
CPE: cpe:2.3:a:djangoproject:django:4.2:*:*:*:*:*:*:*
CVE Search URLs:
  - nist_nvd: https://nvd.nist.gov/vuln/search/results?form_type=Advanced&query=Django%204.2
  - cve_mitre: https://cve.mitre.org/cgi-bin/cvekey.cgi?keyword=Django%204.2
  - cvedetails: https://www.cvedetails.com/version/573214/Djangoproject-Django-4.2.html
  - vulners: https://vulners.com/search?query=Django%204.2
  - exploit_db: https://www.exploit-db.com/search?q=Django%204.2

Recommendation: Review CVE databases for known vulnerabilities in Django 4.2
```

### Using Enhanced Detection

**Standard Detection (Traditional):**
```bash
python main.py example.com
```

**Enhanced Detection (v2.0):**
```python
# Use the demo script
python scripts/demo_enhanced_detection.py example.com

# Output includes:
# - 3000+ technology signatures checked
# - Favicon hash analysis
# - Error page fingerprinting
# - JavaScript endpoints extracted
# - WordPress plugins/themes (if applicable)
# - CVE search URLs for all detected technologies
```

**API Usage:**
```python
from rankle.detectors.technology import TechnologyDetector

detector = TechnologyDetector("example.com")

# Traditional detection
basic_results = detector.detect(headers, cookies, body)

# Enhanced detection (v2.0)
enhanced_results = detector.detect_enhanced(
    headers=headers,
    cookies=cookies,
    body=body,
    base_url="https://example.com"
)

# Compare results
print(f"Basic: {len(basic_results['technologies'])} technologies")
print(f"Enhanced: {len(enhanced_results['technologies'])} technologies")
```

### Performance Comparison

**Test Domain: example.com**

| Method | Technologies | Time | Techniques |
|--------|-------------|------|------------|
| Traditional | 6 | ~2s | Headers, cookies, HTML patterns |
| Enhanced v2.0 | 9 | ~6s | + Wappalyzer, favicon, error pages, JS analysis |

**Enhancement:** +50% more technologies detected, +CVE mapping, +evidence tracking

### Complete Example Output

```json
{
  "detected": true,
  "technologies": [
    {
      "name": "Angular",
      "confidence": 0.9,
      "evidence": "js_pattern",
      "category": "JavaScript Framework"
    },
    {
      "name": "jQuery",
      "confidence": 0.85,
      "evidence": "js_pattern",
      "category": "JavaScript Framework"
    },
    {
      "name": "Google Tag Manager",
      "category": "Tag Manager",
      "confidence": 0.7,
      "version": null,
      "evidence": [
        {"type": "html_pattern", "detail": "GTM-", "weight": 0.7}
      ]
    }
  ],
  "api_endpoints": [
    "/api/v1/users",
    "/graphql"
  ],
  "wordpress": {
    "detected": false
  },
  "cve_mappings": [
    {
      "technology": "Angular",
      "version": null,
      "cpe": "cpe:2.3:a:angular:angular:*:*:*:*:*:*:*:*",
      "cve_search_urls": {
        "nist_nvd": "https://nvd.nist.gov/vuln/search/results?query=Angular",
        "cve_mitre": "https://cve.mitre.org/cgi-bin/cvekey.cgi?keyword=Angular"
      }
    }
  ]
}
```

### Documentation

For complete technical details, see:
- **[Technology Detection Enhancement Guide](TECHNOLOGY_DETECTION_ENHANCEMENT.md)** - Full v2.0 documentation
- **[Scripts Documentation](../scripts/README.md)** - `demo_enhanced_detection.py` usage

---

## Origin Infrastructure Discovery

**Purpose**: Discover real infrastructure behind CDN/WAF protection using **100% passive techniques**.

### Ethical Use Only

- All methods are **passive** - no active attacks
- Uses only **public DNS/SSL data**
- For **authorized testing only**
- Complies with responsible disclosure

### Discovery Methods

#### 1. Subdomain Analysis
```
Check non-CDN subdomains:
  - origin.example.com
  - direct.example.com
  - admin.example.com
  - api.example.com
  - staging.example.com
  - dev.example.com
  - mail.example.com
  - ftp.example.com
  - vpn.example.com
  - cpanel.example.com
  - backend.example.com
  - internal.example.com

Rationale:
  Administrative and infrastructure subdomains often bypass CDN/WAF
  because they're not intended for public access.
```

#### 2. MX Record Analysis
```
Mail servers often reveal origin network:

  1. Query MX records: dig MX example.com
  2. Resolve MX hostname to IP
  3. Analyze IP geolocation and ASN
  4. Compare with main website IP

Why it works:
  Email infrastructure is typically on the same network as web servers,
  but MX records can't be proxied through CDN.
```

#### 3. SPF/TXT Record Parsing
```
SPF records authorize sending IPs:

  Example: "v=spf1 ip4:192.0.2.0/24 include:_spf.google.com ~all"

  Extract:
    - ip4: directives → Direct IP ranges
    - include: directives → Third-party services
    - a: directives → Domain A records

Why it works:
  SPF must list real sending IPs, which often include web server IPs.
```

#### 4. SSL Certificate Subject Alternative Names (SANs)
```
TLS certificates list all valid domains:

  1. Connect to HTTPS endpoint
  2. Extract certificate
  3. Parse Subject Alternative Names
  4. Resolve each SAN to IP
  5. Filter out CDN IPs

Why it works:
  Certificates often include internal/direct-access domains in SANs.
```

#### 5. Certificate Transparency Log Mining
```
Query CT logs (crt.sh) for subdomains:

  https://crt.sh/?q=%.example.com&output=json

  1. Fetch all certificate records
  2. Extract unique subdomains
  3. Resolve to IPs
  4. Exclude CDN ranges

Why it works:
  CT logs are public and reveal historical subdomain usage.
```

#### 6. Common Pattern Discovery
```
Test predictable origin domains:
  - origin-www.example.com
  - origin.example.com
  - direct-www.example.com
  - real.example.com
  - server.example.com
  - backend.example.com
```

### Cloud Provider Identification

Once origin IPs are discovered, identify hosting:

```python
Methods:
  1. Reverse DNS lookup
  2. IP range matching (CIDR)
  3. ASN lookup
  4. WHOIS organization field

Confidence Scoring:
  - High: ASN + rDNS + IP range match
  - Medium: ASN + IP range OR rDNS pattern
  - Low: Single indicator
```

### Example Output

```
Origin Infrastructure Discovery
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Detection Methods Used:
  ✓ MX Records
  ✓ SPF Records
  ✓ Subdomain Analysis
  ✓ Certificate Transparency
  ✓ Pattern Discovery

Origin IPs Found: 4
  • 148.163.154.111 → AWS (high confidence)
    Source: subdomain:api.example.com
    rDNS: ec2-148-163-154-111.compute-1.amazonaws.com

  • 148.163.150.174 → AWS (high confidence)
    Source: mx_record:mail.example.com
    rDNS: ec2-148-163-150-174.compute-1.amazonaws.com

  • 198.51.100.42 → DigitalOcean (medium confidence)
    Source: spf_record:ip4:198.51.100.0/24

  • 203.0.113.10 → Unknown
    Source: ct_log:staging.example.com

Direct Access Domains (3 found):
  • api.example.com → 148.163.154.111
  • staging.example.com → 203.0.113.10
  • origin.example.com → 148.163.154.111

Mail Servers:
  • mail.example.com (preference: 10) → 148.163.150.174

SPF Includes:
  • include:_spf.google.com (Google Workspace)
  • ip4:198.51.100.0/24
```

### Use Cases

1. **Penetration Testing** (authorized) - Identify attack surface
2. **Security Research** - Analyze infrastructure patterns
3. **Infrastructure Analysis** - Map hosting architecture
4. **Attack Surface Mapping** - Enumerate all entry points
5. **Competitor Analysis** - Understand hosting choices

---

## Advanced HTTP Fingerprinting

Rankle performs **8 advanced fingerprinting techniques** beyond basic detection.

### 1. HTTP Methods Testing

Tests which HTTP methods are allowed:

```
Methods Tested:
  - GET, POST, PUT, DELETE, PATCH
  - OPTIONS, HEAD, TRACE
  - CONNECT, PROPFIND, MKCOL

Detection:
  1. Send OPTIONS request
  2. Parse Allow header
  3. Fall back to testing each method individually
  4. Check status codes (405 = not allowed)

Security Implications:
  - PUT/DELETE enabled → Potential file upload/deletion
  - TRACE enabled → Cross-Site Tracing (XST) vulnerability
  - PROPFIND/MKCOL → WebDAV exposed
```

**Example Output**:
```
Allowed HTTP Methods: OPTIONS, HEAD, GET, POST, PUT, DELETE, PATCH
⚠️  PUT and DELETE methods enabled (potential security risk)
⚠️  TRACE method enabled (XST vulnerability)
```

### 2. Server Version Extraction

Extracts exact versions from headers:

```
Server Signatures:
  - Server: nginx/1.21.6
  - Server: Apache/2.4.54 (Ubuntu)
  - Server: Microsoft-IIS/10.0
  - X-Powered-By: PHP/8.1.12
  - X-AspNet-Version: 4.0.30319
  - X-Powered-By: Express 4.18.2

Parsing:
  Pattern: ([A-Za-z]+)[/\s]([0-9.]+)
  Groups: 1=Software, 2=Version
```

**Security Implications**:
- Version disclosure enables CVE research
- Outdated versions indicate security risk
- Server fingerprinting for exploit targeting

### 3. API Endpoint Discovery

Probes for common API endpoints:

```
Endpoints Tested (15+):
  REST APIs:
    - /api, /api/v1, /api/v2, /api/v3
    - /v1, /v2, /rest

  GraphQL:
    - /graphql
    - /api/graphql
    - /graphiql (GraphQL IDE)

  Documentation:
    - /swagger, /swagger.json, /swagger.yaml
    - /api-docs, /api/docs
    - /openapi.json, /openapi.yaml
    - /redoc

  Health Checks:
    - /health, /healthz
    - /status, /ping
    - /metrics, /prometheus
    - /actuator (Spring Boot)
    - /actuator/health

  Configuration:
    - /config.json
    - /.well-known/security.txt
    - /.well-known/openid-configuration

  CMS-Specific:
    - /wp-json (WordPress REST API)
    - /api/users
    - /jsonapi (Drupal)

Status Interpretation:
  - 200 OK → Endpoint accessible
  - 401 Unauthorized → Endpoint exists but protected
  - 403 Forbidden → Endpoint exists but forbidden
  - 404 Not Found → Endpoint doesn't exist
  - 405 Method Not Allowed → Endpoint exists, wrong method
```

**Example Output**:
```
Discovered API Endpoints (4):
  • /api/v1 [200] - application/json
  • /graphql [403] - application/json (protected)
  • /health [200] - text/plain
  • /swagger.json [200] - application/json
```

### 4. Exposed Sensitive Files

Checks for **30+ sensitive paths**:

```
Configuration Files:
  - /.env, /.env.local, /.env.production
  - /config.php, /config.json, /config.yml
  - /settings.json
  - /.htaccess, /web.config

Version Control:
  - /.git/config, /.git/HEAD
  - /.gitignore
  - /.svn/entries
  - /.hg/hgrc

Backups & Databases:
  - /backup.sql, /backup.zip
  - /db.sql, /dump.sql
  - /database.sql

Debug/Development:
  - /phpinfo.php, /info.php
  - /debug.log, /error.log
  - /test.php

Admin Panels:
  - /admin, /administrator
  - /wp-admin, /wp-login.php
  - /phpmyadmin, /adminer

Package Managers:
  - /package.json, /composer.json
  - /requirements.txt, /Pipfile
  - /yarn.lock, /package-lock.json

Cloud/Container:
  - /.aws/credentials
  - /.docker/config.json
  - /Dockerfile, /docker-compose.yml
  - /.kube/config
```

**Detection Method**:
```python
1. Send HEAD request (faster than GET)
2. Check status code == 200
3. For sensitive files (.git, .env, .sql):
   - Verify with GET request
   - Ensure response body is not 404 page
4. Report with status code and content type
```

**Example Output**:
```
Exposed Sensitive Files (3):
  ⚠️  /.git/config [200] - text/plain (74 bytes)
  ⚠️  /phpinfo.php [200] - text/html (52,341 bytes)
  ⚠️  /backup.sql [200] - application/octet-stream (1.2 MB)
```

### 5. Cookie Analysis & Technology Identification

Analyzes cookies for technology fingerprinting:

```
Cookie-Based Detection:
  PHP:
    - PHPSESSID

  Java/Tomcat:
    - JSESSIONID

  ASP.NET:
    - ASP.NET_SessionId
    - .ASPXAUTH

  CDN/WAF:
    - __cfduid, cf_clearance (Cloudflare)
    - incap_ses_* (Imperva)
    - ak_bmsc (Akamai)

  Analytics:
    - _ga, _gid (Google Analytics)
    - _fbp (Facebook Pixel)
    - mp_* (Mixpanel)

  CMS:
    - wordpress_*
    - drupal
    - CONCRETE5

  Frameworks:
    - laravel_session
    - connect.sid (Express)

Security Attributes:
  - Secure flag (HTTPS only)
  - HttpOnly flag (JavaScript access)
  - SameSite (CSRF protection)
```

**Example Output**:
```
Cookie Analysis (5 cookies):
  • PHPSESSID
    Technology: PHP
    Secure: Yes, HttpOnly: Yes, SameSite: Lax

  • _ga
    Technology: Google Analytics
    Secure: No, HttpOnly: No
    ⚠️  Missing security flags

  • cf_clearance
    Technology: Cloudflare
    Secure: Yes, HttpOnly: Yes, SameSite: None
```

### 6. Error Page Fingerprinting

Analyzes 404/error pages to identify infrastructure:

```
Test Method:
  1. Request non-existent path: /this-path-should-not-exist-12345
  2. Analyze error page HTML and headers
  3. Match against 10+ error signatures

Web Servers:
  Apache:
    - "Apache/[\d.]+ Server at"
    - apache_pb.gif

  Nginx:
    - "nginx/[\d.]+"
    - "Welcome to nginx"

  IIS:
    - "Microsoft-IIS/[\d.]+"
    - "The page cannot be found"

  LiteSpeed:
    - "LiteSpeed Web Server"

Frameworks:
  Django:
    - "DisallowedHost"
    - "CSRF verification failed"
    - "Django version X.Y.Z"

  Laravel:
    - "Whoops! There was an error"
    - "Laravel"

  Spring Boot:
    - "Whitelabel Error Page"
    - {"timestamp":..., "status":404, "error":"Not Found"}

  Express:
    - "Cannot GET /path"
    - "Cannot POST /path"
```

### 7. Technology-Specific Headers

Detects headers that reveal infrastructure:

```
Framework Headers:
  - X-AspNet-Version: 4.0.30319 (ASP.NET)
  - X-Drupal-Cache: HIT (Drupal)
  - X-Runtime: 0.123456 (Rails)
  - X-Powered-By: Express (Node.js)

Caching Headers:
  - X-Varnish: 12345 67890 (Varnish)
  - X-Nginx-Cache-Status: HIT
  - CF-Cache-Status: HIT (Cloudflare)

Cloud Provider Headers:
  - X-Amz-Cf-Id (AWS CloudFront)
  - X-Azure-Ref (Azure)
  - X-Goog-* (Google Cloud)

CDN/Proxy Headers:
  - Via: 1.1 varnish
  - X-Served-By: cache-*
  - X-Cache: HIT/MISS

Security Headers:
  - Strict-Transport-Security (HSTS)
  - Content-Security-Policy (CSP)
  - X-Frame-Options (Clickjacking protection)
  - X-Content-Type-Options (MIME sniffing)
```

### 8. Response Time Analysis

Measures server response time:

```
Metrics Collected:
  - DNS resolution time
  - TCP connection time
  - TLS handshake time
  - Time to first byte (TTFB)
  - Total response time

Analysis:
  <50ms:   Excellent (likely cached or nearby)
  50-200ms: Good (typical CDN response)
  200-500ms: Average (distant server or moderate load)
  >500ms:   Slow (high latency or server load)

Indicators:
  - Very fast (<20ms) → CDN/cache hit
  - Consistent times → Cached content
  - Variable times → Dynamic content or load balancing
  - High latency → Geographic distance or server load
```

**Example Comprehensive Output**:

```
Advanced HTTP Fingerprinting Results
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Server Information:
  Server: nginx/1.21.6
  HTTP Version: HTTP/1.1
  HTTP/2 Support: Yes

Allowed HTTP Methods:
  OPTIONS, HEAD, GET, POST, PUT, DELETE, PATCH
  ⚠️  PUT/DELETE enabled

Discovered API Endpoints (3):
  • /api/v1 [200] - application/json
  • /graphql [403] - application/json (protected)
  • /health [200] - text/plain

Exposed Files (2):
  ⚠️  /.git/config [200] - text/plain
  ⚠️  /phpinfo.php [200] - text/html

Technology from Cookies (2):
  • PHP (PHPSESSID)
  • Google Analytics (_ga, _gid)

Server Signatures:
  • Nginx
  • PHP

Technology Headers:
  • X-Powered-By: PHP/8.1.12
  • X-Nginx-Cache-Status: HIT

Response Time: 42.3ms (excellent)

Security Headers:
  ✓ Strict-Transport-Security: max-age=31536000
  ✓ X-Content-Type-Options: nosniff
  ✓ X-Frame-Options: SAMEORIGIN
  ✗ Content-Security-Policy: Missing
```

---

## Integration Examples

### Integration with Nuclei

**Nuclei** is a fast vulnerability scanner based on templates.

#### Direct Subdomain Pipe

```bash
# Scan subdomains discovered by Rankle
python main.py example.com --output json | \
  jq -r '.subdomains[]' | \
  nuclei -l - -t nuclei-templates/
```

#### Technology-Based Scanning

```bash
# Detect CMS and scan with specific templates
CMS=$(cat scan.json | jq -r '.technologies_web.cms' | cut -d' ' -f1 | tr '[:upper:]' '[:lower:]')

cat scan.json | jq -r '.subdomains[]' | \
  nuclei -l - -t nuclei-templates/$CMS/
```

#### CVE Scanning

```bash
# Focus on high/critical CVEs
cat scan.json | jq -r '.subdomains[]' | \
  nuclei -l - \
    -t nuclei-templates/cves/ \
    -t nuclei-templates/vulnerabilities/ \
    -severity high,critical
```

#### Complete Nuclei Pipeline Script

**See:** [`docs/examples/nuclei_pipeline.sh`](examples/nuclei_pipeline.sh)

This ready-to-use script:
1. Runs Rankle scan and exports JSON
2. Extracts and deduplicates subdomains
3. Validates live hosts with httpx
4. Scans for high/critical vulnerabilities with Nuclei

**Usage:**
```bash
chmod +x docs/examples/nuclei_pipeline.sh
./docs/examples/nuclei_pipeline.sh example.com
```

**Output:** `recon_output/nuclei_findings.txt`

### Integration with Nmap

**Nmap** is a network scanning tool for port discovery and service detection.

#### Scan Discovered IPs

```bash
# Scan all A records
cat scan.json | jq -r '.dns.A[]' | nmap -iL - -sV -oA nmap_scan

# IPv6 scan
cat scan.json | jq -r '.dns.AAAA[]' | nmap -6 -iL - -sV
```

#### Targeted Port Scanning

```bash
# Scan common web ports with scripts
cat scan.json | jq -r '.dns.A[]' | \
  nmap -iL - \
    -p 80,443,8080,8443 \
    -sV \
    --script=http-enum,http-headers,ssl-cert
```

#### Service Enumeration

```bash
# Full service detection with OS fingerprinting
FIRST_IP=$(cat scan.json | jq -r '.dns.A[0]')
nmap $FIRST_IP -sV -O --script=banner -oA detailed_scan
```

#### Complete Nmap Pipeline Script

**See:** [`docs/examples/nmap_pipeline.sh`](examples/nmap_pipeline.sh)

This ready-to-use script:
1. Runs Rankle scan and exports JSON
2. Extracts all IPv4 addresses from DNS results
3. Performs service detection on common ports (80, 443, 8080, 8443, 22, 21, 3306, 5432)
4. Runs full port scan on first discovered IP

**Usage:**
```bash
chmod +x docs/examples/nmap_pipeline.sh
./docs/examples/nmap_pipeline.sh example.com
```

**Output:** `recon_output/nmap_services.xml` and `recon_output/nmap_full_*.xml`

### Integration with httpx

**httpx** is a fast HTTP toolkit for probing live hosts.

#### Verify Live Subdomains

```bash
# Check which subdomains are actually live
cat scan.json | jq -r '.subdomains[]' | \
  httpx -silent -status-code -title -tech-detect
```

#### Extract Technology Stack

```bash
# Detect web technologies on live hosts
cat scan.json | jq -r '.subdomains[]' | \
  httpx -silent -tech-detect -json -o tech_results.json
```

#### Screenshot All Hosts

```bash
# Take screenshots of all live subdomains
cat scan.json | jq -r '.subdomains[]' | \
  httpx -silent -screenshot -output-folder screenshots/
```

### Integration with jq

**jq** is a JSON processor for parsing Rankle's output.

#### Extract Specific Fields

```bash
# Get all IPs
jq -r '.dns.A[]' scan.json

# Count subdomains
jq '.subdomains | length' scan.json

# Get detected CMS
jq -r '.technologies_web.cms' scan.json

# Extract origin IPs
jq -r '.origin_discovery.potential_origins[].ip' scan.json

# Get CDN name
jq -r '.cdn.name' scan.json

# List all technologies
jq -r '.technologies_web.detected_technologies[].name' scan.json
```

#### Complex Queries

```bash
# Get high-confidence technologies (>70%)
jq '.technologies_web.detected_technologies[] | select(.confidence > 0.7) | .name' scan.json

# Extract subdomains with specific pattern
jq -r '.subdomains[] | select(contains("api"))' scan.json

# Get IPs not in Cloudflare range
jq -r '.dns.A[] | select(. | startswith("104.16.") | not)' scan.json

# List exposed files with status 200
jq '.http_fingerprint.exposed_paths[] | select(.status == 200)' scan.json
```

### Integration with SIEM/SOAR

#### Elasticsearch

```bash
# Index Rankle results into Elasticsearch
curl -X POST "localhost:9200/recon-$(date +%Y.%m)/_doc/" \
  -H 'Content-Type: application/json' \
  -d @scan.json
```

#### Splunk

```bash
# Send to Splunk HTTP Event Collector
curl -X POST "https://splunk:8088/services/collector/event" \
  -H "Authorization: Splunk YOUR-TOKEN" \
  -d '{"event": '"$(cat scan.json)"', "sourcetype": "rankle_scan"}'
```

#### PostgreSQL

```sql
-- Store JSON in PostgreSQL
CREATE TABLE recon_scans (
    id SERIAL PRIMARY KEY,
    domain TEXT NOT NULL,
    scan_time TIMESTAMP DEFAULT NOW(),
    results JSONB NOT NULL
);

-- Insert scan results
INSERT INTO recon_scans (domain, results)
VALUES ('example.com', '{"dns": {...}, "subdomains": [...]}');

-- Query using JSONB operators
SELECT domain, results->'dns'->'A' as ips
FROM recon_scans
WHERE results->'cdn'->>'detected' = 'true';
```

---

## Full Reconnaissance Pipeline

Complete automated reconnaissance workflow combining multiple tools.

### Complete Recon Chain Script

**See:** [`docs/examples/full_recon_chain.sh`](examples/full_recon_chain.sh)

This comprehensive script combines all tools into a single automated workflow:

**Workflow:**
```
[1/5] Rankle reconnaissance
   └─ DNS, subdomains, technologies, CDN/WAF detection

[2/5] Extract and deduplicate subdomains
   └─ Filter wildcards and duplicates

[3/5] Live host detection with httpx
   └─ Verify which hosts are actually live

[4/5] Nuclei vulnerability scan
   └─ Scan for medium/high/critical vulnerabilities

[5/5] Nmap port scan on discovered IPs
   └─ Service detection and port enumeration
```

**Usage:**
```bash
chmod +x docs/examples/full_recon_chain.sh
./docs/examples/full_recon_chain.sh example.com
```

**Output:** Creates a timestamped workspace directory with:
- Rankle JSON and text reports
- Subdomain list (deduplicated)
- Live host verification results
- Nuclei vulnerability findings
- Nmap port scan results
- Automated summary report (`REPORT.txt`)

### Multi-Domain Batch Scan

```bash
#!/bin/bash
# Scan multiple domains from file

DOMAINS_FILE=$1

if [ -z "$DOMAINS_FILE" ]; then
    echo "Usage: $0 <domains.txt>"
    exit 1
fi

BATCH_DIR="batch_recon_$(date +%Y%m%d_%H%M%S)"
mkdir -p $BATCH_DIR

while IFS= read -r domain; do
    echo "[*] Scanning: $domain"

    DOMAIN_DIR="$BATCH_DIR/$domain"
    mkdir -p $DOMAIN_DIR

    # Run Rankle
    docker run --rm -v "$(pwd)/$DOMAIN_DIR:/output" rankle "$domain" --output both

    # Extract subdomains
    JSON="$DOMAIN_DIR/${domain//./_}_rankle.json"
    jq -r '.subdomains[]' $JSON | sort -u > $DOMAIN_DIR/subdomains.txt

    # Check live hosts
    cat $DOMAIN_DIR/subdomains.txt | \
      httpx -silent -o $DOMAIN_DIR/live_hosts.txt

    echo "    Found: $(wc -l < $DOMAIN_DIR/subdomains.txt) subdomains, $(wc -l < $DOMAIN_DIR/live_hosts.txt) live"

done < "$DOMAINS_FILE"

# Generate batch summary
cat > $BATCH_DIR/SUMMARY.txt << SUMMARY
Batch Reconnaissance Summary
Generated: $(date)
============================

Domains Scanned: $(wc -l < $DOMAINS_FILE)

Per-Domain Statistics:
$(for dir in $BATCH_DIR/*/; do
    domain=$(basename $dir)
    subdomains=$(wc -l < $dir/subdomains.txt 2>/dev/null || echo "0")
    live=$(wc -l < $dir/live_hosts.txt 2>/dev/null || echo "0")
    echo "  $domain: $subdomains subdomains, $live live hosts"
done)
SUMMARY

echo ""
echo "Batch scan complete! Results in: $BATCH_DIR/"
echo "Summary: $BATCH_DIR/SUMMARY.txt"
```

### Continuous Monitoring Setup

```bash
#!/bin/bash
# Set up continuous monitoring with cron

DOMAIN=$1
MONITOR_DIR="/var/recon/monitoring"
ALERT_EMAIL="security@example.com"

mkdir -p $MONITOR_DIR/$DOMAIN

# Initial baseline scan
docker run --rm -v "$MONITOR_DIR/$DOMAIN:/output" rankle "$DOMAIN" --output json
cp "$MONITOR_DIR/$DOMAIN/${DOMAIN//./_}_rankle.json" "$MONITOR_DIR/$DOMAIN/baseline.json"

# Create monitoring script
cat > $MONITOR_DIR/$DOMAIN/monitor.sh << 'SCRIPT'
#!/bin/bash
DOMAIN=$1
MONITOR_DIR="/var/recon/monitoring/$DOMAIN"

# Run new scan
docker run --rm -v "$MONITOR_DIR:/output" rankle "$DOMAIN" --output json
NEW_SCAN="$MONITOR_DIR/${DOMAIN//./_}_rankle.json"
BASELINE="$MONITOR_DIR/baseline.json"

# Compare subdomain counts
OLD_COUNT=$(jq '.subdomains | length' $BASELINE)
NEW_COUNT=$(jq '.subdomains | length' $NEW_SCAN)
DIFF=$((NEW_COUNT - OLD_COUNT))

# Check for new subdomains
comm -13 \
  <(jq -r '.subdomains[]' $BASELINE | sort) \
  <(jq -r '.subdomains[]' $NEW_SCAN | sort) \
  > $MONITOR_DIR/new_subdomains.txt

NEW_SUBS=$(wc -l < $MONITOR_DIR/new_subdomains.txt)

# Alert if changes detected
if [ $NEW_SUBS -gt 0 ]; then
    mail -s "Recon Alert: $NEW_SUBS new subdomains for $DOMAIN" "$ALERT_EMAIL" < $MONITOR_DIR/new_subdomains.txt
fi

# Update baseline
cp $NEW_SCAN $BASELINE
SCRIPT

chmod +x $MONITOR_DIR/$DOMAIN/monitor.sh

# Add to crontab (run daily at 2 AM)
(crontab -l 2>/dev/null; echo "0 2 * * * $MONITOR_DIR/$DOMAIN/monitor.sh $DOMAIN") | crontab -

echo "Monitoring configured for $DOMAIN"
echo "Daily scans at 2 AM, alerts to $ALERT_EMAIL"
```

### Output Format Examples

#### JSON Output (Machine-Readable)

```json
{
  "domain": "example.com",
  "scan_time": "2025-01-19T12:00:00Z",
  "dns": {
    "A": ["93.184.216.34"],
    "AAAA": ["2606:2800:220:1:248:1893:25c8:1946"],
    "MX": [
      {"priority": 10, "host": "mail.example.com"}
    ],
    "NS": ["ns1.example.com", "ns2.example.com"],
    "TXT": ["v=spf1 include:_spf.example.com ~all"]
  },
  "subdomains": [
    "www.example.com",
    "api.example.com",
    "staging.example.com"
  ],
  "cdn": {
    "detected": true,
    "name": "Cloudflare",
    "confidence": 0.95,
    "evidence": [
      {"type": "header", "detail": "CF-Ray: 123456789"}
    ]
  },
  "waf": {
    "detected": true,
    "name": "Cloudflare WAF",
    "confidence": 0.90
  },
  "technologies_web": {
    "cms": "Drupal 10",
    "detected_technologies": [
      {
        "name": "Nginx",
        "category": "Web Server",
        "confidence": 0.80,
        "version": "1.21.6"
      },
      {
        "name": "Drupal",
        "category": "CMS",
        "confidence": 0.95,
        "version": "10.0.0"
      }
    ]
  },
  "origin_discovery": {
    "potential_origins": [
      {
        "ip": "198.51.100.42",
        "source": "subdomain:api.example.com",
        "cloud_provider": "AWS",
        "confidence": 0.7
      }
    ]
  }
}
```

#### Text Output (Human-Readable)

```
DOMAIN: example.com
SCAN_TIME: 2025-01-19 12:00:00
STATUS: 200
════════════════════════════════════════════════════════════════

[INFRASTRUCTURE]
  IPv4 Addresses: 93.184.216.34
  IPv6 Addresses: 2606:2800:220:1:248:1893:25c8:1946
  Location: United States (US)
  ISP: Example Hosting, Inc.
  ASN: AS15133

[TECHNOLOGY]
  CMS: Drupal 10
  Server: nginx/1.21.6
  Frameworks: React, Bootstrap
  JavaScript: jQuery 3.6.0, D3.js 7.8.0

[SECURITY]
  CDN: Cloudflare (95% confidence)
  WAF: Cloudflare WAF (90% confidence)
  TLS Version: TLSv1.3
  Certificate: Valid until 2026-01-19
  Security Headers:
    ✓ Strict-Transport-Security
    ✓ X-Content-Type-Options
    ✓ X-Frame-Options
    ✗ Content-Security-Policy (missing)

[SUBDOMAINS] (24 found via Certificate Transparency)
  www.example.com
  api.example.com
  staging.example.com
  (21 more...)

[ORIGIN_INFRASTRUCTURE]
  Detection Methods: subdomain_bruteforce, mx_records
  Potential Origins: 2
    • 198.51.100.42 → AWS (70% confidence)
    • 203.0.113.10 → DigitalOcean (50% confidence)

[DNS_RECORDS]
  MX Records: mail.example.com (priority: 10)
  NS Records: ns1.example.com, ns2.example.com
  TXT Records: v=spf1 include:_spf.example.com ~all
```

---

## Performance & Best Practices

### Scanning Speed

- **Concurrent Requests**: ThreadPoolExecutor for parallel path checking (~60-70% faster)
- **Connection Pooling**: Reuses TCP connections (10 connections, 20 max pool)
- **DNS Caching**: Reduces redundant queries
- **Rate Limiting**: Configurable delays to respect target servers

### Recommended Settings

```python
# config/settings.py

# Timeouts
DEFAULT_TIMEOUT = 45      # HTTP request timeout (seconds)
DNS_TIMEOUT = 10          # DNS query timeout (seconds)

# Rate Limiting
RATE_LIMIT_DELAY = 0.5    # Delay between requests (seconds)
MAX_CONCURRENT_REQUESTS = 5

# Retries
MAX_RETRIES = 3           # HTTP retry attempts
BACKOFF_FACTOR = 2        # Exponential backoff multiplier
```

### Ethical Scanning Guidelines

1. **Authorization Required** - Always obtain written permission
2. **Respect robots.txt** - Honor website directives
3. **Rate Limiting** - Don't overwhelm target servers
4. **Legal Compliance** - Follow local laws and regulations
5. **Responsible Disclosure** - Report findings ethically
6. **No Active Attacks** - Use only passive techniques
7. **Data Protection** - Secure storage of scan results

---

## Troubleshooting

### Common Issues

#### DNS Resolution Failures

```bash
# Use custom DNS servers
export DNS_NAMESERVERS="8.8.8.8,1.1.1.1"
python main.py example.com
```

#### Timeout Errors

```bash
# Increase timeout
# Edit config/settings.py:
DEFAULT_TIMEOUT = 60  # Increase from 45 to 60
```

#### Rate Limiting / 429 Errors

```bash
# Automatic retry with exponential backoff is built-in
# To increase delay between requests:
# Edit config/settings.py:
RATE_LIMIT_DELAY = 1.0  # Increase from 0.5 to 1.0
```

#### Certificate Verification Errors

```bash
# Behind corporate proxy with SSL inspection:
export REQUESTS_CA_BUNDLE=/path/to/corporate-ca-bundle.crt
python main.py example.com
```

---

## Appendix: Quick Reference

### Command Cheat Sheet

```bash
# Basic scan
python main.py example.com

# Save JSON output
python main.py example.com -o json

# Verbose mode
python main.py example.com -v

# Docker scan
docker run --rm rankle example.com

# Extract subdomains
jq -r '.subdomains[]' scan.json

# Count technologies
jq '.technologies_web.detected_technologies | length' scan.json

# Get origin IPs
jq -r '.origin_discovery.potential_origins[].ip' scan.json

# Pipe to Nuclei
python main.py example.com -o json | jq -r '.subdomains[]' | nuclei -l -

# Pipe to Nmap
jq -r '.dns.A[]' scan.json | nmap -iL - -sV
```

### JSON Path Reference

```javascript
.domain                          // Target domain
.scan_time                       // Timestamp
.dns.A[]                        // IPv4 addresses
.dns.AAAA[]                     // IPv6 addresses
.dns.MX[].host                  // Mail servers
.subdomains[]                   // Discovered subdomains
.cdn.name                       // CDN provider
.cdn.confidence                 // Detection confidence
.waf.name                       // WAF solution
.technologies_web.cms           // Detected CMS
.technologies_web.detected_technologies[].name   // All technologies
.origin_discovery.potential_origins[].ip         // Origin IPs
.http_fingerprint.exposed_paths[]               // Exposed files
.http_fingerprint.allowed_methods[]             // HTTP methods
```

---

## License & Disclaimer

**License**: MIT License

**Disclaimer**: This tool is for **authorized security testing only**. Users must:
- Obtain proper authorization before scanning
- Comply with all applicable laws and regulations
- Use responsibly and ethically
- Not use for malicious purposes

Unauthorized access to computer systems is illegal.

---

**Documentation Version**: 1.0.0
**Last Updated**: 2025-01-19
**Rankle Version**: 1.0.0-RC

For more information, visit the [GitHub repository](https://github.com/javicosvml/rankle).
