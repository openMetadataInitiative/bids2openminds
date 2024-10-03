<a href="/logo/light_openMINDS-bids2openminds-logo.png">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="/logo/dark_openMINDS-bids2openminds-logo.png">
    <source media="(prefers-color-scheme: light)" srcset="/logo/light_openMINDS-bids2openminds-logo.png">
    <img alt="bids2openminds logo: created by S Pieschnik, U. Schlegel, L. Zehl, P. Najafi, A. Davison and C. Hagen Blixhavn" src="/logo/light_openMINDS-bids2openminds-logo.png" title="openMINDS instances" align="right" height="70">
  </picture>
</a>

# bids2openminds
A tool to generate openMINDS metadata from BIDS datasets

In active development, please try the first alpha release and send us feedback by creating an issue.  

## Installation

```
pip install bids2openminds
```

## Usage

```
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
  --help                          Show this message and exit.
```

## For developers

To run tests:
```
  $ pytest
```
