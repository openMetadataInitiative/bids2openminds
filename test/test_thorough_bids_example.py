import bids2openminds.converter
import os
from openminds import Collection
import pytest
from tempfile import mkdtemp
import pathlib
import shutil
import platform


dataset_labels = ["eeg_rest_fmri", "ds005"]


@pytest.fixture(scope="session")
def load_collections():
    collections = {}
    tempdir = mkdtemp()
    for dataset_label in dataset_labels:
        test_standard_name = "bids_examples_" + dataset_label + ".jsonld"
        test_standard_path = os.path.join("test", test_standard_name)

        test_dataset = os.path.join("bids-examples", dataset_label)
        prefix = pathlib.Path(test_dataset).absolute().as_uri()+"/"

        with open(test_standard_path, "r") as file:
            template_data = file.read()
            actual_data = template_data.replace(
                "PREFIX", prefix)

        with open(tempdir+test_standard_name, "w") as file:
            file.write(actual_data)

        reference_collection = Collection()
        reference_collection.load(tempdir+test_standard_name)

        bids2openminds.converter.convert(test_dataset, save_output=True)
        generated_collection = Collection()
        generated_collection.load(os.path.join(
            test_dataset, "openminds.jsonld"))

        collections[dataset_label] = (
            reference_collection, generated_collection)

    shutil.rmtree(tempdir)
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


def find_name(name, items):
    for item in items:
        if item.name == name:
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
    assert len(generated_dataset_version.techniques or []) == len(
        reference_dataset_version.techniques or [])


@pytest.mark.parametrize("dataset_label", dataset_labels)
def test_file(load_collections, dataset_label):
    reference_collection, generated_collection = load_collections[dataset_label]
    generated_files = detect_type(generated_collection, "File")
    reference_files = detect_type(reference_collection, "File")

    assert len(generated_files) == len(reference_files)
    for refrence_file in reference_files:
        generated_file = find_name(refrence_file.name, generated_files)
        assert generated_file is not None
        assert generated_file.iri.value == refrence_file.iri.value
        if generated_file.format is None:
            assert refrence_file.format is None
        else:
            assert generated_file.format.id == refrence_file.format.id
        if platform.system() != 'Windows':
            assert generated_file.hashes[0].digest == refrence_file.hashes[0].digest


@pytest.mark.parametrize("dataset_label", dataset_labels)
def test_file_bundle(load_collections, dataset_label):
    reference_collection, generated_collection = load_collections[dataset_label]
    generated_file_bundles = detect_type(generated_collection, "FileBundle")
    reference_file_bundles = detect_type(reference_collection, "FileBundle")

    assert len(generated_file_bundles) == len(reference_file_bundles)
    for refrence_file_bundle in reference_file_bundles:
        generated_file_bundle = find_name(
            refrence_file_bundle.name, generated_file_bundles)
        assert generated_file_bundle is not None
        if refrence_file_bundle.is_part_of.type_ == "https://openminds.ebrains.eu/core/FileBundle":
            assert generated_file_bundle.is_part_of.type_ == "https://openminds.ebrains.eu/core/FileBundle"
            assert refrence_file_bundle.is_part_of.name == generated_file_bundle.is_part_of.name
