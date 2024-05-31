import bids2openminds.converter
import os
from openminds import Collection
import pytest

dataset_labels = ["eeg_rest_fmri", "eeg_cbm"]


@pytest.fixture(scope="session")
def load_collections():
    collections = {}
    for dataset_label in dataset_labels:
        test_standard_name = "bids_examples_" + dataset_label + ".jsonld"
        test_standard_path = os.path.join("test", test_standard_name)
        reference_collection = Collection()
        reference_collection.load(test_standard_path)

        test_dataset = os.path.join("bids-examples", dataset_label)
        bids2openminds.converter.convert(test_dataset)
        generated_collection = Collection()
        generated_collection.load(os.path.join(
            test_dataset, "openminds.jsonld"))

        collections[dataset_label] = (
            reference_collection, generated_collection)

    return collections


def detect_type(collection, type):
    type_IRI = "https://openminds.ebrains.eu/core/" + type
    items_list = []
    for item in collection:
        if item.type_ == type_IRI:
            items_list.append(item)
    return items_list if items_list else []


def find_lookup_label(lookup_label, items):
    for item in items:
        if item.lookup_label == lookup_label:
            return item
    return None


def find_person(given_name, family_name, persons):
    for person in persons:
        if person.given_name == given_name and person.family_name == family_name:
            return person
    return None


@pytest.mark.parametrize("dataset_label", dataset_labels)
def test_subject(load_collections, dataset_label):
    reference_collection, generated_collection = load_collections[dataset_label]
    generated_subjects = detect_type(generated_collection, "Subject")
    reference_subjects = detect_type(reference_collection, "Subject")

    assert len(generated_subjects) == len(reference_subjects)

    for reference_subject in reference_subjects:
        generated_subject = find_lookup_label(
            reference_subject.lookup_label, generated_subjects)
        assert generated_subject is not None


@pytest.mark.parametrize("dataset_label", dataset_labels)
def test_subject_state(load_collections, dataset_label):
    reference_collection, generated_collection = load_collections[dataset_label]
    generated_subjects_states = detect_type(
        generated_collection, "SubjectState")
    reference_subjects_states = detect_type(
        reference_collection, "SubjectState")

    assert len(generated_subjects_states) == len(reference_subjects_states)

    for reference_subject_state in reference_subjects_states:
        generated_subject_state = find_lookup_label(
            reference_subject_state.lookup_label, generated_subjects_states)
        assert generated_subject_state is not None


@pytest.mark.parametrize("dataset_label", dataset_labels)
def test_person(load_collections, dataset_label):
    reference_collection, generated_collection = load_collections[dataset_label]
    generated_persons = detect_type(generated_collection, "Person")
    reference_persons = detect_type(reference_collection, "Person")

    assert len(generated_persons) == len(reference_persons)

    for reference_person in reference_persons:
        generated_person = find_person(
            reference_person.given_name, reference_person.family_name, generated_persons)
        assert generated_person is not None


@pytest.mark.parametrize("dataset_label", dataset_labels)
def test_dataset_version(load_collections, dataset_label):
    reference_collection, generated_collection = load_collections[dataset_label]
    generated_dataset_version = detect_type(
        generated_collection, "DatasetVersion")[0]
    reference_dataset_version = detect_type(
        reference_collection, "DatasetVersion")[0]

    assert len(generated_dataset_version.experimental_approaches) == len(
        reference_dataset_version.experimental_approaches)
    assert generated_dataset_version.short_name == reference_dataset_version.short_name
    assert len(generated_dataset_version.techniques) == len(
        reference_dataset_version.techniques)
