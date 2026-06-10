# Changelog

All notable changes to this project are documented in this file.

## [4.2.1] - 2026-06-10

### Fixed
- Simplified `manifest.json` to Anki-supported add-on metadata so local `.ankiaddon` imports do not fail manifest validation.
- Added build-time manifest validation before packaging release archives.

## [4.2.0] - 2026-02-18

### Added
- Support for Cloze Deletion note workflows through profile-aware parsing and field mapping.
- Support for Basic (Front/Back) note workflows through profile-aware parsing and field mapping.
- Support for maintaining multiple profiles for each prompt format (MCQ, Cloze, and Basic).

### Notes
- This release emphasizes profile flexibility for users who want separate prompt variants per format.
