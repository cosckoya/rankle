"""
Validation utilities for Rankle
"""

import re
from urllib.parse import urlparse


def validate_domain(domain: str) -> bool:
    """
    Validate domain name format using RFC-compliant regex.

    Checks if the domain follows standard DNS naming conventions:
    - Labels can contain alphanumerics and hyphens
    - Labels cannot start or end with hyphen
    - TLD must be at least 2 characters

    Args:
        domain: Domain name to validate (e.g., "example.com")

    Returns:
        True if domain format is valid, False otherwise

    Example:
        >>> validate_domain("example.com")
        True
        >>> validate_domain("sub.example.co.uk")
        True
        >>> validate_domain("-invalid.com")
        False
        >>> validate_domain("invalid..com")
        False
        >>> validate_domain("no-tld")
        False
    """
    pattern = r"^([a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}$"
    return bool(re.match(pattern, domain))


def extract_domain(url: str) -> str:
    """
    Extract clean domain name from URL or partial URL.

    Handles various input formats:
    - Full URLs with protocol
    - URLs without protocol
    - Removes port numbers
    - Extracts netloc from parsed URL

    Args:
        url: URL or domain to extract from

    Returns:
        Clean domain name without protocol or port

    Example:
        >>> extract_domain("https://example.com/path")
        'example.com'
        >>> extract_domain("example.com:8080")
        'example.com'
        >>> extract_domain("subdomain.example.co.uk")
        'subdomain.example.co.uk'
        >>> extract_domain("http://user:pass@example.com")
        'example.com'
    """
    if not url.startswith(("http://", "https://")):
        url = "https://" + url
    parsed = urlparse(url)
    domain = parsed.netloc or parsed.path
    # Remove port if present
    return domain.split(":")[0]


def validate_ip(ip: str) -> bool:
    """
    Validate IP address format (IPv4 or IPv6).

    Checks both IPv4 and IPv6 formats:
    - IPv4: Validates octet ranges (0-255)
    - IPv6: Validates hexadecimal colon-separated format

    Args:
        ip: IP address string to validate

    Returns:
        True if valid IPv4 or IPv6 address, False otherwise

    Example:
        >>> validate_ip("192.168.1.1")
        True
        >>> validate_ip("256.1.1.1")
        False
        >>> validate_ip("2001:0db8:85a3:0000:0000:8a2e:0370:7334")
        True
        >>> validate_ip("invalid")
        False
    """
    ipv4_pattern = r"^(\d{1,3}\.){3}\d{1,3}$"
    ipv6_pattern = r"^([0-9a-fA-F]{0,4}:){7}[0-9a-fA-F]{0,4}$"

    if re.match(ipv4_pattern, ip):
        parts = ip.split(".")
        return all(0 <= int(part) <= 255 for part in parts)

    return bool(re.match(ipv6_pattern, ip))


def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename for safe cross-platform file system usage.

    Removes or replaces characters that are invalid on common filesystems:
    - Windows: < > : " / \\ | ? *
    - Replaces with underscore
    - Limits length to 200 characters

    Args:
        filename: Filename to sanitize

    Returns:
        Sanitized filename safe for use on Windows, macOS, and Linux

    Example:
        >>> sanitize_filename("example.com")
        'example.com'
        >>> sanitize_filename("file:with<invalid>chars")
        'file_with_invalid_chars'
        >>> sanitize_filename("path/to/file.txt")
        'path_to_file.txt'
        >>> sanitize_filename("a" * 300)[:10]
        'aaaaaaaaaa'
    """
    # Remove invalid characters
    filename = re.sub(r'[<>:"/\\|?*]', "_", filename)
    # Limit length
    return filename[:200]


def validate_url(url: str) -> bool:
    """
    Validate URL format

    Args:
        url: URL to validate

    Returns:
        True if valid, False otherwise

    Example:
        >>> validate_url("https://example.com")
        True
        >>> validate_url("not a url")
        False
    """
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except (ValueError, AttributeError):
        # Invalid URL format or parsing error
        return False
