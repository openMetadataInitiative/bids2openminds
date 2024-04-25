import os
import pytest
from openminds import Collection
from click.testing import CliRunner

from bids2openminds.converter import convert

example_dataset_labels = ("ds003", "ds000247", "eeg_cbm", "asl001")

@pytest.mark.parametrize("dataset_label", example_dataset_labels)
def test_example_datasets(dataset_label):
    test_dir = os.path.join("bids-examples", dataset_label)
    runner = CliRunner()
    result = runner.invoke(convert, [test_dir])
    assert result.exit_code == 0
    c = Collection()
    c.load(os.path.join(test_dir, "openminds.jsonld"))
