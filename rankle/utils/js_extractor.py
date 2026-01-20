"""
JavaScript endpoint extraction and analysis.

Implements LinkFinder-style regex patterns to extract API endpoints,
framework routes, and technology signatures from JavaScript files.
"""

import re
from typing import Any
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup

from config.settings import DEFAULT_TIMEOUT


def extract_js_files_from_html(html: str, base_url: str) -> list[str]:
    """
    Extract all JavaScript file URLs from HTML.

    Args:
        html: HTML content
        base_url: Base URL for resolving relative paths

    Returns:
        List of absolute JavaScript file URLs

    Example:
        >>> extract_js_files_from_html('<script src="/app.js"></script>', 'https://example.com')
        ['https://example.com/app.js']
    """
    soup = BeautifulSoup(html, "html.parser")
    js_files: list[str] = []

    # Find all script tags with src attribute
    for script in soup.find_all("script", src=True):
        src = script.get("src", "")
        if src:
            # Convert relative URLs to absolute
            absolute_url = urljoin(base_url, src)
            # Only include .js files or common bundle patterns
            if ".js" in absolute_url or "/js/" in absolute_url:
                js_files.append(absolute_url)

    return js_files


def extract_endpoints_from_js(js_content: str) -> list[str]:
    """
    Extract API endpoints and routes from JavaScript content.

    Uses LinkFinder-style regex patterns to identify:
    - Full URLs (https://api.example.com/*)
    - Absolute paths (/api/v1/*)
    - Relative paths (../api/*)
    - API-like strings

    Args:
        js_content: JavaScript file content

    Returns:
        List of extracted endpoints (deduplicated)

    Example:
        >>> extract_endpoints_from_js('fetch("/api/users")')
        ['/api/users']
    """
    endpoints: set[str] = set()

    # LinkFinder regex patterns (4 patterns for different endpoint types)
    patterns = [
        # Pattern 1: Full URLs (http/https)
        r'["\']((https?:)?//[^"\']+)["\']',
        # Pattern 2: Absolute paths starting with /
        r'["\']([/][^"\']*)["\']',
        # Pattern 3: Relative paths with ../
        r'["\'](\.\./[^"\']+)["\']',
        # Pattern 4: Simple relative paths
        r'["\']([a-zA-Z0-9_\-/]+\.(?:php|asp|aspx|jsp|json|xml|do|action))["\']',
    ]

    for pattern in patterns:
        matches = re.findall(pattern, js_content)
        for match in matches:
            # Handle tuples from regex groups
            endpoint = match[0] if isinstance(match, tuple) else match
            if endpoint:
                endpoints.add(endpoint)

    # Filter for API-like patterns
    api_patterns = ["/api/", "/graphql", "/rest/", "/v1/", "/v2/", "/json/", "/ajax/"]
    api_endpoints = [
        e for e in endpoints if any(pattern in e.lower() for pattern in api_patterns)
    ]

    return sorted(list(set(api_endpoints)))[:50]  # Limit to 50 endpoints


def detect_frameworks_from_js(js_content: str) -> list[dict[str, Any]]:
    """
    Detect JavaScript frameworks and libraries from code patterns.

    Args:
        js_content: JavaScript file content

    Returns:
        List of detected frameworks with confidence scores

    Example:
        >>> detect_frameworks_from_js('import React from "react"')
        [{'name': 'React', 'confidence': 0.9, 'evidence': 'import_statement'}]
    """
    detected: list[dict[str, Any]] = []

    # Framework detection patterns
    framework_patterns: dict[str, dict[str, Any]] = {
        "React": {
            "patterns": [
                r"from ['\"]react['\"]",
                r"require\(['\"]react['\"]\)",
                r"React\.Component",
                r"React\.createElement",
                r"\.jsx",
            ],
            "confidence": 0.9,
        },
        "Vue": {
            "patterns": [
                r"from ['\"]vue['\"]",
                r"require\(['\"]vue['\"]\)",
                r"Vue\.component",
                r"new Vue\(",
                r"\.vue",
            ],
            "confidence": 0.9,
        },
        "Angular": {
            "patterns": [
                r"from ['\"]\@angular",
                r"angular\.module",
                r"ng-[a-z]+",
                r"\.ngModule",
            ],
            "confidence": 0.9,
        },
        "Next.js": {
            "patterns": [
                r"from ['\"]next/",
                r"/_next/static/",
                r"__NEXT_DATA__",
                r"next/router",
            ],
            "confidence": 0.95,
        },
        "Nuxt.js": {
            "patterns": [
                r"from ['\"]nuxt",
                r"/_nuxt/",
                r"__NUXT__",
                r"\$nuxt",
            ],
            "confidence": 0.95,
        },
        "Svelte": {
            "patterns": [
                r"from ['\"]svelte",
                r"\.svelte",
                r"createComponent",
            ],
            "confidence": 0.9,
        },
        "jQuery": {
            "patterns": [
                r"jQuery\(",
                r"\$\(",
                r"jquery\.min\.js",
            ],
            "confidence": 0.85,
        },
        "Webpack": {
            "patterns": [
                r"webpackJsonp",
                r"__webpack_require__",
                r"\.chunk\.js",
            ],
            "confidence": 0.8,
        },
        "Vite": {
            "patterns": [
                r"from ['\"]vite",
                r"/@vite/",
                r"vite\.config",
            ],
            "confidence": 0.85,
        },
    }

    for framework, data in framework_patterns.items():
        for pattern in data["patterns"]:
            if re.search(pattern, js_content, re.IGNORECASE):
                detected.append(
                    {
                        "name": framework,
                        "confidence": data["confidence"],
                        "evidence": "js_pattern",
                        "category": "JavaScript Framework",
                    }
                )
                break  # Only add once per framework

    return detected


