import bids2openminds.converter
import os
from openminds import Collection
import pytest


@pytest.fixture
def test_standard_collection():
    test_standatd_path = os.path.join(
        "test", "bids_examples_eeg_rest_fmri.jsonld")
    test_standard_collection = Collection()
    test_standard_collection.load(test_standatd_path)
    return test_standard_collection


@pytest.fixture
def test_dataset_collection():
    test_dataset = os.path.join("bids-examples", "eeg_rest_fmri")
    bids2openminds.converter.convert(test_dataset)
    test_dataset_collection = Collection()
    test_dataset_collection.load(
        os.path.join(test_dataset, "openminds.jsonld"))
    return test_dataset_collection


def detect_type(collection, type):
    type_IRI = "https://openminds.ebrains.eu/core/"+type
    items_list = []
    for item in collection:
        if item.type_ == type_IRI:
            items_list.append(item)
    if len(items_list) > 1:
        return items_list
    elif len(items_list) == 1:
        return items_list[0]


def find_lookup_label(lookup_label, list: list):
    for item in list:
        if item.lookup_label == lookup_label:
            return item
    return None


def find_person(given_name, family_name, list: list):
    for person in list:
        if person.given_name == given_name and person.family_name == family_name:
            return person
    return None


def test_subject(test_standard_collection, test_dataset_collection):
    dataset_subjects = detect_type(test_dataset_collection, "Subject")
    standard_subjects = detect_type(test_standard_collection, "Subject")
    assert len(dataset_subjects) == len(standard_subjects)
    for subject in standard_subjects:
        dataset_subject = find_lookup_label(
            subject.lookup_label, dataset_subjects)
        assert dataset_subject is not None


def test_subject_state(test_standard_collection, test_dataset_collection):
    dataset_subjects_state = detect_type(
        test_dataset_collection, "SubjectState")
    standard_subjects_state = detect_type(
        test_standard_collection, "SubjectState")
    assert len(dataset_subjects_state) == len(standard_subjects_state)
    for subject_state in standard_subjects_state:
        dataset_subject_state = find_lookup_label(
            subject_state.lookup_label, dataset_subjects_state)
        assert dataset_subject_state is not None


@pytest.mark.skip(reason="This test should be activated after pull request #36")
def test_person(test_standard_collection, test_dataset_collection):
    dataset_persons = detect_type(
        test_dataset_collection, "Person")
    standard_persons = detect_type(
        test_standard_collection, "Person")
    assert len(dataset_persons) == len(standard_persons)
    for person in standard_persons:
        dataset_p = find_person(
            person.given_name, person.family_name, dataset_persons)
        assert dataset_p is not None


def test_dataset_version(test_standard_collection, test_dataset_collection):
    dataset_version = detect_type(
        test_dataset_collection, "DatasetVersion")
    standard_dataset_version = detect_type(
        test_standard_collection, "DatasetVersion")
    assert len(dataset_version.experimental_approaches) == len(
        standard_dataset_version.experimental_approaches)
    assert dataset_version.short_name == standard_dataset_version.short_name
    assert len(dataset_version.techniques) == len(
        standard_dataset_version.techniques)
