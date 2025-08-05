Usage
=====

You can use bids2openminds as both a command line tool and a python library.

Usage as Python library
=======================

Overview
########
The ``convert`` function processes a Brain Imaging Data Structure (BIDS) directory, converts its contents into OpenMINDS format, and optionally saves the output. It handles BIDS layout, extracts relevant information, and creates a dataset description based on BIDS data using OpenMINDS templates.


Function Signature
##################
>>> def convert(input_path, save_output=False, output_path=None, short_name=None, multiple_files=False, include_empty_properties=False, quiet=False):

Parameters
##########
- ``input_path`` (str): Path to the BIDS directory. This is required and must be a valid directory.
- ``save_output`` (bool, default=False): If True, the converted OpenMINDS data will be saved to the specified output_path.
- ``output_path`` (str, default=None): The path where the OpenMINDS data should be saved. If not specified, defaults to [``input_path``]/openminds.jsonld (single file mode) or [``input_path``]/openminds/ (multiple files mode).
- ``multiple_files`` (bool, default=False): If True, the OpenMINDS data will be saved into multiple files within the specified output_path.
- ``include_empty_properties`` (bool, default=False): If True, includes all the openMINDS properties with empty values in the final output. Otherwise includes only properties that have a non `None` value.
- ``quiet`` (bool, default=False): If True, suppresses warnings and the final report output. Only prints success messages.
- ``short_name`` (str or bool, default=None): A short name for this dataset. If set to a string, it will be used as the dataset's short name. If set to False, a short name will be assigned automatically. If None, the user will be prompted to enter one during conversion.

Returns
#######
- ``collection`` (openminds.Collection): The OpenMINDS collection object representing the converted dataset. For more information on OpenMINDS collection please refer to `openMINDS readthedocs <https://openminds-documentation.readthedocs.io/en/latest/shared/getting_started/openMINDS_collections.html>`_.

Example Usage
#############
>>> import bids2openminds.converter as converter
>>> input_path = "/path/to/BIDS/dataset"
>>> collection = converter.convert(input_path, save_output=True, short_name=False, output_path="/path/to/output", multiple_files=False, include_empty_properties=False, quiet=False)

Or one can chose the default parmetrs as following:

>>> import bids2openminds.converter as converter
>>> collection = converter.convert("/path/to/BIDS/dataset")


Command-Line Interface (CLI)
============================
This function is also accessible via a command-line interface using the `click` library.

.. code-block:: console

    Usage: bids2openminds [OPTIONS] INPUT_PATH

    Options:
    -o, --output-path PATH          The output path or filename for OpenMINDS
                                    file/files.
    --single-file                   Save the entire collection into a single
                                    file (default).
    --multiple-files                Each node is saved into a separate file
                                    within the specified directory. 'output-
                                    path' if specified, must be a directory.
    -e, --include-empty-properties  Whether to include empty properties in the
                                    final file.
    -q, --quiet                     Not generate the final report and no
                                    warning.
    -n, --short-name TEXT           Short name for the dataset. Set to False to
                                    auto-generate.
    --help                          Show this message and exit.


