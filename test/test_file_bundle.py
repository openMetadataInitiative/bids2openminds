import pytest
import os
import openminds.latest.core as omcore
from openminds import Collection
from bids2openminds.main import create_file_bundle

(test_data_set, number_of_openminds_bundle, example_file, example_file_bubdels) = (
    "ds007", 61, "sub-04/anat/sub-04_inplaneT2.nii.gz", ["sub-04", "sub-04_anat"])


@pytest.fixture
def test_dir():
    test_dir = os.path.join("bids-examples", test_data_set)
    return test_dir


@pytest.fixture
def path_name(test_dir):
    name = str(test_dir).replace("/", "_").replace("\\", "_")
    if name[0] == "_":
        name = name[1:]
    return name


@pytest.fixture
def generate_file_bundle_collection(test_dir):
    collection = Collection()
    file_bundels, _ = create_file_bundle(test_dir, collection)
    return file_bundels, collection


def test_file_bundels_type(generate_file_bundle_collection):
    file_bundels, _ = generate_file_bundle_collection
    assert type(file_bundels) is dict


def test_number_file_bundle(generate_file_bundle_collection):
    _, collection = generate_file_bundle_collection
    m = 0
    for item in collection:
        if item.type_ == "https://openminds.ebrains.eu/core/FileBundle":
            m += 1
    assert m == number_of_openminds_bundle


def test_dataset_description_location(test_dir, path_name, generate_file_bundle_collection):
    file_bundels, collection = generate_file_bundle_collection
    dataset_description_location = os.path.join(
        test_dir, "dataset_description.json")
    assert len(file_bundels[dataset_description_location]) == 1

    for item in collection:
        if item.type_ == "https://openminds.ebrains.eu/core/FileBundle" and item.name == path_name:
            main_file_boundle = item

    assert file_bundels[dataset_description_location][0].id == main_file_boundle.id


def test_random_file(test_dir, path_name, generate_file_bundle_collection):
    file_bundels, _ = generate_file_bundle_collection

    reference_boundels = []
    for file in example_file_bubdels:
        reference_boundels.append(path_name+"_"+file)
    reference_boundels.append(path_name)

    test_file_path = os.path.join(
        test_dir, example_file)

    test_bundels = file_bundels[test_file_path]

    assert len(test_bundels) == len(reference_boundels)

    for bundel in test_bundels:
        assert bundel.name in reference_boundels
