import os
import pytest
from openminds import Collection

import bids2openminds.converter

example_dataset = [("ds003",13), ("ds000247",6), ("eeg_cbm",20), ("asl001",1),("eeg_rest_fmri",3)]

@pytest.mark.parametrize("dataset_label,dataset_number_subject", example_dataset)
def test_example_datasets(dataset_label, dataset_number_subject):
    test_dir = os.path.join("bids-examples", dataset_label)
    bids2openminds.converter.convert(test_dir)
    c = Collection()
    c.load(os.path.join(test_dir, "openminds.jsonld"))
    subject_numbers=0
    for item in c:
        if item.type_=='https://openminds.ebrains.eu/core/Subject':
            subject_numbers+=1
    print(subject_numbers)
    assert dataset_number_subject==subject_numbers
    


