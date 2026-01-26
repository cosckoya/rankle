"""
WordPress plugin detection utilities.

Detects WordPress plugins through passive reconnaissance of
HTML content, analyzing wp-content/plugins/ paths and plugin assets.
"""

import re
from typing import Any


def detect_wordpress_plugins(html: str) -> list[dict[str, Any]]:
    """
    Detect WordPress plugins from HTML content.

    Analyzes HTML for WordPress plugin paths (/wp-content/plugins/plugin-slug/)
    and extracts unique plugin identifiers.

    Args:
        html: HTML content from WordPress site

    Returns:
        List of detected plugins with slugs and confidence

    Example:
        >>> html = '<script src="/wp-content/plugins/contact-form-7/script.js"></script>'
        >>> detect_wordpress_plugins(html)
        [{'name': 'contact-form-7', 'type': 'wordpress-plugin', 'confidence': 0.8}]
    """
    plugins: list[dict[str, Any]] = []

    # Pattern: /wp-content/plugins/plugin-slug/
    plugin_pattern = r'/wp-content/plugins/([^/\s"\'<>]+)/'
    matches = re.findall(plugin_pattern, html, re.IGNORECASE)

    seen_plugins: set[str] = set()

    for plugin_slug in matches:
        if plugin_slug not in seen_plugins:
            seen_plugins.add(plugin_slug)

            # Map known plugins to friendly names
            friendly_name = _get_plugin_friendly_name(plugin_slug)

            plugins.append(
                {
                    "name": friendly_name,
                    "slug": plugin_slug,
                    "type": "wordpress-plugin",
                    "category": "WordPress Plugin",
                    "confidence": 0.8,
                    "evidence": "wp_content_path",
                }
            )

    return plugins


def _get_plugin_friendly_name(slug: str) -> str:
    """
    Convert plugin slug to friendly name.

    Maps common plugin slugs to their marketing names.

    Args:
        slug: Plugin directory slug

    Returns:
        Friendly plugin name or slug if unknown

    Example:
        >>> _get_plugin_friendly_name("contact-form-7")
        'Contact Form 7'
    """
    # Map of known plugin slugs to friendly names
    known_plugins: dict[str, str] = {
        "contact-form-7": "Contact Form 7",
        "woocommerce": "WooCommerce",
        "yoast-seo": "Yoast SEO",
        "wordpress-seo": "Yoast SEO",
        "akismet": "Akismet Anti-Spam",
        "jetpack": "Jetpack",
        "elementor": "Elementor",
        "advanced-custom-fields": "Advanced Custom Fields",
        "wordfence": "Wordfence Security",
        "wpforms-lite": "WPForms Lite",
        "classic-editor": "Classic Editor",
        "wp-super-cache": "WP Super Cache",
        "w3-total-cache": "W3 Total Cache",
        "all-in-one-seo-pack": "All in One SEO",
        "google-analytics-for-wordpress": "MonsterInsights",
        "duplicate-post": "Duplicate Post",
        "wp-optimize": "WP-Optimize",
        "updraftplus": "UpdraftPlus",
        "wp-mail-smtp": "WP Mail SMTP",
        "smush": "Smush",
        "redirection": "Redirection",
        "mailchimp-for-wp": "MC4WP: Mailchimp",
        "really-simple-ssl": "Really Simple SSL",
        "limit-login-attempts-reloaded": "Limit Login Attempts",
        "wp-fastest-cache": "WP Fastest Cache",
        "autoptimize": "Autoptimize",
        "siteorigin-panels": "Page Builder by SiteOrigin",
        "beaver-builder-lite-version": "Beaver Builder",
        "wpbakery": "WPBakery Page Builder",
        "visual-composer-starter": "Visual Composer",
        "gravityforms": "Gravity Forms",
        "ninja-forms": "Ninja Forms",
        "wp-rocket": "WP Rocket",
        "wp-smushit": "Smush",
        "antispam-bee": "Antispam Bee",
        "regenerate-thumbnails": "Regenerate Thumbnails",
        "broken-link-checker": "Broken Link Checker",
        "wp-security-audit-log": "WP Activity Log",
        "insert-headers-and-footers": "Insert Headers and Footers",
        "popup-maker": "Popup Maker",
        "custom-post-type-ui": "Custom Post Type UI",
        "tinymce-advanced": "TinyMCE Advanced",
        "disable-comments": "Disable Comments",
        "user-role-editor": "User Role Editor",
        "enable-media-replace": "Enable Media Replace",
        "post-smtp": "Post SMTP",
        "google-site-kit": "Site Kit by Google",
        "loco-translate": "Loco Translate",
        "polylang": "Polylang",
        "wpml": "WPML Multilingual CMS",
        "weglot": "Weglot Translate",
        "translatepress-multilingual": "TranslatePress",
        "amp": "AMP",
        "wp-statistics": "WP Statistics",
    }

    return known_plugins.get(slug, slug.replace("-", " ").title())


