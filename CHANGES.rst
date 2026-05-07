Changelog
=========

0.2.0 (2026-05-07)
------------------

- Update to openMINDS v4
- Add content-type metadata to file objects
- Improved conversion report: now lists detected behavioral protocols and tasks

0.1.1 (2025-06-05)
------------------

- Pin to openMINDS v3 for stability
- Fix compatibility with updated BIDS example datasets
- Add Read the Docs documentation
- Add project logo

0.1.0 (2024-06-21)
------------------

Initial release. Features include:

- Convert BIDS datasets to openMINDS metadata collections (JSON-LD)
- CLI interface (``bids2openminds`` command)
- Support for subjects, authors/persons, file repositories, behavioral protocols, and dataset versions
- NIfTI version detection and content-type mapping
- Subject age validation and anomaly checking
- Conversion summary report
- Test suite using BIDS example datasets
- Cross-platform CI (Linux, Windows, macOS)
