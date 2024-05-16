import bids2openminds.converter
import os
from openminds import Collection
import pytest


@pytest.fixture
def reference_collection():
    test_standatd_path = os.path.join(
        "test", "bids_examples_eeg_rest_fmri.jsonld")
    reference_collection = Collection()
    reference_collection.load(test_standatd_path)
    return reference_collection


@pytest.fixture
def generated_collection():
    test_dataset = os.path.join("bids-examples", "eeg_rest_fmri")
    bids2openminds.converter.convert(test_dataset)
    generated_collection = Collection()
    generated_collection.load(
        os.path.join(test_dataset, "openminds.jsonld"))
    return generated_collection


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


def test_subject(reference_collection, generated_collection):
    generated_subjects = detect_type(generated_collection, "Subject")
    reference_subjects = detect_type(reference_collection, "Subject")
    assert len(generated_subjects) == len(reference_subjects)
    for reference_subject in reference_subjects:
        generated_subject = find_lookup_label(
            reference_subject.lookup_label, generated_subjects)
        assert generated_subject is not None


def test_subject_state(reference_collection, generated_collection):
    generated_subjects_states = detect_type(
        generated_collection, "SubjectState")
    reference_subjects_states = detect_type(
        reference_collection, "SubjectState")
    assert len(generated_subjects_states) == len(reference_subjects_states)
    for reference_subject_state in reference_subjects_states:
        generated_subject_state = find_lookup_label(
            reference_subject_state.lookup_label, generated_subjects_states)
        assert generated_subject_state is not None


@pytest.mark.skip(reason="This test should be activated after pull request #36")
def test_person(reference_collection, generated_collection):
    generated_persons = detect_type(
        generated_collection, "Person")
    reference_persons = detect_type(
        reference_collection, "Person")
    assert len(generated_persons) == len(reference_persons)
    for reference_person in reference_persons:
        generated_person = find_person(
            reference_person.given_name, reference_person.family_name, generated_persons)
        assert generated_person is not None


def test_dataset_version(reference_collection, generated_collection):
    generated_dataset_version = detect_type(
        generated_collection, "DatasetVersion")
    reference_dataset_version = detect_type(
        reference_collection, "DatasetVersion")
    assert len(generated_dataset_version.experimental_approaches) == len(
        reference_dataset_version.experimental_approaches)
    assert generated_dataset_version.short_name == reference_dataset_version.short_name
    assert len(generated_dataset_version.techniques) == len(
        reference_dataset_version.techniques)
