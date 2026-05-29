# Contributing to bids2openminds

Full contribution guidelines are in the [documentation](https://bids2openminds.readthedocs.io/en/latest/contributing.html).

## Quick start

```bash
git clone --recurse-submodules https://github.com/openMetadataInitiative/bids2openminds.git
cd bids2openminds
pip install -e ".[test]"
pytest
```

## Key points

- Feature branches off `main`; PR required to merge; CI must pass
- Google-style docstrings for all public functions
- Deprecations get a `DeprecationWarning` for one release before removal
- Contributors are expected to abide by the [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)
