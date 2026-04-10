"""
Technology Detection Module for Rankle

Detects web technologies through multiple passive techniques:
- HTML content pattern matching
- HTTP Headers analysis
- Cookie analysis
- Meta tags parsing
- JavaScript global detection
- Version extraction
"""

import json
import logging
import re
from pathlib import Path
from typing import Any

from bs4 import BeautifulSoup

from config.settings import MINIMUM_DETECTION_CONFIDENCE
from rankle.utils.confidence import calculate_confidence_score


logger = logging.getLogger(__name__)


# Load signatures from config file
def _load_signatures() -> dict[str, Any]:
    """Load technology signatures from JSON config."""
    config_path = (
        Path(__file__).parent.parent.parent / "config" / "tech_signatures.json"
    )
    try:
        with config_path.open(encoding="utf-8") as f:
            data: dict[str, Any] = json.load(f)
            technologies: dict[str, Any] = data.get("technologies", {})
            return technologies
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


TECH_SIGNATURES = _load_signatures()

# Additional runtime signatures (extend JSON config)
ADDITIONAL_SIGNATURES: dict[str, dict[str, Any]] = {
    "Django": {
        "category": "Web Framework",
        "patterns": {
            "html": ["csrfmiddlewaretoken", "django"],
            "headers": {"X-Frame-Options": ["SAMEORIGIN"]},
            "cookies": ["csrftoken", "sessionid"],
        },
        "version_patterns": [],
        "confidence_weights": {"header": 0.3, "cookie": 0.5, "pattern": 0.3},
    },
    "Laravel": {
        "category": "Web Framework",
        "patterns": {
            "html": ["laravel", "csrf-token"],
            "headers": {},
            "cookies": ["laravel_session", "XSRF-TOKEN"],
        },
        "version_patterns": [],
        "confidence_weights": {"cookie": 0.6, "pattern": 0.3},
    },
    "Ruby on Rails": {
        "category": "Web Framework",
        "patterns": {
            "html": ["rails", "csrf-token", "authenticity_token"],
            "headers": {"X-Runtime": [""], "X-Request-Id": [""]},
            "cookies": ["_session_id"],
        },
        "version_patterns": [],
        "confidence_weights": {"header": 0.4, "cookie": 0.5, "pattern": 0.3},
    },
    "Express": {
        "category": "Web Framework",
        "patterns": {
            "headers": {"X-Powered-By": ["Express"]},
        },
        "version_patterns": [],
        "confidence_weights": {"header": 0.7},
    },
    "Flask": {
        "category": "Web Framework",
        "patterns": {
            "cookies": ["session"],
            "headers": {"Server": ["Werkzeug"]},
        },
        "version_patterns": ["Werkzeug/([\\d.]+)"],
        "confidence_weights": {"header": 0.5, "cookie": 0.3},
    },
    "FastAPI": {
        "category": "Web Framework",
        "patterns": {
            "html": ["/openapi.json", "/docs", "/redoc"],
            "headers": {},
        },
        "version_patterns": [],
        "confidence_weights": {"pattern": 0.5},
    },
    "ASP.NET": {
        "category": "Web Framework",
        "patterns": {
            "html": ["__VIEWSTATE", "__EVENTVALIDATION", "aspnetForm"],
            "headers": {"X-AspNet-Version": [""], "X-Powered-By": ["ASP.NET"]},
            "cookies": ["ASP.NET_SessionId", ".ASPXAUTH"],
        },
        "version_patterns": ["X-AspNet-Version: ([\\d.]+)"],
        "confidence_weights": {"header": 0.6, "cookie": 0.5, "pattern": 0.4},
    },
    "Spring": {
        "category": "Web Framework",
        "patterns": {
            "headers": {"X-Application-Context": [""]},
            "cookies": ["JSESSIONID"],
            "html": ["spring", "org.springframework"],
        },
        "version_patterns": [],
        "confidence_weights": {"header": 0.5, "cookie": 0.3, "pattern": 0.3},
    },
    "Svelte": {
        "category": "JavaScript Framework",
        "patterns": {
            "html": ["svelte", "__svelte"],
            "js_globals": ["__svelte"],
        },
        "version_patterns": [],
        "confidence_weights": {"pattern": 0.4, "js_global": 0.6},
    },
    "Next.js": {
        "category": "JavaScript Framework",
        "patterns": {
            "html": [
                "/_next/static/",
                "__NEXT_DATA__",
                "_next/image",
                "next-head",
            ],
            "headers": {"x-nextjs-cache": [""]},
            "js_globals": ["__NEXT_DATA__"],
        },
        "version_patterns": ["/_next/static/([^/]+)/"],
        "confidence_weights": {"pattern": 0.6, "header": 0.7, "js_global": 0.8},
    },
    "Nuxt.js": {
        "category": "JavaScript Framework",
        "patterns": {
            "html": [
                "/_nuxt/",
                "__NUXT__",
                "nuxt-link",
                "nuxt-page",
            ],
            "headers": {"x-nuxt-": [""]},
            "js_globals": ["__NUXT__", "$nuxt"],
        },
        "version_patterns": ["/_nuxt/([^/]+)/"],
        "confidence_weights": {"pattern": 0.6, "header": 0.7, "js_global": 0.8},
    },
    "Astro": {
        "category": "JavaScript Framework",
        "patterns": {
            "html": [
                "data-astro-cid-",
                "<!--astro:",
                "/_astro/",
                "astro-island",
            ],
        },
        "version_patterns": [],
        "confidence_weights": {"pattern": 0.7},
    },
    "SvelteKit": {
        "category": "JavaScript Framework",
        "patterns": {
            "html": [
                "__sveltekit",
                "sveltekit:",
                "data-sveltekit-",
                "/_app/",
            ],
            "js_globals": ["__sveltekit"],
        },
        "version_patterns": [],
        "confidence_weights": {"pattern": 0.7, "js_global": 0.8},
    },
    "Remix": {
        "category": "JavaScript Framework",
        "patterns": {
            "html": [
                "/__remix",
                "remix-route",
                "/__remix_manifest",
            ],
        },
        "version_patterns": [],
        "confidence_weights": {"pattern": 0.7},
    },
    "Vite": {
        "category": "Build Tool",
        "patterns": {
            "html": [
                "/@vite/",
                "vite.svg",
                "/@fs/",
            ],
        },
        "version_patterns": [],
        "confidence_weights": {"pattern": 0.6},
    },
    "Tailwind CSS": {
        "category": "CSS Framework",
        "patterns": {
            "html": [
                r"class=\"[^\"]*(?:flex|grid|w-|h-|p-|m-|text-|bg-|border-|rounded-)[^\"]*\"",
                "tailwindcss",
                "tailwind",
            ],
        },
        "version_patterns": ["tailwindcss@([\\d.]+)"],
        "confidence_weights": {"pattern": 0.5},
    },
    "WooCommerce": {
        "category": "E-commerce",
        "patterns": {
            "html": ["woocommerce", "wc-", "/wc-api/"],
            "cookies": ["woocommerce_"],
            "js_globals": ["wc_add_to_cart_params"],
        },
        "version_patterns": ["WooCommerce ([\\d.]+)"],
        "confidence_weights": {"pattern": 0.4, "cookie": 0.4, "js_global": 0.5},
    },
    "PrestaShop": {
        "category": "E-commerce",
        "patterns": {
            "html": ["prestashop", "presta"],
            "cookies": ["PrestaShop-"],
            "meta": ["PrestaShop"],
        },
        "version_patterns": ["PrestaShop ([\\d.]+)"],
        "confidence_weights": {"pattern": 0.4, "cookie": 0.5, "meta": 0.5},
    },
    "Squarespace": {
        "category": "CMS",
        "patterns": {
            "html": ["squarespace", "static.squarespace.com"],
            "headers": {"X-ServedBy": ["squarespace"]},
        },
        "version_patterns": [],
        "confidence_weights": {"header": 0.6, "pattern": 0.5},
    },
    "Wix": {
        "category": "CMS",
        "patterns": {
            "html": ["wix.com", "static.wixstatic.com", "_wix_browser_sess"],
            "cookies": ["wixSession"],
        },
        "version_patterns": [],
        "confidence_weights": {"pattern": 0.6, "cookie": 0.5},
    },
    "Ghost": {
        "category": "CMS",
        "patterns": {
            "html": ["ghost", "ghost-"],
            "headers": {"X-Ghost-": [""]},
            "meta": ["Ghost"],
        },
        "version_patterns": ["Ghost ([\\d.]+)"],
        "confidence_weights": {"header": 0.5, "pattern": 0.4, "meta": 0.5},
    },
    "Contentful": {
        "category": "Headless CMS",
        "patterns": {
            "html": ["contentful", "ctfassets.net"],
        },
        "version_patterns": [],
        "confidence_weights": {"pattern": 0.5},
    },
    "Strapi": {
        "category": "Headless CMS",
        "patterns": {
            "html": ["/api/", "strapi"],
            "headers": {"X-Powered-By": ["Strapi"]},
        },
        "version_patterns": [],
        "confidence_weights": {"header": 0.6, "pattern": 0.3},
    },
    "Google Tag Manager": {
        "category": "Tag Manager",
        "patterns": {
            "html": [
                "googletagmanager.com/gtm.js",
                "GTM-",
                "gtm.start",
            ],
        },
        "version_patterns": [],
        "confidence_weights": {"pattern": 0.7},
    },
    "Hotjar": {
        "category": "Analytics",
        "patterns": {
            "html": ["hotjar", "static.hotjar.com", "hj.q"],
            "cookies": ["_hj"],
        },
        "version_patterns": [],
        "confidence_weights": {"pattern": 0.6, "cookie": 0.5},
    },
    "Segment": {
        "category": "Analytics",
        "patterns": {
            "html": ["segment.com/analytics.js", "analytics.load"],
            "js_globals": ["analytics"],
        },
        "version_patterns": [],
        "confidence_weights": {"pattern": 0.5, "js_global": 0.4},
    },
    "Mixpanel": {
        "category": "Analytics",
        "patterns": {
            "html": ["mixpanel", "cdn.mxpnl.com"],
            "cookies": ["mp_"],
            "js_globals": ["mixpanel"],
        },
        "version_patterns": [],
        "confidence_weights": {"pattern": 0.5, "cookie": 0.4, "js_global": 0.5},
    },
    "Intercom": {
        "category": "Customer Support",
        "patterns": {
            "html": ["intercom", "widget.intercom.io", "intercomSettings"],
            "cookies": ["intercom-"],
            "js_globals": ["Intercom"],
        },
        "version_patterns": [],
        "confidence_weights": {"pattern": 0.5, "cookie": 0.4, "js_global": 0.6},
    },
    "Zendesk": {
        "category": "Customer Support",
        "patterns": {
            "html": ["zendesk", "static.zdassets.com", "zdcdn.net"],
            "js_globals": ["zE", "zESettings"],
        },
        "version_patterns": [],
        "confidence_weights": {"pattern": 0.5, "js_global": 0.5},
    },
    "Drift": {
        "category": "Customer Support",
        "patterns": {
            "html": ["drift", "js.driftt.com"],
            "js_globals": ["drift", "driftt"],
        },
        "version_patterns": [],
        "confidence_weights": {"pattern": 0.5, "js_global": 0.5},
    },
    "Crisp": {
        "category": "Customer Support",
        "patterns": {
            "html": ["crisp.chat", "client.crisp.chat"],
            "js_globals": ["$crisp", "CRISP_WEBSITE_ID"],
        },
        "version_patterns": [],
        "confidence_weights": {"pattern": 0.5, "js_global": 0.6},
    },
    "Mailchimp": {
        "category": "Marketing",
        "patterns": {
            "html": ["mailchimp", "list-manage.com", "chimpstatic.com"],
        },
        "version_patterns": [],
        "confidence_weights": {"pattern": 0.6},
    },
    "HubSpot": {
        "category": "Marketing",
        "patterns": {
            "html": ["hubspot", "hs-scripts.com", "hs-analytics.net"],
            "cookies": ["hubspotutk", "__hstc", "__hssc"],
            "js_globals": ["_hsq", "HubSpotConversations"],
        },
        "version_patterns": [],
        "confidence_weights": {"pattern": 0.5, "cookie": 0.5, "js_global": 0.5},
    },
    "reCAPTCHA": {
        "category": "Security",
        "patterns": {
            "html": ["google.com/recaptcha", "grecaptcha", "g-recaptcha"],
            "js_globals": ["grecaptcha"],
        },
        "version_patterns": [],
        "confidence_weights": {"pattern": 0.6, "js_global": 0.6},
    },
    "hCaptcha": {
        "category": "Security",
        "patterns": {
            "html": ["hcaptcha.com", "h-captcha"],
            "js_globals": ["hcaptcha"],
        },
        "version_patterns": [],
        "confidence_weights": {"pattern": 0.6, "js_global": 0.6},
    },
    "Cloudflare Turnstile": {
        "category": "Security",
        "patterns": {
            "html": ["challenges.cloudflare.com/turnstile", "cf-turnstile"],
            "js_globals": ["turnstile"],
        },
        "version_patterns": [],
        "confidence_weights": {"pattern": 0.6, "js_global": 0.6},
    },
    "Varnish": {
        "category": "Cache",
        "patterns": {
            "headers": {"Via": ["varnish"], "X-Varnish": [""]},
        },
        "version_patterns": [],
        "confidence_weights": {"header": 0.7},
    },
    "Redis": {
        "category": "Cache",
        "patterns": {
            "headers": {"X-Cache-Engine": ["Redis"]},
        },
        "version_patterns": [],
        "confidence_weights": {"header": 0.6},
    },
    "OpenResty": {
        "category": "Web Server",
        "patterns": {
            "headers": {"Server": ["openresty"]},
        },
        "version_patterns": ["openresty/([\\d.]+)"],
        "confidence_weights": {"header": 0.8},
    },
    "LiteSpeed": {
        "category": "Web Server",
        "patterns": {
            "headers": {"Server": ["LiteSpeed"]},
        },
        "version_patterns": ["LiteSpeed/([\\d.]+)"],
        "confidence_weights": {"header": 0.8},
    },
    "IIS": {
        "category": "Web Server",
        "patterns": {
            "headers": {"Server": ["Microsoft-IIS"], "X-Powered-By": ["ASP.NET"]},
        },
        "version_patterns": ["Microsoft-IIS/([\\d.]+)"],
        "confidence_weights": {"header": 0.8},
    },
    "Envoy": {
        "category": "Proxy",
        "patterns": {
            "headers": {"Server": ["envoy"], "X-Envoy-": [""]},
        },
        "version_patterns": [],
        "confidence_weights": {"header": 0.7},
    },
    "Traefik": {
        "category": "Proxy",
        "patterns": {
            "headers": {"Server": ["Traefik"]},
        },
        "version_patterns": [],
        "confidence_weights": {"header": 0.7},
    },
    "HAProxy": {
        "category": "Load Balancer",
        "patterns": {
            "headers": {"Server": ["HAProxy"]},
            "cookies": ["SERVERID"],
        },
        "version_patterns": [],
        "confidence_weights": {"header": 0.7, "cookie": 0.4},
    },
    "Sentry": {
        "category": "Error Tracking",
        "patterns": {
            "html": ["sentry", "browser.sentry-cdn.com", "Sentry.init"],
            "js_globals": ["Sentry"],
        },
        "version_patterns": [],
        "confidence_weights": {"pattern": 0.5, "js_global": 0.6},
    },
    "New Relic": {
        "category": "APM",
        "patterns": {
            "html": ["newrelic", "js-agent.newrelic.com", "NREUM"],
            "js_globals": ["NREUM", "newrelic"],
        },
        "version_patterns": [],
        "confidence_weights": {"pattern": 0.5, "js_global": 0.6},
    },
    "Datadog": {
        "category": "APM",
        "patterns": {
            "html": ["datadoghq", "datadog"],
            "js_globals": ["DD_RUM", "DD_LOGS"],
        },
        "version_patterns": [],
        "confidence_weights": {"pattern": 0.5, "js_global": 0.6},
    },
    "Stripe": {
        "category": "Payment",
        "patterns": {
            "html": ["stripe", "js.stripe.com"],
            "js_globals": ["Stripe"],
        },
        "version_patterns": [],
        "confidence_weights": {"pattern": 0.6, "js_global": 0.7},
    },
    "PayPal": {
        "category": "Payment",
        "patterns": {
            "html": ["paypal", "paypalobjects.com"],
            "js_globals": ["paypal"],
        },
        "version_patterns": [],
        "confidence_weights": {"pattern": 0.6, "js_global": 0.6},
    },
    "Braintree": {
        "category": "Payment",
        "patterns": {
            "html": ["braintree", "js.braintreegateway.com"],
            "js_globals": ["braintree"],
        },
        "version_patterns": [],
        "confidence_weights": {"pattern": 0.5, "js_global": 0.6},
    },
    "Lodash": {
        "category": "JavaScript Library",
        "patterns": {
            "html": ["lodash"],
            "js_globals": ["_"],
        },
        "version_patterns": ["lodash[.-]([\\d.]+)"],
        "confidence_weights": {"pattern": 0.3, "js_global": 0.3},
    },
    "Axios": {
        "category": "JavaScript Library",
        "patterns": {
            "html": ["axios"],
        },
        "version_patterns": ["axios@([\\d.]+)"],
        "confidence_weights": {"pattern": 0.4},
    },
    "D3.js": {
        "category": "JavaScript Library",
        "patterns": {
            "html": ["d3.js", "d3.min.js"],
            "js_globals": ["d3"],
        },
        "version_patterns": ["d3[.-]([\\d.]+)"],
        "confidence_weights": {"pattern": 0.4, "js_global": 0.5},
    },
    "Three.js": {
        "category": "JavaScript Library",
        "patterns": {
            "html": ["three.js", "three.min.js"],
            "js_globals": ["THREE"],
        },
        "version_patterns": ["three[.-]([\\d.]+)"],
        "confidence_weights": {"pattern": 0.4, "js_global": 0.5},
    },
    "GSAP": {
        "category": "Animation",
        "patterns": {
            "html": ["gsap", "greensock"],
            "js_globals": ["gsap", "TweenMax", "TweenLite"],
        },
        "version_patterns": ["gsap@([\\d.]+)"],
        "confidence_weights": {"pattern": 0.4, "js_global": 0.5},
    },
    "AOS": {
        "category": "Animation",
        "patterns": {
            "html": ["aos.js", "data-aos="],
        },
        "version_patterns": [],
        "confidence_weights": {"pattern": 0.5},
    },
    "Font Awesome": {
        "category": "Icons",
        "patterns": {
            "html": ["font-awesome", "fontawesome", "fa-"],
        },
        "version_patterns": ["font-awesome[/-]([\\d.]+)"],
        "confidence_weights": {"pattern": 0.5},
    },
    "Material Icons": {
        "category": "Icons",
        "patterns": {
            "html": ["material-icons", "fonts.googleapis.com/icon"],
        },
        "version_patterns": [],
        "confidence_weights": {"pattern": 0.5},
    },
    "ZURB Foundation": {
        "category": "CSS Framework",
        "patterns": {
            "html": ["foundation", "Foundation."],
            "js_globals": ["Foundation"],
        },
        "version_patterns": ["foundation[.-]([\\d.]+)"],
        "confidence_weights": {"pattern": 0.4, "js_global": 0.5},
    },
    "Bulma": {
        "category": "CSS Framework",
        "patterns": {
            "html": ["bulma", "is-", "has-text-"],
        },
        "version_patterns": ["bulma[/-]([\\d.]+)"],
        "confidence_weights": {"pattern": 0.4},
    },
    "Semantic UI": {
        "category": "CSS Framework",
        "patterns": {
            "html": ["semantic-ui", "semantic.min"],
        },
        "version_patterns": ["semantic[.-]([\\d.]+)"],
        "confidence_weights": {"pattern": 0.5},
    },
    "Material UI": {
        "category": "CSS Framework",
        "patterns": {
            "html": ["@mui", "@material-ui", "MuiButton"],
        },
        "version_patterns": [],
        "confidence_weights": {"pattern": 0.5},
    },
    "Chakra UI": {
        "category": "CSS Framework",
        "patterns": {
            "html": ["@chakra-ui", "chakra-"],
        },
        "version_patterns": [],
        "confidence_weights": {"pattern": 0.5},
    },
    "Ant Design": {
        "category": "CSS Framework",
        "patterns": {
            "html": ["antd", "ant-"],
        },
        "version_patterns": [],
        "confidence_weights": {"pattern": 0.5},
    },
}


