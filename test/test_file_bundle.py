import pytest
import os
import pathlib
from openminds import Collection
from bids2openminds.main import create_file_bundle

(test_data_set, number_of_openminds_bundle) = (
    "ds007", 60)

# example_file_filebundle = ([list of the path to this file],[expected file bundle])
example_file_filebundle = ((["sub-04", "anat", "sub-04_inplaneT2.nii.gz"], ["sub-04/anat"]),
                           (["sub-03", "func", "sub-03_task-stopsignalwithmanualresponse_run-02_events.tsv"], ["sub-03/func"]))
# example_folder_filebundle= ([list of path to this folder],[expected folder name],[expected parent filebundle (None for highest level file bundles)])
example_folder_filebundle = ((["sub-04", "anat"], ["sub-04/anat"], ["sub-04"]),
                             (["sub-01"], ["sub-01"], [None]))


@pytest.fixture(scope="session")
def test_dir():
    test_dir = os.path.join("bids-examples", test_data_set)
    return test_dir


def path_name(path):
    name = str(path).replace("\\", "/")
    return name


def example_path(test_dir, path_list):
    path = test_dir
    for item in path_list:
        path = os.path.join(path, item)
    return path


@pytest.fixture(scope="session")
def generate_file_bundle_collection(test_dir):
    collection = Collection()
    file_bundles, _, file_repository = create_file_bundle(
        test_dir, test_dir, collection, is_file_repository=True)
    return file_bundles, collection, file_repository


def test_file_bundles_type(generate_file_bundle_collection):
    file_bundles, _, _ = generate_file_bundle_collection
    assert type(file_bundles) is dict


def test_number_file_bundle(generate_file_bundle_collection):
    _, collection, _ = generate_file_bundle_collection
    m = 0
    for item in collection:
        if item.type_ == "https://openminds.ebrains.eu/core/FileBundle":
            m += 1
    assert m == number_of_openminds_bundle


@pytest.mark.parametrize("path_list, bundle", example_file_filebundle)
def test_random_file(test_dir, path_list, bundle, generate_file_bundle_collection):

    file_bundles, _, _ = generate_file_bundle_collection

    example_file_path = example_path(test_dir, path_list)

    test_bundles = file_bundles[example_file_path]

    assert len(test_bundles) == len(bundle)

    for test_bundle in test_bundles:
        assert test_bundle.name in bundle


@pytest.mark.parametrize("path_list, bundle, parent_bundle", example_folder_filebundle)
def test_random_folder(test_dir, path_list, bundle, parent_bundle, generate_file_bundle_collection):

    _, collection, _ = generate_file_bundle_collection

    file_repository_iri = pathlib.Path(test_dir).absolute().as_uri()

    folder_name = path_name(example_path("", path_list))

    dataset_bundle = None

    for item in collection:
        if item.type_ == "https://openminds.ebrains.eu/core/FileBundle" and item.name == folder_name:
            # detects only one file bundle have this name
            assert dataset_bundle is None
            dataset_bundle = item
    # asserts at least one file bundle have this name
    assert dataset_bundle is not None

    assert dataset_bundle.name == bundle[0]

    if parent_bundle is not None:
        assert dataset_bundle.is_part_of.name == parent_bundle[0]
    else:
        assert dataset_bundle.is_part_of.type_ == "https://openminds.ebrains.eu/core/FileRepository"
        assert dataset_bundle.is_part_of.iri.value == file_repository_iri
