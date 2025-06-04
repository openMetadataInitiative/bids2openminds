import os
import pytest
from openminds import Collection
import bids2openminds.converter


# Dataset information in following order dataset_label, dataset_subject_number, dataset_subject_state_number, dataset_person_number, dataset_files_number, dataset_file_bundles_number, dataset_behavioral_protocol_number
example_dataset = [("ds003", 13, 13, 2, 58, 39, 1),
                   ("ds000247", 6, 10, 5, 50, 41, 2),
                   # The authors list in 'eeg_cbm' contains non person entities 2 is not correct name (issue raied #43)
                   ("eeg_cbm", 20, 20, 2, 104, 40, 1),
                   ("asl001", 1, 1, 2, 8, 3, 0),
                   # Number of files in 'eeg_rest_fmri' is not correct as it doesn't contain files in derivated (issue raied #42)
                   ("eeg_rest_fmri", 3, 3, 6, 45, 22, 1)]


@pytest.mark.parametrize("dataset_label, dataset_subject_number, dataset_subject_state_number, dataset_person_number, dataset_files_number, dataset_file_bundles_number, dataset_behavioral_protocol_number", example_dataset)
def test_example_datasets(dataset_label, dataset_subject_number, dataset_subject_state_number, dataset_person_number, dataset_files_number, dataset_file_bundles_number, dataset_behavioral_protocol_number):
    test_dir = os.path.join("bids-examples", dataset_label)
    bids2openminds.converter.convert(test_dir, save_output=True)
    c = Collection()
    c.load(os.path.join(test_dir, "openminds.jsonld"))

    subject_number = 0
    subject_state_number = 0
    person_number = 0
    files_number = 0
    file_bundles_number = 0
    behavioral_protocol_number = 0
    subject_state_number_besed_on_subject = 0

    for item in c:
        if item.type_ == "https://openminds.om-i.org/types/Subject":
            subject_number += 1
            subject_state_number_besed_on_subject += len(item.studied_states)
        if item.type_ == "https://openminds.om-i.org/types/SubjectState":
            subject_state_number += 1
        if item.type_ == "https://openminds.om-i.org/types/Person":
            person_number += 1
        if item.type_ == "https://openminds.om-i.org/types/File":
            files_number += 1
        if item.type_ == "https://openminds.om-i.org/types/FileBundle":
            file_bundles_number += 1
        if item.type_ == "https://openminds.om-i.org/types/BehavioralProtocol":
            behavioral_protocol_number += 1

    assert dataset_subject_number == subject_number
    assert dataset_subject_state_number == subject_state_number
    assert subject_state_number_besed_on_subject == subject_state_number, "There was a discrepancy between the total number of subject states and the subject states attached to subjects."
    assert dataset_person_number == person_number
    assert dataset_files_number == files_number
    assert dataset_file_bundles_number == file_bundles_number
    assert dataset_behavioral_protocol_number == behavioral_protocol_number