class TechnologyDetector:
    """Detects web technologies using passive analysis techniques.

    Integrates Wappalyzer (3000+ signatures), favicon hashing (mmh3),
    and custom pattern matching to identify CMS, frameworks, libraries,
    and servers with confidence scores (0-100%).

    Supported categories:
    - CMS: WordPress, Drupal, Joomla, Magento, Ghost, etc.
    - Frameworks: Django, Rails, Laravel, .NET, Spring, etc.
    - JavaScript: React, Vue, Angular, jQuery, Bootstrap, etc.
    - Servers: Apache, nginx, IIS, etc.
    - Languages: PHP, Python, Java, C#, etc.

    Attributes:
        domain: Target domain being analyzed.
        signatures: Combined technology detection signatures and patterns.
    """

    def __init__(self, domain: str) -> None:
        """Initialize technology detector.

        Args:
            domain: Target domain to analyze.

        Example:
            >>> detector = TechnologyDetector("wordpress.com")
            >>> results = detector.detect(
            ...     headers={"Server": "Apache/2.4"},
            ...     body="<meta name='generator' content='WordPress 6.4' />"
            ... )
        """
        self.domain = domain
        # Merge signatures from JSON and additional
        self.signatures = {**TECH_SIGNATURES, **ADDITIONAL_SIGNATURES}

    def detect(
        self,
        headers: dict[str, str] | None = None,
        cookies: list[str] | None = None,
        body: str | None = None,
    ) -> dict[str, Any]:
        """Perform comprehensive technology detection on HTTP response data.

        Analyzes multiple sources (headers, cookies, HTML body) using pattern
        matching and signature-based detection to identify technologies with
        confidence scoring (0-100%).

        Args:
            headers: HTTP response headers dict (e.g., {"Server": "Apache/2.4"}).
            cookies: List of cookie names from Set-Cookie headers.
            body: HTML response body as string.

        Returns:
            Dict mapping technology names to detection data:
            {
                "WordPress": {
                    "confidence": 0.95,
                    "version": "6.4.1",
                    "category": "CMS",
                    "evidence": ["meta generator tag", "wp-content directory"]
                },
                ...
            }
        """
        results: dict[str, Any] = {
            "detected": False,
            "technologies": [],
            "categories": {},
        }

        if not any([headers, cookies, body]):
            return results

        all_detections: list[dict[str, Any]] = []

        for tech_name, signatures in self.signatures.items():
            evidence: list[dict[str, Any]] = []

            # Check headers
            if headers:
                header_matches = self._check_headers(headers, signatures)
                evidence.extend(header_matches)

            # Check cookies
            if cookies:
                cookie_matches = self._check_cookies(cookies, signatures)
                evidence.extend(cookie_matches)

            # Check HTML body
            if body:
                html_matches = self._check_html(body, signatures)
                evidence.extend(html_matches)

                # Check meta tags
                meta_matches = self._check_meta_tags(body, signatures)
                evidence.extend(meta_matches)

                # Extract version
                version = self._extract_version(body, headers or {}, signatures)
            else:
                version = None

            if evidence:
                confidence = self._calculate_confidence(evidence, signatures)
                if confidence >= MINIMUM_DETECTION_CONFIDENCE:
                    detection = {
                        "name": tech_name,
                        "category": signatures.get("category", "Unknown"),
                        "confidence": round(confidence, 2),
                        "version": version,
                        "evidence": evidence,
                    }
                    all_detections.append(detection)

        # Sort by confidence
        all_detections.sort(key=lambda x: x["confidence"], reverse=True)

        if all_detections:
            results["detected"] = True
            results["technologies"] = all_detections

            # Group by category
            for tech in all_detections:
                category = tech["category"]
                if category not in results["categories"]:
                    results["categories"][category] = []
                results["categories"][category].append(
                    {
                        "name": tech["name"],
                        "confidence": tech["confidence"],
                        "version": tech["version"],
                    }
                )

        return results

    def _check_headers(
        self, headers: dict[str, str], signatures: dict[str, Any]
    ) -> list[dict[str, Any]]:
        """Check HTTP headers for technology signatures."""
        matches = []
        headers_lower = {k.lower(): v for k, v in headers.items()}
        patterns = signatures.get("patterns", {}).get("headers", {})

        for header_pattern, value_patterns in patterns.items():
            header_pattern_lower = header_pattern.lower()

            for header_name, header_value in headers_lower.items():
                # Check for prefix match (e.g., "X-Powered-By")
                if header_pattern_lower.endswith("-"):
                    if header_name.startswith(header_pattern_lower):
                        matches.append(
                            {
                                "type": "header",
                                "detail": f"{header_name} header present",
                                "weight": signatures.get("confidence_weights", {}).get(
                                    "header", 0.4
                                ),
                            }
                        )
                elif header_name == header_pattern_lower:
                    for pattern in value_patterns:
                        if not pattern:  # Empty = just check existence
                            matches.append(
                                {
                                    "type": "header",
                                    "detail": f"{header_name} header present",
                                    "weight": signatures.get(
                                        "confidence_weights", {}
                                    ).get("header", 0.4),
                                }
                            )
                            break
                        if re.search(pattern, header_value, re.IGNORECASE):
                            matches.append(
                                {
                                    "type": "header",
                                    "detail": f"{header_name}: {header_value[:50]}",
                                    "weight": signatures.get(
                                        "confidence_weights", {}
                                    ).get("header", 0.4),
                                }
                            )
                            break

        return matches

    def _check_cookies(
        self, cookies: list[str], signatures: dict[str, Any]
    ) -> list[dict[str, Any]]:
        """Check cookies for technology signatures."""
        matches = []
        patterns = signatures.get("patterns", {}).get("cookies", [])

        for pattern in patterns:
            for cookie_name in cookies:
                if re.search(pattern, cookie_name, re.IGNORECASE):
                    matches.append(
                        {
                            "type": "cookie",
                            "detail": f"Cookie: {cookie_name}",
                            "weight": signatures.get("confidence_weights", {}).get(
                                "cookie", 0.3
                            ),
                        }
                    )
                    break  # One match per pattern is enough

        return matches

    def _check_html(
        self, body: str, signatures: dict[str, Any]
    ) -> list[dict[str, Any]]:
        """Check HTML body for technology patterns."""
        matches = []
        patterns = signatures.get("patterns", {}).get("html", [])

        body_lower = body.lower()

        for pattern in patterns:
            try:
                if re.search(pattern, body_lower, re.IGNORECASE):
                    # Truncate pattern for display
                    display_pattern = (
                        pattern[:30] + "..." if len(pattern) > 30 else pattern
                    )
                    matches.append(
                        {
                            "type": "html_pattern",
                            "detail": f"Pattern: {display_pattern}",
                            "weight": signatures.get("confidence_weights", {}).get(
                                "pattern", 0.3
                            ),
                        }
                    )
            except re.error:
                # Invalid regex, try as literal string
                if pattern.lower() in body_lower:
                    matches.append(
                        {
                            "type": "html_pattern",
                            "detail": f"Pattern: {pattern[:30]}",
                            "weight": signatures.get("confidence_weights", {}).get(
                                "pattern", 0.3
                            ),
                        }
                    )

        # Check JavaScript globals in scripts
        js_globals = signatures.get("patterns", {}).get("js_globals", [])
        for js_global in js_globals:
            # Look for assignments or references
            js_patterns = [
                rf"window\.{js_global}\s*=",
                rf"typeof\s+{js_global}",
                rf'"{js_global}"',
                rf"'{js_global}'",
                rf"\b{js_global}\b",
            ]
            for js_pattern in js_patterns:
                if re.search(js_pattern, body, re.IGNORECASE):
                    matches.append(
                        {
                            "type": "js_global",
                            "detail": f"JS Global: {js_global}",
                            "weight": signatures.get("confidence_weights", {}).get(
                                "js_global", 0.4
                            ),
                        }
                    )
                    break

        return matches

    def _check_meta_tags(
        self, body: str, signatures: dict[str, Any]
    ) -> list[dict[str, Any]]:
        """Check meta tags for technology signatures."""
        matches: list[dict[str, Any]] = []
        meta_patterns = signatures.get("patterns", {}).get("meta", [])

        if not meta_patterns:
            return matches

        try:
            soup = BeautifulSoup(body, "html.parser")

            # Check generator meta tag
            generator = soup.find("meta", attrs={"name": "generator"})
            if generator and hasattr(generator, "get"):
                content = generator.get("content", "")
                content_str = str(content) if content else ""
                for pattern in meta_patterns:
                    if re.search(pattern, content_str, re.IGNORECASE):
                        matches.append(
                            {
                                "type": "meta_tag",
                                "detail": f"Generator: {content_str[:50]}",
                                "weight": signatures.get("confidence_weights", {}).get(
                                    "meta", 0.4
                                ),
                            }
                        )
                        break

            # Check all meta tags
            for meta in soup.find_all("meta"):
                content = meta.get("content", "")
                for pattern in meta_patterns:
                    if re.search(pattern, str(content), re.IGNORECASE):
                        matches.append(
                            {
                                "type": "meta_tag",
                                "detail": f"Meta content: {str(content)[:50]}",
                                "weight": signatures.get("confidence_weights", {}).get(
                                    "meta", 0.4
                                ),
                            }
                        )
                        break

        except (AttributeError, TypeError, ValueError):
            # BeautifulSoup parsing errors or invalid HTML
            pass

        return matches

    def _extract_version(
        self, body: str, headers: dict[str, str], signatures: dict[str, Any]
    ) -> str | None:
        """Extract version information from response."""
        version_patterns = signatures.get("version_patterns", [])

        # Check in body
        for pattern in version_patterns:
            try:
                match = re.search(pattern, body, re.IGNORECASE)
                if match:
                    return match.group(1)
            except (re.error, IndexError):
                continue

        # Check in headers
        for header_value in headers.values():
            for pattern in version_patterns:
                try:
                    match = re.search(pattern, header_value, re.IGNORECASE)
                    if match:
                        return match.group(1)
                except (re.error, IndexError):
                    continue

        return None

    def _calculate_confidence(
        self, evidence: list[dict[str, Any]], _signatures: dict[str, Any]
    ) -> float:
        """
        Calculate confidence score from evidence.

        Uses shared confidence calculation utility with weighted scoring
        and diminishing returns for multiple pieces of the same type.

        Args:
            evidence: List of evidence dictionaries
            _signatures: Signature configuration (unused, kept for compatibility)

        Returns:
            Confidence score between 0.0 and 1.0
        """
        return calculate_confidence_score(evidence, diminishing_factor=0.5)

    def detect_enhanced(
        self,
        headers: dict[str, str] | None = None,
        cookies: list[str] | None = None,
        body: str | None = None,
        base_url: str | None = None,
    ) -> dict[str, Any]:
        """
        Enhanced technology detection with Wappalyzer, favicon hash, error fingerprinting.

        Combines traditional detection with modern techniques:
        - Wappalyzer (3000+ technologies)
        - Favicon hashing (mmh3)
        - Error page fingerprinting
        - JavaScript endpoint extraction
        - WordPress plugin detection
        - CVE mapping for detected technologies

        Args:
            headers: HTTP response headers
            cookies: List of cookie names
            body: HTML response body
            base_url: Base URL for fetching additional resources

        Returns:
            Enhanced detection results with CVE information
        """
        # Start with traditional detection
        results = self.detect(headers=headers, cookies=cookies, body=body)

        enhanced_detections: list[dict[str, Any]] = []

        # 1. Wappalyzer integration
        if body and headers and base_url:
            try:
                from Wappalyzer import Wappalyzer, WebPage

                wappalyzer = Wappalyzer.latest()
                webpage = WebPage(base_url, body, dict(headers))
                wap_technologies = wappalyzer.analyze(webpage)

                for tech_name in wap_technologies:
                    enhanced_detections.append(
                        {
                            "name": tech_name,
                            "category": "Unknown",  # Wappalyzer doesn't provide categories
                            "confidence": 0.85,  # Wappalyzer is reliable
                            "version": None,
                            "evidence": [
                                {
                                    "type": "wappalyzer",
                                    "detail": "Detected by Wappalyzer",
                                    "weight": 0.85,
                                }
                            ],
                        }
                    )
            except ImportError:
                logger.debug("Wappalyzer not available, skipping")
            except Exception as e:
                logger.debug("Wappalyzer analysis failed: %s", e)

        # 2. Favicon hashing
        if base_url:
            try:
                from rankle.utils.favicon_hash import analyze_favicon

                favicon_result = analyze_favicon(base_url)
                if favicon_result:
                    enhanced_detections.append(
                        {
                            "name": favicon_result["name"],
                            "category": "Web Application",
                            "confidence": favicon_result["confidence"],
                            "version": None,
                            "evidence": [
                                {
                                    "type": "favicon_hash",
                                    "detail": f"Favicon hash: {favicon_result['hash']}",
                                    "weight": favicon_result["confidence"],
                                }
                            ],
                        }
                    )
            except Exception as e:
                logger.debug("Favicon analysis failed: %s", e)

        # 3. Error page fingerprinting
        if self.domain:
            try:
                from rankle.utils.error_fingerprint import fingerprint_error_page

                error_frameworks = fingerprint_error_page(self.domain)
                for framework in error_frameworks:
                    enhanced_detections.append(framework)
            except Exception as e:
                logger.debug("Error fingerprinting failed: %s", e)

        # 4. JavaScript analysis
        if body and base_url:
            try:
                from rankle.utils.js_extractor import analyze_javascript

                js_results = analyze_javascript(base_url, body, max_files=3)

                # Add detected frameworks
                for framework in js_results["frameworks"]:
                    enhanced_detections.append(framework)

                # Add endpoints to results
                if js_results["endpoints"]:
                    results["api_endpoints"] = js_results["endpoints"][:10]

            except Exception as e:
                logger.debug("JS analysis failed: %s", e)

        # 5. WordPress plugin detection
        if body and headers:
            try:
                from rankle.utils.wordpress_plugins import analyze_wordpress

                wp_results = analyze_wordpress(body, dict(headers))
                if wp_results["is_wordpress"]:
                    results["wordpress"] = wp_results
            except Exception as e:
                logger.debug("WordPress analysis failed: %s", e)

        # 6. Enhanced version extraction from assets
        if body:
            try:
                from rankle.utils.js_extractor import extract_version_from_assets

                asset_versions = extract_version_from_assets(body)
                if asset_versions:
                    results["asset_versions"] = asset_versions
            except Exception as e:
                logger.debug("Version extraction failed: %s", e)

        # Merge enhanced detections with existing
        all_technologies = results.get("technologies", []) + enhanced_detections

        # Deduplicate by name (keep highest confidence)
        seen: dict[str, dict[str, Any]] = {}
        for tech in all_technologies:
            name = tech["name"]
            if name not in seen or tech["confidence"] > seen[name]["confidence"]:
                seen[name] = tech

        results["technologies"] = sorted(
            seen.values(), key=lambda x: x["confidence"], reverse=True
        )
        results["detected"] = len(results["technologies"]) > 0

        # 7. Add CVE mapping for detected technologies
        try:
            from rankle.utils.cve_mapper import map_technology_to_cve_urls

            cve_mappings: list[dict[str, Any]] = []
            for tech in results["technologies"][:10]:  # Top 10 only
                cve_info = map_technology_to_cve_urls(tech["name"], tech.get("version"))
                cve_mappings.append(cve_info)

            results["cve_mappings"] = cve_mappings
        except Exception as e:
            logger.debug("CVE mapping failed: %s", e)

        return results


def detect_technologies(
    domain: str,
    headers: dict[str, str] | None = None,
    cookies: list[str] | None = None,
    body: str | None = None,
) -> dict[str, Any]:
    """
    Convenience function for technology detection.

    Args:
        domain: Target domain
        headers: HTTP response headers
        cookies: List of cookie names
        body: HTML response body

    Returns:
        Technology detection results
    """
    detector = TechnologyDetector(domain)
    return detector.detect(headers=headers, cookies=cookies, body=body)
