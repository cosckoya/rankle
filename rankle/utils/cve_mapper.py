"""
CVE mapping utilities for detected technologies.

Maps technology names and versions to Common Platform Enumeration (CPE)
identifiers and provides CVE search URLs for vulnerability research.
"""

from typing import Any
from urllib.parse import quote


def generate_cpe(vendor: str, product: str, version: str | None = None) -> str:
    """
    Generate CPE 2.3 identifier for technology.

    CPE Format: cpe:2.3:a:vendor:product:version:*:*:*:*:*:*:*

    Args:
        vendor: Technology vendor (e.g., "wordpress", "django")
        product: Product name (e.g., "wordpress", "django")
        version: Version string (e.g., "6.4.2"), None if unknown

    Returns:
        CPE 2.3 formatted string

    Example:
        >>> generate_cpe("wordpress", "wordpress", "6.4.2")
        'cpe:2.3:a:wordpress:wordpress:6.4.2:*:*:*:*:*:*:*'
    """
    vendor_normalized = vendor.lower().replace(" ", "_")
    product_normalized = product.lower().replace(" ", "_")
    version_part = version if version else "*"

    return f"cpe:2.3:a:{vendor_normalized}:{product_normalized}:{version_part}:*:*:*:*:*:*:*"


def map_technology_to_cve_urls(
    tech_name: str,
    version: str | None = None,
) -> dict[str, Any]:
    """
    Generate CVE search URLs for detected technology.

    Creates URLs for multiple CVE databases to facilitate
    vulnerability research.

    Args:
        tech_name: Technology name (e.g., "WordPress", "Django")
        version: Technology version if known

    Returns:
        Dictionary with CPE and CVE search URLs

    Example:
        >>> map_technology_to_cve_urls("WordPress", "6.4.2")
        {
            'technology': 'WordPress',
            'version': '6.4.2',
            'cpe': 'cpe:2.3:a:wordpress:wordpress:6.4.2:*:*:*:*:*:*:*',
            'cve_search_urls': {...}
        }
    """
    # Normalize technology name for CPE
    vendor_map = _get_vendor_map()
    vendor = vendor_map.get(tech_name.lower(), tech_name.lower())
    product = tech_name.lower()

    cpe = generate_cpe(vendor, product, version)

    # Build search queries
    search_query = f"{tech_name} {version}" if version else tech_name
    encoded_query = quote(search_query)

    return {
        "technology": tech_name,
        "version": version,
        "cpe": cpe,
        "cve_search_urls": {
            "nist_nvd": f"https://nvd.nist.gov/vuln/search/results?form_type=Advanced&query={encoded_query}",
            "cve_mitre": f"https://cve.mitre.org/cgi-bin/cvekey.cgi?keyword={encoded_query}",
            "cvedetails": f"https://www.cvedetails.com/google-search-results.php?q={encoded_query}",
            "vulners": f"https://vulners.com/search?query={encoded_query}",
            "exploit_db": f"https://www.exploit-db.com/search?q={encoded_query}",
        },
        "recommendation": "Review CVE databases for known vulnerabilities in this version",
    }


def _get_vendor_map() -> dict[str, str]:
    """
    Map technology names to CPE vendor names.

    Returns:
        Dictionary mapping technology to vendor identifier

    Example:
        >>> _get_vendor_map()["wordpress"]
        'wordpress'
    """
    return {
        # CMS
        "wordpress": "wordpress",
        "drupal": "drupal",
        "joomla": "joomla",
        "magento": "magento",
        "shopify": "shopify",
        # Frameworks
        "django": "djangoproject",
        "laravel": "laravel",
        "ruby on rails": "rubyonrails",
        "express": "expressjs",
        "flask": "palletsprojects",
        "fastapi": "tiangolo",
        "asp.net": "microsoft",
        "spring": "vmware",
        "spring boot": "vmware",
        # JavaScript
        "react": "facebook",
        "vue": "vuejs",
        "vue.js": "vuejs",
        "angular": "angular",
        "next.js": "vercel",
        "nuxt.js": "nuxtjs",
        "jquery": "jquery",
        # Web Servers
        "nginx": "f5",
        "apache": "apache",
        "iis": "microsoft",
        "tomcat": "apache",
        # Other
        "woocommerce": "woocommerce",
        "elementor": "elementor",
        "yoast seo": "yoast",
        "jetpack": "automattic",
    }


