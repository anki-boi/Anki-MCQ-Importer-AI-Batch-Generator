#!/usr/bin/env python3
"""
Build script for Anki MCQ Importer - AI Batch Generator addon.
Creates .ankiaddon package for distribution.
"""

import os
import re
import zipfile
import json
from datetime import datetime

# Files to include in the package
INCLUDE_FILES = [
    '__init__.py',
    'config.json',
    'manifest.json',
    'README.md',
    'LICENSE'
]

# Optional files (include if they exist)
OPTIONAL_FILES = [
    'CHANGELOG.md',
    'icon.png'
]


REQUIRED_MANIFEST_KEYS = ("package", "name")
MANIFEST_KEY_TYPES = {
    "package": str,
    "name": str,
    "mod": (int, float),
    "conflicts": list,
    "min_point_version": (int, float),
    "max_point_version": (int, float),
    "branch_index": (int, float),
    "human_version": str,
    "homepage": str,
}


def load_manifest():
    """Load manifest.json as UTF-8 JSON."""
    with open('manifest.json', 'r', encoding='utf-8') as f:
        return json.load(f)


def validate_manifest():
    """Validate manifest.json against Anki's local .ankiaddon import requirements."""

    manifest = load_manifest()

    for key in REQUIRED_MANIFEST_KEYS:
        if not isinstance(manifest.get(key), str) or not manifest[key].strip():
            raise ValueError(f"manifest.json must contain a non-empty string '{key}' key")

    package = manifest["package"]
    if os.path.basename(package) != package or package in {".", ".."}:
        raise ValueError("manifest.json 'package' must be a plain folder name, not a path")
    if not re.fullmatch(r"[A-Za-z0-9_.-]+", package):
        raise ValueError(
            "manifest.json 'package' should contain only letters, numbers, dots, underscores, or hyphens"
        )

    for key, expected_type in MANIFEST_KEY_TYPES.items():
        if key in manifest and not isinstance(manifest[key], expected_type):
            raise ValueError(f"manifest.json '{key}' has the wrong type")

    if "conflicts" in manifest and not all(
        isinstance(item, str) for item in manifest["conflicts"]
    ):
        raise ValueError("manifest.json 'conflicts' must be a list of strings")

    return manifest


def get_version():
    """Extract version from manifest.json"""
    manifest = load_manifest()
    return manifest.get('human_version', manifest.get('version', '0.0.0'))


def create_package():
    """Create .ankiaddon package"""

    manifest = validate_manifest()
    version = get_version()
    output_filename = f'anki_mcq_importer_ai_batch_generator_v{version}.ankiaddon'

    print(f"Building {manifest['name']} v{version}")
    print(f"Output: {output_filename}")
    print("-" * 50)

    # Check required files
    missing = []
    for filename in INCLUDE_FILES:
        if not os.path.exists(filename):
            missing.append(filename)

    if missing:
        print("ERROR: Missing required files:")
        for f in missing:
            print(f"  - {f}")
        return False

    # Create zip file
    with zipfile.ZipFile(output_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:

        # Add required files
        for filename in INCLUDE_FILES:
            print(f"Adding: {filename}")
            zipf.write(filename)

        # Add optional files if they exist
        for filename in OPTIONAL_FILES:
            if os.path.exists(filename):
                print(f"Adding: {filename} (optional)")
                zipf.write(filename)
            else:
                print(f"Skipping: {filename} (not found)")

    # Verify package
    file_size = os.path.getsize(output_filename)
    print("-" * 50)
    print("✓ Package created successfully!")
    print(f"  File: {output_filename}")
    print(f"  Size: {file_size:,} bytes ({file_size / 1024:.1f} KB)")

    # List contents
    print("\nPackage contents:")
    with zipfile.ZipFile(output_filename, 'r') as zipf:
        for info in zipf.filelist:
            print(f"  {info.filename} ({info.file_size} bytes)")

    return True


def create_release_notes():
    """Create release notes template"""

    version = get_version()
    date = datetime.now().strftime('%Y-%m-%d')

    notes = f"""# Release Notes - v{version}

**Release Date**: {date}

## What's New

- Feature 1
- Feature 2
- Feature 3

## Improvements

- Improvement 1
- Improvement 2

## Bug Fixes

- Fix 1
- Fix 2

## Installation

### From AnkiWeb
1. Open Anki
2. Go to Tools → Add-ons → Get Add-ons
3. Enter code: [ANKIWEB_ID]

### Manual Installation
1. Download `anki_mcq_importer_ai_batch_generator_v{version}.ankiaddon`
2. In Anki, go to Tools → Add-ons → Install from file
3. Select the downloaded file
4. Restart Anki

## Requirements

- Anki 2.1.45 or higher
- Internet connection for AI processing
- Google Gemini API key (free)

## Known Issues

- None

## Upgrade Notes

If upgrading from previous version:
- Your settings will be preserved
- API key does not need to be re-entered
- Note types are compatible

## Support

- GitHub Issues: https://github.com/anki-boi/True-Anki-MCQ-Note-Template/issues
- Documentation: https://github.com/anki-boi/True-Anki-MCQ-Note-Template
"""

    with open(f'RELEASE_NOTES_v{version}.md', 'w', encoding='utf-8') as f:
        f.write(notes)

    print(f"\n✓ Created: RELEASE_NOTES_v{version}.md")
    print("  Edit this file before publishing release")


if __name__ == '__main__':
    print("=" * 50)
    print("Anki MCQ Importer - AI Batch Generator Build Script")
    print("=" * 50)
    print()

    if create_package():
        print()
        create_release_notes()
        print()
        print("=" * 50)
        print("Build Complete!")
        print("=" * 50)
        print("\nNext steps:")
        print("1. Test the .ankiaddon file in Anki")
        print("2. Edit the release notes")
        print("3. Create GitHub release")
        print("4. Upload to AnkiWeb")
    else:
        print()
        print("=" * 50)
        print("Build Failed!")
        print("=" * 50)
