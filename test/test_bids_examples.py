import os
import pytest
from openminds import Collection

import bids2openminds.converter

example_dataset_labels = ("ds003", "ds000247", "eeg_cbm", "asl001")

@pytest.mark.parametrize("dataset_label", example_dataset_labels)
def test_example_datasets(dataset_label):
    test_dir = os.path.join("bids-examples", dataset_label)
    bids2openminds.converter.convert(test_dir)
    c = Collection()
    c.load(os.path.join(test_dir, "openminds.jsonld"))