def get_high_risk_technologies() -> dict[str, list[str]]:
    """
    List of technologies with known critical vulnerabilities.

    Returns:
        Dictionary mapping technology to list of concerns

    Example:
        >>> get_high_risk_technologies()["wordpress"]
        ['Frequently targeted', 'Plugin vulnerabilities common', ...]
    """
    return {
        "WordPress": [
            "Frequently targeted by attackers",
            "Plugin vulnerabilities common",
            "Requires regular updates",
            "Check wp-admin/install.php exposure",
        ],
        "Drupal": [
            "Historical critical RCE vulnerabilities",
            "Drupalgeddon 2/3 attacks",
            "Module vulnerabilities",
        ],
        "Joomla": [
            "Historical SQL injection issues",
            "Extension vulnerabilities",
            "Admin panel exposure",
        ],
        "Apache": [
            "CVE-2021-44228 (Log4j) if using Java",
            "Directory traversal risks",
            "Check for outdated versions",
        ],
        "nginx": [
            "Buffer overflow in older versions",
            "Integer overflow vulnerabilities",
            "Check for version < 1.20",
        ],
        "jQuery": [
            "XSS vulnerabilities in older versions",
            "DOM-based vulnerabilities",
            "Update to latest version",
        ],
        "PHP": [
            "Memory corruption vulnerabilities",
            "Deserialization attacks",
            "Check PHP version < 7.4 (EOL)",
        ],
        "ASP.NET": [
            "ViewState deserialization",
            "Request validation bypass",
            "Check for .NET framework version",
        ],
    }


def assess_technology_risk(
    tech_name: str,
    version: str | None = None,
) -> dict[str, Any]:
    """
    Assess security risk for detected technology.

    Args:
        tech_name: Technology name
        version: Technology version if known

    Returns:
        Risk assessment with severity and recommendations

    Example:
        >>> assess_technology_risk("WordPress", "5.0.0")
        {'severity': 'high', 'concerns': [...], 'action': '...'}
    """
    high_risk = get_high_risk_technologies()
    concerns = high_risk.get(tech_name, [])

    severity = "medium"  # Default
    if concerns:
        severity = "high"

    # Version-specific risk assessment
    version_concerns: list[str] = []
    if version:
        version_concerns = _assess_version_risk(tech_name, version)

    all_concerns = concerns + version_concerns

    return {
        "technology": tech_name,
        "version": version,
        "severity": severity,
        "concerns": all_concerns,
        "action": "Review CVE databases and update to latest version" if all_concerns else "Monitor for new vulnerabilities",
        "cve_urls": map_technology_to_cve_urls(tech_name, version)["cve_search_urls"],
    }


def _assess_version_risk(tech_name: str, version: str) -> list[str]:
    """
    Assess version-specific security risks.

    Args:
        tech_name: Technology name
        version: Version string

    Returns:
        List of version-specific concerns
    """
    concerns: list[str] = []

    # WordPress version checks
    if tech_name.lower() == "wordpress":
        try:
            major, minor, patch = map(int, version.split(".")[:3])
            if major < 6:
                concerns.append(f"WordPress {version} is outdated (current: 6.4+)")
            if major == 5 and minor < 9:
                concerns.append("Multiple known vulnerabilities in WordPress < 5.9")
        except (ValueError, AttributeError):
            pass

    # jQuery version checks
    if tech_name.lower() == "jquery":
        try:
            major, minor = map(int, version.split(".")[:2])
            if major < 3:
                concerns.append(f"jQuery {version} has known XSS vulnerabilities")
            if major == 3 and minor < 5:
                concerns.append("Update jQuery to 3.5.0+ for security fixes")
        except (ValueError, AttributeError):
            pass

    # Django version checks
    if tech_name.lower() == "django":
        try:
            major, minor = map(int, version.split(".")[:2])
            if major < 4:
                concerns.append(f"Django {version} is outdated (current: 4.x+)")
            if major == 3 and minor < 2:
                concerns.append("Multiple CVEs fixed in Django 3.2+")
        except (ValueError, AttributeError):
            pass

    return concerns
