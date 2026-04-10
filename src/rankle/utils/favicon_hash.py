"""
Favicon hashing utilities for technology fingerprinting.

Uses MurmurHash3 (mmh3) algorithm to create unique favicon signatures
that can identify technologies even behind CDN/proxy obfuscation.
"""

import codecs
from typing import Any

import mmh3
import requests

from config.settings import DEFAULT_TIMEOUT


def calculate_favicon_hash(
    favicon_url: str, timeout: int = DEFAULT_TIMEOUT
) -> str | None:
    """
    Calculate mmh3 hash of favicon for fingerprinting.

    This method is used by Shodan and httpx for technology detection.
    The hash survives CDN obfuscation and identifies default installations.

    Args:
        favicon_url: Full URL to favicon.ico
        timeout: Request timeout in seconds

    Returns:
        String representation of mmh3 hash, or None if fetch fails

    Example:
        >>> calculate_favicon_hash("https://example.com/favicon.ico")
        '-235440351'
    """
    try:
        response = requests.get(favicon_url, timeout=timeout, allow_redirects=True)
        if response.status_code == 200 and response.content:
            # Base64 encode the favicon
            favicon_b64 = codecs.encode(response.content, "base64")
            # Calculate MurmurHash3
            hash_value = mmh3.hash(favicon_b64)
            return str(hash_value)
    except (
        requests.exceptions.RequestException,
        requests.exceptions.Timeout,
        requests.exceptions.ConnectionError,
    ):
        pass
    return None


def get_technology_from_favicon_hash(favicon_hash: str) -> dict[str, Any] | None:
    """
    Map favicon hash to known technology.

    Args:
        favicon_hash: mmh3 hash string

    Returns:
        Technology information dict with name and confidence, or None

    Example:
        >>> get_technology_from_favicon_hash("-235440351")
        {'name': 'WordPress', 'confidence': 0.8, 'method': 'favicon_hash'}
    """
    # Known favicon hashes database
    # Source: Shodan, httpx, community research
    KNOWN_HASHES: dict[str, str] = {
        "-235440351": "WordPress",
        "81586312": "Jenkins",
        "708578229": "Atlassian Jira",
        "-1248544179": "Atlassian Confluence",
        "1708240621": "Apache Tomcat",
        "-257232473": "Fortinet FortiGate",
        "-1426884126": "Grafana",
        "1131645170": "UniFi Network Controller",
        "-1506567918": "SonarQube",
        "999357577": "Drupal",
        "-1691330359": "Magento",
        "1063456691": "Joomla",
        "-1588080585": "phpMyAdmin",
        "1335392827": "GitLab",
        "1506877664": "Nginx",
        "-88861654": "OwnCloud",
        "1721648852": "Nextcloud",
        "-1246928907": "cPanel",
        "1873852339": "Plesk",
        "-1194767827": "VMware vCenter",
        "372660252": "Cisco ASA",
        "-1902288867": "Microsoft IIS",
        "1635273628": "Adobe Experience Manager",
        "1099103700": "Atlassian Bitbucket",
        "-1541021706": "JBoss Application Server",
    }

    if favicon_hash in KNOWN_HASHES:
        tech_name = KNOWN_HASHES[favicon_hash]
        return {
            "name": tech_name,
            "confidence": 0.8,  # High confidence for favicon match
            "method": "favicon_hash",
            "hash": favicon_hash,
        }

    return None


def analyze_favicon(
    base_url: str, timeout: int = DEFAULT_TIMEOUT
) -> dict[str, Any] | None:
    """
    Complete favicon analysis: hash calculation and technology matching.

    Args:
        base_url: Base URL of target (e.g., "https://example.com")
        timeout: Request timeout in seconds

    Returns:
        Technology information if match found, None otherwise

    Example:
        >>> analyze_favicon("https://wordpress-site.com")
        {'name': 'WordPress', 'confidence': 0.8, 'method': 'favicon_hash', 'hash': '-235440351'}
    """
    favicon_url = f"{base_url.rstrip('/')}/favicon.ico"
    favicon_hash = calculate_favicon_hash(favicon_url, timeout)

    if favicon_hash:
        return get_technology_from_favicon_hash(favicon_hash)

    return None
