#!/usr/bin/env python3
"""
Test script for enhanced technology detection capabilities.

Demonstrates new features:
- Wappalyzer integration (3000+ technologies)
- Favicon hashing
- Error page fingerprinting
- JavaScript endpoint extraction
- WordPress plugin detection
- CVE mapping
"""

import json

import requests

from rankle.detectors.technology import TechnologyDetector


def test_enhanced_detection(domain: str) -> None:
    """
    Test enhanced detection on a domain.

    Args:
        domain: Target domain (e.g., "example.com")
    """
    print("=" * 80)
    print(f"🔬 Testing Enhanced Technology Detection: {domain}")
    print("=" * 80)

    # Fetch page
    url = f"https://{domain}"
    print(f"\n[1/3] Fetching {url}...")

    try:
        response = requests.get(url, timeout=15, allow_redirects=True)
        print(f"   Status: {response.status_code}")

        # Extract data
        headers = dict(response.headers)
        cookies = [cookie.name for cookie in response.cookies]
        body = response.text

        # Run enhanced detection
        print("\n[2/3] Running enhanced technology detection...")
        detector = TechnologyDetector(domain)

        results = detector.detect_enhanced(
            headers=headers,
            cookies=cookies,
            body=body,
            base_url=url,
        )

        # Display results
        print("\n[3/3] Results:")
        print("=" * 80)

        if results.get("detected"):
            technologies = results["technologies"]
            print(f"\n✅ Detected {len(technologies)} technologies:\n")

            for i, tech in enumerate(technologies[:15], 1):  # Top 15
                confidence_pct = int(tech["confidence"] * 100)

                # Confidence indicator
                if confidence_pct >= 80:
                    indicator = "🟢"
                elif confidence_pct >= 60:
                    indicator = "🟡"
                else:
                    indicator = "🟠"

                version_str = f" v{tech['version']}" if tech.get("version") else ""
                category_str = f" [{tech['category']}]" if tech.get("category") else ""

                print(
                    f"  {i:2}. {indicator} {tech['name']}{version_str} ({confidence_pct}%){category_str}"
                )

                # Show evidence if verbose
                evidence = tech.get("evidence", [])
                if isinstance(evidence, list) and len(evidence) > 0:
                    for ev in evidence[:2]:  # First 2 pieces of evidence
                        if isinstance(ev, dict):
                            ev_type = ev.get("type", "unknown")
                            ev_detail = ev.get("detail", "detected")
                            if isinstance(ev_detail, str):
                                print(f"       → {ev_type}: {ev_detail[:60]}")

            # WordPress details
            if "wordpress" in results:
                wp = results["wordpress"]
                if wp["plugin_count"] > 0:
                    print(f"\n📦 WordPress Plugins ({wp['plugin_count']}):")
                    for plugin in wp["plugins"][:5]:
                        print(f"   - {plugin['name']}")

                if wp["theme_count"] > 0:
                    print(f"\n🎨 WordPress Themes ({wp['theme_count']}):")
                    for theme in wp["themes"]:
                        print(f"   - {theme['name']}")

            # API endpoints
            if "api_endpoints" in results:
                endpoints = results["api_endpoints"]
                if endpoints:
                    print(f"\n🔗 API Endpoints Found ({len(endpoints)}):")
                    for endpoint in endpoints[:10]:
                        print(f"   - {endpoint}")

            # Asset versions
            if "asset_versions" in results:
                versions = results["asset_versions"]
                if versions:
                    print("\n📦 Version Detection from Assets:")
                    for tech, version in versions.items():
                        print(f"   - {tech}: {version}")

            # CVE mappings
            if "cve_mappings" in results:
                print("\n🔐 CVE Search URLs (Top 5 Technologies):")
                for cve_info in results["cve_mappings"][:5]:
                    tech_name = cve_info["technology"]
                    version = cve_info.get("version")
                    version_str = f" {version}" if version else ""
                    print(f"\n   {tech_name}{version_str}:")
                    print(f"   - NIST NVD: {cve_info['cve_search_urls']['nist_nvd']}")
                    if version:
                        print(f"   - CPE: {cve_info['cpe']}")

        else:
            print("   No technologies detected")

        print("\n" + "=" * 80)
        print("✅ Enhanced detection complete!")
        print("=" * 80)

        # Save results
        output_file = f"{domain.replace('.', '_')}_enhanced_detection.json"
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        print(f"\n💾 Full results saved to: {output_file}")

    except requests.exceptions.RequestException as e:
        print(f"❌ Error fetching {url}: {e}")
    except Exception as e:
        print(f"❌ Error during detection: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        domain = sys.argv[1]
    else:
        domain = "example.com"  # Default test domain

    test_enhanced_detection(domain)
