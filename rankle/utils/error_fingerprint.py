"""
Error page fingerprinting for framework detection.

Triggers 404 errors and analyzes error pages to identify
web frameworks based on error message patterns and structure.
"""

import uuid
from typing import Any

import requests
from bs4 import BeautifulSoup

from config.settings import DEFAULT_TIMEOUT


def fingerprint_error_page(
    domain: str,
    timeout: int = DEFAULT_TIMEOUT,
    use_https: bool = True,
) -> list[dict[str, Any]]:
    """
    Analyze error page to detect web framework.

    Sends request to non-existent path to trigger 404/error response,
    then analyzes error page patterns to identify framework.

    Args:
        domain: Target domain
        timeout: Request timeout in seconds
        use_https: Use HTTPS (default) or HTTP

    Returns:
        List of detected technologies with confidence scores

    Example:
        >>> fingerprint_error_page("django-site.com")
        [{'name': 'Django', 'confidence': 0.9, 'evidence': 'error_page', 'detail': 'DisallowedHost error'}]
    """
    protocol = "https" if use_https else "http"
    # Generate unique path to ensure 404
    unique_path = f"rankle-probe-{uuid.uuid4()}"
    error_url = f"{protocol}://{domain}/{unique_path}"

    detected: list[dict[str, Any]] = []

    try:
        response = requests.get(
            error_url,
            timeout=timeout,
            allow_redirects=False,
            verify=True,
        )

        # Framework signatures in error pages
        error_signatures: dict[str, dict[str, Any]] = {
            "Django": {
                "patterns": [
                    "DisallowedHost",
                    "CSRF verification failed",
                    "Django version",
                    "ProgrammingError",
                    "django.core.exceptions",
                ],
                "confidence": 0.9,
                "category": "Web Framework",
            },
            "Laravel": {
                "patterns": [
                    "Whoops!",
                    "Laravel",
                    "Illuminate\\",
                    "RouteCollection.php",
                ],
                "confidence": 0.95,
                "category": "Web Framework",
            },
            "Spring Boot": {
                "patterns": [
                    "Whitelabel Error Page",
                    "This application has no explicit mapping",
                    '"timestamp":',
                    '"status":404',
                    "org.springframework",
                ],
                "confidence": 0.9,
                "category": "Web Framework",
            },
            "Express": {
                "patterns": [
                    "Cannot GET /",
                    "Cannot POST /",
                    "Error: Not Found",
                ],
                "confidence": 0.7,
                "category": "Web Framework",
            },
            "ASP.NET": {
                "patterns": [
                    "Server Error in '/' Application",
                    "ASP.NET",
                    "System.Web.HttpException",
                    "__VIEWSTATE",
                ],
                "confidence": 0.85,
                "category": "Web Framework",
            },
            "Ruby on Rails": {
                "patterns": [
                    "Routing Error",
                    "Rails.root:",
                    "ActionController::RoutingError",
                    "config/routes.rb",
                ],
                "confidence": 0.9,
                "category": "Web Framework",
            },
            "Flask": {
                "patterns": [
                    "werkzeug.exceptions.NotFound",
                    "404 Not Found",
                    "Werkzeug",
                ],
                "confidence": 0.7,
                "category": "Web Framework",
            },
            "FastAPI": {
                "patterns": [
                    '"detail":"Not Found"',
                    "FastAPI",
                    "/openapi.json",
                ],
                "confidence": 0.8,
                "category": "Web Framework",
            },
            "Phoenix": {
                "patterns": [
                    "Phoenix.Router.NoRouteError",
                    "no route found",
                    "Available routes:",
                ],
                "confidence": 0.9,
                "category": "Web Framework",
            },
            "Symfony": {
                "patterns": [
                    "Symfony\\",
                    "No route found",
                    "NotFoundHttpException",
                ],
                "confidence": 0.85,
                "category": "Web Framework",
            },
        }

        response_text = response.text.lower()
        original_text = response.text  # Keep original case for detail extraction

        # Check each framework signature
        for framework, sig_data in error_signatures.items():
            patterns = sig_data["patterns"]
            matched_patterns = [p for p in patterns if p.lower() in response_text]

            if matched_patterns:
                detected.append(
                    {
                        "name": framework,
                        "confidence": sig_data["confidence"],
                        "category": sig_data["category"],
                        "evidence": "error_page",
                        "detail": f"Error pattern: {matched_patterns[0][:50]}",
                        "matched_patterns": len(matched_patterns),
                    }
                )

        # Additional: Parse HTML structure for error page patterns
        try:
            soup = BeautifulSoup(original_text, "html.parser")

            # Check for specific HTML elements that indicate frameworks
            if soup.find("div", {"class": "exception_title"}) and not any(
                d["name"] == "Laravel" for d in detected
            ):
                detected.append(
                    {
                        "name": "Laravel",
                        "confidence": 0.8,
                        "category": "Web Framework",
                        "evidence": "error_page_html",
                        "detail": "Laravel exception page structure",
                    }
                )

            summary_div = soup.find("div", {"id": "summary"})
            if summary_div:
                title = soup.find("h1")
                if (
                    title
                    and "django" in title.text.lower()
                    and not any(d["name"] == "Django" for d in detected)
                ):
                    detected.append(
                        {
                            "name": "Django",
                            "confidence": 0.85,
                            "category": "Web Framework",
                            "evidence": "error_page_html",
                            "detail": "Django debug page structure",
                        }
                    )

        except (AttributeError, TypeError):
            pass  # HTML parsing failed, continue with text-based detection

    except requests.exceptions.Timeout:
        pass  # Timeout, no detection
    except requests.exceptions.ConnectionError:
        pass  # Connection error, no detection
    except requests.exceptions.RequestException:
        pass  # Other request errors

    return detected


def fingerprint_stack_trace(response_text: str) -> dict[str, Any] | None:
    """
    Extract framework information from stack traces in error responses.

    Args:
        response_text: HTTP response body containing potential stack trace

    Returns:
        Framework information if stack trace found, None otherwise

    Example:
        >>> fingerprint_stack_trace("at django.core.handlers.exception...")
        {'name': 'Django', 'confidence': 0.95, 'evidence': 'stack_trace'}
    """
    stack_patterns: dict[str, dict[str, Any]] = {
        "Django": {
            "patterns": ["django.core", "django.contrib", "django.db"],
            "confidence": 0.95,
        },
        "Laravel": {
            "patterns": ["Illuminate\\", "Laravel\\", "vendor/laravel"],
            "confidence": 0.95,
        },
        "Rails": {
            "patterns": ["actionpack", "activerecord", "railties"],
            "confidence": 0.95,
        },
        "Spring": {
            "patterns": ["org.springframework", "springframework.web"],
            "confidence": 0.95,
        },
        "Express": {
            "patterns": ["node_modules/express", "at Function.app.use"],
            "confidence": 0.9,
        },
    }

    for framework, data in stack_patterns.items():
        if any(pattern in response_text for pattern in data["patterns"]):
            return {
                "name": framework,
                "confidence": data["confidence"],
                "evidence": "stack_trace",
                "detail": "Stack trace analysis",
            }

    return None