def detect_wordpress_themes(html: str) -> list[dict[str, Any]]:
    """
    Detect WordPress themes from HTML content.

    Analyzes HTML for WordPress theme paths (/wp-content/themes/theme-slug/)
    and extracts theme identifiers.

    Args:
        html: HTML content from WordPress site

    Returns:
        List of detected themes

    Example:
        >>> html = '<link href="/wp-content/themes/twentytwentythree/style.css">'
        >>> detect_wordpress_themes(html)
        [{'name': 'Twenty Twenty-Three', 'slug': 'twentytwentythree', 'type': 'wordpress-theme'}]
    """
    themes: list[dict[str, Any]] = []

    # Pattern: /wp-content/themes/theme-slug/
    theme_pattern = r'/wp-content/themes/([^/\s"\'<>]+)/'
    matches = re.findall(theme_pattern, html, re.IGNORECASE)

    seen_themes: set[str] = set()

    for theme_slug in matches:
        if theme_slug not in seen_themes:
            seen_themes.add(theme_slug)

            # Map known themes
            friendly_name = _get_theme_friendly_name(theme_slug)

            themes.append(
                {
                    "name": friendly_name,
                    "slug": theme_slug,
                    "type": "wordpress-theme",
                    "category": "WordPress Theme",
                    "confidence": 0.8,
                    "evidence": "wp_content_path",
                }
            )

    return themes


def _get_theme_friendly_name(slug: str) -> str:
    """
    Convert theme slug to friendly name.

    Args:
        slug: Theme directory slug

    Returns:
        Friendly theme name or slug if unknown
    """
    known_themes: dict[str, str] = {
        "twentytwentyfour": "Twenty Twenty-Four",
        "twentytwentythree": "Twenty Twenty-Three",
        "twentytwentytwo": "Twenty Twenty-Two",
        "twentytwentyone": "Twenty Twenty-One",
        "twentytwenty": "Twenty Twenty",
        "twentynineteen": "Twenty Nineteen",
        "astra": "Astra",
        "oceanwp": "OceanWP",
        "generatepress": "GeneratePress",
        "neve": "Neve",
        "kadence": "Kadence",
        "blocksy": "Blocksy",
        "hello-elementor": "Hello Elementor",
        "divi": "Divi",
        "avada": "Avada",
        "enfold": "Enfold",
        "flatsome": "Flatsome",
        "storefront": "Storefront",
        "sydney": "Sydney",
        "zakra": "Zakra",
        "hestia": "Hestia",
    }

    return known_themes.get(slug, slug.replace("-", " ").title())


def is_wordpress_site(html: str, headers: dict[str, str]) -> bool:
    """
    Check if site is running WordPress.

    Args:
        html: HTML content
        headers: HTTP response headers

    Returns:
        True if WordPress detected, False otherwise

    Example:
        >>> is_wordpress_site('<meta name="generator" content="WordPress 6.4">', {})
        True
    """
    # Check meta generator tag
    if re.search(r'<meta[^>]*name=["\']generator["\'][^>]*content=["\']WordPress', html, re.IGNORECASE):
        return True

    # Check wp-content paths
    if re.search(r'/wp-content/', html, re.IGNORECASE):
        return True

    # Check wp-includes paths
    if re.search(r'/wp-includes/', html, re.IGNORECASE):
        return True

    # Check X-Powered-By header
    x_powered_by = headers.get("X-Powered-By", "").lower()
    if "wordpress" in x_powered_by:
        return True

    # Check for wp-json REST API
    if "/wp-json/" in html:
        return True

    return False


def analyze_wordpress(html: str, headers: dict[str, str]) -> dict[str, Any]:
    """
    Complete WordPress analysis: detection, plugins, themes.

    Args:
        html: HTML content
        headers: HTTP response headers

    Returns:
        Dictionary containing WordPress detection results

    Example:
        >>> analyze_wordpress(html, headers)
        {
            'is_wordpress': True,
            'plugins': [{'name': 'Contact Form 7', ...}],
            'themes': [{'name': 'Astra', ...}],
            'plugin_count': 5,
            'theme_count': 1
        }
    """
    is_wp = is_wordpress_site(html, headers)

    if not is_wp:
        return {
            "is_wordpress": False,
            "plugins": [],
            "themes": [],
            "plugin_count": 0,
            "theme_count": 0,
        }

    plugins = detect_wordpress_plugins(html)
    themes = detect_wordpress_themes(html)

    return {
        "is_wordpress": True,
        "plugins": plugins,
        "themes": themes,
        "plugin_count": len(plugins),
        "theme_count": len(themes),
    }
