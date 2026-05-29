Architecture
============

bids2openminds converts `BIDS <https://bids.neuroimaging.io/>`_ neuroimaging datasets into
`openMINDS <https://openminds-documentation.readthedocs.io/>`_ metadata collections
serialised as JSON-LD.

Conversion pipeline
-------------------

The top-level entry point is :func:`bids2openminds.converter.convert`.
It orchestrates the following steps:

1. Validate that the input path is a directory and load a BIDS layout via
   `ancpBIDS <https://github.com/ANCPLabOldenburg/ancp-bids>`_.
2. Flatten the layout into a Pandas ``DataFrame`` (one row per file) via the
   ``layout_to_df()`` shim in ``converter.py``.
3. Call functions in ``main.py`` to create typed openMINDS objects:

   * Subjects and their biological states
   * Persons (authors / contributors)
   * Behavioural protocols (tasks)
   * File bundles and individual files
   * A ``DatasetVersion`` and its parent ``Dataset``

4. Validate the resulting ``openminds.Collection`` against the openMINDS schema.
5. Optionally serialise to JSON-LD (single file or one file per object).
6. Print a human-readable conversion report.

Module descriptions
-------------------

``converter.py``
~~~~~~~~~~~~~~~~

CLI entry point (Click command) and the ``convert()`` function that orchestrates
the pipeline.  Also contains ``layout_to_df()``, a shim that translates the
ancpBIDS object model into a flat Pandas DataFrame so the rest of the code can
query files without depending directly on the ancpBIDS API.

``main.py``
~~~~~~~~~~~

All object-creation functions that map BIDS concepts to openMINDS schema objects:
``create_subjects()``, ``create_persons()``, ``create_behavioral_protocol()``,
``create_file()``, ``create_dataset_version()``, and ``create_dataset()``.

``mapping.py``
~~~~~~~~~~~~~~

Controlled-vocabulary dictionaries that translate BIDS terms (file suffixes,
acquisition labels, species identifiers, sex codes, handedness codes) into
openMINDS ``ControlledTerm`` instances.  Entries that do not yet have a
corresponding openMINDS instance are marked ``None`` with a ``# TODO`` comment.

``utility.py``
~~~~~~~~~~~~~~

Helper functions: JSON reading, Pandas DataFrame filtering and value extraction,
file hashing (returns an openMINDS ``Hash`` object), file size (returns an
openMINDS ``QuantitativeValue``), and NIfTI version detection.

``report.py``
~~~~~~~~~~~~~

Generates a human-readable conversion summary printed after a successful run,
showing counts of subjects, files, persons, and protocols.

openMINDS object model
----------------------

All metadata objects are instances from the ``openminds.v4`` package:

* ``openminds.v4.core`` — ``Dataset``, ``DatasetVersion``, ``SubjectGroup``,
  ``Subject``, ``SubjectState``, ``Person``, ``File``, ``FileBundle``, etc.
* ``openminds.v4.controlled_terms`` — ``Species``, ``BiologicalSex``,
  ``Handedness``, ``Technique``, ``ExperimentalApproach``, ``UnitOfMeasurement``, etc.

Objects are added to an ``openminds.Collection``, which enforces the schema and
handles JSON-LD serialisation.

Test structure
--------------

``test/test_bids_examples.py``
    End-to-end conversion of datasets from the `bids-examples
    <https://github.com/bids-standard/bids-examples>`_ corpus (checked out as a
    git submodule at ``bids-examples/``).  Each test asserts on the counts of
    openMINDS objects produced.

``test/test_thorough_bids_example.py``
    Deep validation on a more complex BIDS dataset.

``test/test_person.py``, ``test/test_task.py``, ``test/test_subject_age.py``, ``test/test_file_bundle.py``, ``test/test_mapping_completeness.py``
    Unit tests for individual mapping and utility functions.

The ``bids-examples`` submodule must be initialised before running the full test suite::

    git submodule update --init
