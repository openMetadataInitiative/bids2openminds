import pytest

import pandas as pd
from openminds import Collection
import openminds.v4.core as omcore

from bids2openminds.main import create_dataset_version

# Mock BIDS layout DataFrame
layout_df = pd.DataFrame({
    "suffix": ["T1w", "T2w", "bold"],
    "path": ["sub-01/anat/sub-01_T1w.nii.gz", "sub-01/anat/sub-01_T2w.nii.gz", "sub-01/func/sub-01_task-rest_bold.nii.gz"],
    "datatype": ["anat", "anat", "func"]
})


def test_create_dataset_version_citation():
    # Mock loaded CITATION.cff
    citation = {
        "title": "My Dataset",
        "version": "1.05.9",
        "doi": "10.5281/zenodo.123456",
        "license": "Apache-2.0"
    }

    citation_dataset_version = create_dataset_version(
        "", citation, {}, layout_df, [], [], [], Collection()
    )

    expected = omcore.DatasetVersion(
        digital_identifier=omcore.DOI(identifier="10.5281/zenodo.123456"),
        full_name="My Dataset",
        short_name="My Dataset",
        license=omcore.License.apache_2_0,
        version_identifier="1.05.9"
    )

    for field in ["full_name", "short_name", "version_identifier", "license"]:
        assert getattr(citation_dataset_version, field) == getattr(expected, field)
    assert citation_dataset_version.digital_identifier.identifier == expected.digital_identifier.identifier


def test_create_dataset_version_without_citation():
    # Mock missing CITATION.cff
    citation = None
    dataset_description = {
        "Name": "My Dataset",
        "DatasetDOI": "10.5281/zenodo.123456"
    }

    dataset_version = create_dataset_version(
        "", citation, dataset_description, layout_df, [], [], [], Collection()
    )

    expected = omcore.DatasetVersion(
        digital_identifier=omcore.DOI(identifier="10.5281/zenodo.123456"),
        full_name="My Dataset",
        short_name="My Dataset"
    )

    for field in ["full_name", "short_name"]:
        assert getattr(dataset_version, field) == getattr(expected, field)
    assert dataset_version.digital_identifier.identifier == expected.digital_identifier.identifier
