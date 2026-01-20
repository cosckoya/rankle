"""
Utilities package for Rankle
"""

from .confidence import (
    calculate_confidence_score,
    group_evidence_by_type,
    meets_confidence_threshold,
)
from .cve_mapper import (
    assess_technology_risk,
    generate_cpe,
    get_high_risk_technologies,
    map_technology_to_cve_urls,
)
from .error_fingerprint import fingerprint_error_page, fingerprint_stack_trace
from .favicon_hash import (
    analyze_favicon,
    calculate_favicon_hash,
    get_technology_from_favicon_hash,
)
from .helpers import (
    format_bytes,
    format_duration,
    load_json_file,
    save_json_file,
    truncate_list,
)
from .js_extractor import (
    analyze_javascript,
    detect_frameworks_from_js,
    extract_endpoints_from_js,
    extract_js_files_from_html,
    extract_version_from_assets,
)
from .rate_limiter import RateLimiter, get_rate_limiter
from .validators import (
    extract_domain,
    sanitize_filename,
    validate_domain,
    validate_ip,
    validate_url,
)
from .wordpress_plugins import (
    analyze_wordpress,
    detect_wordpress_plugins,
    detect_wordpress_themes,
    is_wordpress_site,
)


__all__ = [
    # Confidence scoring
    "calculate_confidence_score",
    "group_evidence_by_type",
    "meets_confidence_threshold",
    # CVE mapping
    "assess_technology_risk",
    "generate_cpe",
    "get_high_risk_technologies",
    "map_technology_to_cve_urls",
    # Error fingerprinting
    "fingerprint_error_page",
    "fingerprint_stack_trace",
    # Favicon hashing
    "analyze_favicon",
    "calculate_favicon_hash",
    "get_technology_from_favicon_hash",
    # Helpers
    "extract_domain",
    "format_bytes",
    "format_duration",
    "load_json_file",
    "sanitize_filename",
    "save_json_file",
    "truncate_list",
    # JavaScript extraction
    "analyze_javascript",
    "detect_frameworks_from_js",
    "extract_endpoints_from_js",
    "extract_js_files_from_html",
    "extract_version_from_assets",
    # Rate limiting
    "RateLimiter",
    "get_rate_limiter",
    # Validators
    "validate_domain",
    "validate_ip",
    "validate_url",
    # WordPress detection
    "analyze_wordpress",
    "detect_wordpress_plugins",
    "detect_wordpress_themes",
    "is_wordpress_site",
]
