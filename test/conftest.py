import pytest

import bids2openminds.openminds_version as om


@pytest.fixture(autouse=True)
def reset_openminds_version():
    """Reset the global openMINDS version around every test.

    ``convert(..., openminds_version=...)`` (and tests calling
    ``om.configure``) mutate module-level state in
    ``bids2openminds.openminds_version``. Resetting to the default before and
    after each test keeps a test that selects a non-default version from leaking
    that choice into later tests, which call the conversion functions directly
    and expect the default (v4).
    """
    om.configure(om.DEFAULT_VERSION)
    yield
    om.configure(om.DEFAULT_VERSION)
