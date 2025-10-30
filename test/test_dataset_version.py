import pytest

import pandas as pd
from openminds import Collection
import openminds.v3.core as omcore

from bids2openminds.main import create_dataset_version

def test_create_dataset_version_citation():
    citation = {
        "title": "My Dataset",
        "version": "1.05.9",
        "doi": "10.5281/zenodo.123456",
        "license": "Apache-2.0"
    }

    # Mock BIDS layout DataFrame
    layout_df = pd.DataFrame({
        "suffix": ["T1w", "T2w", "bold"],
        "path": ["sub-01/anat/sub-01_T1w.nii.gz", "sub-01/anat/sub-01_T2w.nii.gz", "sub-01/func/sub-01_task-rest_bold.nii.gz"],
        "datatype": ["anat", "anat", "func"]
    })

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