def analyze_javascript(
    base_url: str,
    html: str,
    max_files: int = 5,
    timeout: int = DEFAULT_TIMEOUT,
) -> dict[str, Any]:
    """
    Complete JavaScript analysis: extract files, find endpoints, detect frameworks.

    Args:
        base_url: Base URL of target
        html: HTML content containing script tags
        max_files: Maximum number of JS files to analyze
        timeout: Request timeout for fetching JS files

    Returns:
        Dictionary containing endpoints and detected frameworks

    Example:
        >>> analyze_javascript('https://example.com', html_content)
        {
            'endpoints': ['/api/users', '/api/posts'],
            'frameworks': [{'name': 'React', 'confidence': 0.9}],
            'analyzed_files': 3
        }
    """
    js_files = extract_js_files_from_html(html, base_url)[:max_files]

    all_endpoints: set[str] = set()
    all_frameworks: list[dict[str, Any]] = []
    analyzed_count = 0

    for js_url in js_files:
        try:
            response = requests.get(js_url, timeout=timeout)
            if response.status_code == 200:
                js_content = response.text

                # Extract endpoints
                endpoints = extract_endpoints_from_js(js_content)
                all_endpoints.update(endpoints)

                # Detect frameworks
                frameworks = detect_frameworks_from_js(js_content)
                all_frameworks.extend(frameworks)

                analyzed_count += 1

        except (
            requests.exceptions.RequestException,
            requests.exceptions.Timeout,
        ):
            continue  # Skip failed JS file fetches

    # Deduplicate frameworks
    seen_frameworks: set[str] = set()
    unique_frameworks: list[dict[str, Any]] = []
    for fw in all_frameworks:
        if fw["name"] not in seen_frameworks:
            seen_frameworks.add(fw["name"])
            unique_frameworks.append(fw)

    return {
        "endpoints": sorted(list(all_endpoints))[:30],  # Top 30 endpoints
        "frameworks": unique_frameworks,
        "analyzed_files": analyzed_count,
        "total_files_found": len(js_files),
    }


def extract_version_from_assets(html: str) -> dict[str, str]:
    """
    Extract framework versions from asset filenames in HTML.

    Parses script/link tags to find versioned assets like:
    - react.18.2.0.min.js
    - vue@3.2.45/dist/vue.js
    - jquery-3.6.0.min.js

    Args:
        html: HTML content

    Returns:
        Dictionary mapping framework name to version

    Example:
        >>> extract_version_from_assets('<script src="react.18.2.0.js"></script>')
        {'React': '18.2.0'}
    """
    versions: dict[str, str] = {}

    # Version extraction patterns for popular frameworks
    version_patterns: dict[str, str] = {
        "React": r"react[.-]?v?(\d+\.\d+\.\d+)",
        "Vue": r"vue[@.-]?v?(\d+\.\d+\.\d+)",
        "jQuery": r"jquery[.-]?v?(\d+\.\d+\.?\d*)",
        "Bootstrap": r"bootstrap[.-]?v?(\d+\.\d+\.\d+)",
        "Angular": r"angular[.-]?v?(\d+\.\d+\.\d+)",
        "Lodash": r"lodash[.-]?v?(\d+\.\d+\.\d+)",
        "Moment.js": r"moment[.-]?v?(\d+\.\d+\.\d+)",
        "D3.js": r"d3[.-]?v?(\d+\.\d+\.\d+)",
    }

    for framework, pattern in version_patterns.items():
        match = re.search(pattern, html, re.IGNORECASE)
        if match:
            versions[framework] = match.group(1)

    return versions
