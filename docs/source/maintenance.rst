Maintenance
===========

This page is intended for project maintainers.

Cutting a release
-----------------

1. Decide on the new version number following `SemVer <https://semver.org/>`_
   (``MAJOR.MINOR.PATCH``).
2. Update ``version`` in ``pyproject.toml``.
3. Add a dated section to ``CHANGES.rst``::

       0.3.0 (YYYY-MM-DD)
       ------------------

       * Description of changes.

4. Commit the changes::

       git commit -m "Release 0.3.0"

5. Tag the commit::

       git tag v0.3.0

6. Push the commit and the tag::

       git push
       git push --tags

7. Build and upload to PyPI::

       pip install --upgrade build twine
       python -m build
       twine upload dist/*

Building the documentation locally
-----------------------------------

From the repository root::

    pip install sphinx sphinx-rtd-theme
    sphinx-build -W docs/source docs/_build/html

Then open ``docs/_build/html/index.html`` in a browser.

The documentation is also built automatically on every push to ``main`` by
`Read the Docs <https://bids2openminds.readthedocs.io/>`_.

Updating dependencies
---------------------

After upgrading a dependency (e.g. testing against a new ``ancpbids`` release):

1. Run the full test suite: ``pytest``.
2. If the new version introduces breaking changes, update the code accordingly
   and bump the lower-bound constraint in ``pyproject.toml``.
3. Update the ``CHANGES.rst`` entry for the release.
