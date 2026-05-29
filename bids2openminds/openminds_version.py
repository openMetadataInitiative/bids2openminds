"""
Single source of truth for the active openMINDS schema version.

The bids2openminds converter can emit either openMINDS v4 or v5. The ``openminds``
package exposes each schema version under a separate import path
(``openminds.v4.core``, ``openminds.v5.core``, ...), so this module holds the
``core`` and ``controlled_terms`` submodules of the *currently selected* version.
The rest of the package references them through ``om.core`` / ``om.controlled_terms``
(``from . import openminds_version as om``) instead of hard-coding a version.

Always use attribute access (``om.core.X``), never ``from .openminds_version import core``,
so the reference reflects the version chosen at runtime by :func:`configure`.

It is named ``openminds_version`` rather than ``schema`` because both BIDS and
openMINDS use the word "schema"; this module is specifically about the openMINDS
package *version*.
"""

import importlib

SUPPORTED_VERSIONS = ("v4", "v5")
DEFAULT_VERSION = "v4"

#: The currently configured version string (one of SUPPORTED_VERSIONS).
version = None
#: The ``openminds.<version>.core`` submodule for the configured version.
core = None
#: The ``openminds.<version>.controlled_terms`` submodule for the configured version.
controlled_terms = None


def configure(requested_version=DEFAULT_VERSION):
    """Select the openMINDS schema version to use for the output.

    Rebinds the module-level :data:`core` and :data:`controlled_terms` to the
    submodules of the requested version and records the choice in :data:`version`.
    Call this before creating any openMINDS objects.

    Parameters:
    - requested_version (str): one of :data:`SUPPORTED_VERSIONS` ("v4" or "v5").

    Raises:
    - ValueError: if ``requested_version`` is not supported.
    """
    global version, core, controlled_terms
    if requested_version not in SUPPORTED_VERSIONS:
        raise ValueError(
            f"Unsupported openMINDS version {requested_version!r}; "
            f"choose one of {', '.join(SUPPORTED_VERSIONS)}."
        )
    core = importlib.import_module(f"openminds.{requested_version}.core")
    controlled_terms = importlib.import_module(
        f"openminds.{requested_version}.controlled_terms")
    version = requested_version


# Initialise to the default version on import so that simply importing the package
# (and the existing unit tests, which exercise functions directly) works without an
# explicit configure() call.
configure(DEFAULT_VERSION)
