#!/usr/bin/env python3
"""Add return type hints to methods missing them - Phase 3 automation."""

import re
import sys
from pathlib import Path


def add_return_types_to_file(filepath: Path) -> int:
    """Add return type hints to functions/methods missing them."""
    content = filepath.read_text()
    original = content
    fixes = 0

    # Pattern: def method_name(args): without return type
    # Add -> dict[str, Any]: for most module methods
    pattern = r'(\s+def\s+\w+\([^)]*\):(?!\s*->))'

    lines = content.split('\n')
    new_lines = []

    for i, line in enumerate(lines):
        if re.search(r'def\s+\w+\([^)]*\):\s*$', line):
            # Skip if already has type hint or docstring follows
            if i + 1 < len(lines):
                next_line = lines[i + 1].strip()
                if next_line.startswith('"""') or next_line.startswith("'''"):
                    # Has docstring, likely needs type hint before docstring
                    if ' -> ' not in line:
                        # Add generic return type for analyze/detect methods
                        if any(x in line for x in ['analyze', 'detect', 'fingerprint', 'audit', 'lookup']):
                            line = line.replace(':', ' -> dict[str, Any]:')
                            fixes += 1

        new_lines.append(line)

    new_content = '\n'.join(new_lines)

    if new_content != original:
        filepath.write_text(new_content)
        print(f"✓ {filepath.relative_to(Path.cwd())}: +{fixes} return types")

    return fixes


def main() -> None:
    """Add return types to rankle package."""
    rankle_dir = Path('rankle')
    total_fixes = 0

    for py_file in rankle_dir.rglob('*.py'):
        if '__pycache__' not in str(py_file):
            fixes = add_return_types_to_file(py_file)
            total_fixes += fixes

    print(f"\n✅ Total: +{total_fixes} return type hints added")


if __name__ == '__main__':
    main()
