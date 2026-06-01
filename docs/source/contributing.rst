Contributing
============

This document describes how to set up a development environment, our workflow conventions, and the standards we follow.

Development setup
-----------------

Clone the repository **with its submodules** (the BIDS example test corpus
lives in a submodule)::

    git clone --recurse-submodules https://github.com/openMetadataInitiative/bids2openminds.git
    cd bids2openminds
    pip install -e ".[test]"

Run the full test suite::

    pytest

If you cloned without ``--recurse-submodules``, initialise the submodule afterwards::

    git submodule update --init

Branching model
---------------

- All development happens on feature branches created from ``main``.
- Do not push commits directly to ``main``.
- Open a pull request to merge your branch into ``main``.
- At least one maintainer approval is required.
- CI must pass (tests on Linux/Windows/macOS, codespell, docs build) before merging.

Review process
--------------

- Keep pull requests focused; one logical change per PR makes review easier.
- Add an entry to ``CHANGES.rst`` in the *Unreleased* section (or under the next version)
  describing the change.
- Respond to review comments; squash fixup commits before the PR is merged if requested.

Versioning
----------

We follow `Semantic Versioning <https://semver.org/>`_ (``MAJOR.MINOR.PATCH``).
While the project is at ``0.x``, minor version bumps may introduce breaking API changes.
Once we reach ``1.0``, breaking changes will only occur in major releases.

Releasing a new version
-----------------------

See :doc:`maintenance` for the full release procedure.

Docstring standard
------------------

Use `Google-style docstrings
<https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings>`_
for all public functions and classes. A minimal example:

.. code-block:: python

    def my_function(param: str) -> dict:
        """One-line summary ending with a period.

        Parameters:
            param (str): Description of the parameter.

        Returns:
            dict: Description of the return value.

        Raises:
            ValueError: If param is empty.
        """

Communication
-------------

- **Bugs and feature requests**: `GitHub Issues <https://github.com/openMetadataInitiative/bids2openminds/issues>`_
- **Questions and general discussion**: `GitHub Discussions <https://github.com/openMetadataInitiative/bids2openminds/discussions>`_

Deprecation policy
------------------

When a feature is to be removed:

1. Add a ``DeprecationWarning`` in the current release pointing to the replacement.
2. Document the deprecation in ``CHANGES.rst``.
3. Remove the feature in the next minor (or major) release.

Code of Conduct
---------------

This project follows the `openMINDS Code of Conduct
<https://github.com/openMetadataInitiative/bids2openminds/blob/main/CODE_OF_CONDUCT.md>`_.
All participants are expected to uphold its standards.
