import os
import pytest
from openminds import Collection
import bids2openminds.converter


# Dataset information in following order dataset_label, dataset_subject_number, dataset_subject_state_number, dataset_person_number, dataset_files_number
example_dataset = [("ds003", 13, 13, 2, 58),
                   ("ds000247", 6, 10, 5, 202),
                   # The authors list in 'eeg_cbm' contains non person entities 2 is not correct name (issue raied #43)
                   ("eeg_cbm", 20, 20, 2, 104),
                   ("asl001", 1, 1, 2, 8),
                   # Number of files in 'eeg_rest_fmri' is not correct as it doesn't contain files in derivated (issue raied #42)
                   ("eeg_rest_fmri", 3, 3, 6, 46)]


@pytest.mark.parametrize("dataset_label, dataset_subject_number, dataset_subject_state_number, dataset_person_number, dataset_files_number", example_dataset)
def test_example_datasets(dataset_label, dataset_subject_number, dataset_subject_state_number, dataset_person_number, dataset_files_number):
    test_dir = os.path.join("bids-examples", dataset_label)
    bids2openminds.converter.convert(test_dir, save_output=True)
    c = Collection()
    c.load(os.path.join(test_dir, "openminds.jsonld"))

    subject_number = 0
    subject_state_number = 0
    person_number = 0
    files_number = 0

    for item in c:
        match item.type_:
            case "https://openminds.ebrains.eu/core/Subject":
                subject_number += 1
            case "https://openminds.ebrains.eu/core/SubjectState":
                subject_state_number += 1
            case "https://openminds.ebrains.eu/core/Person":
                person_number += 1
            case "https://openminds.ebrains.eu/core/File":
                files_number += 1

    assert dataset_subject_number == subject_number
    assert dataset_subject_state_number == subject_state_number
    assert dataset_person_number == person_number
    assert dataset_files_number == files_number
