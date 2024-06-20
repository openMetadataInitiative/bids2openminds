import os
import shutil
from openminds import Collection
from bids2openminds.converter import convert_click
from click.testing import CliRunner

(test_data_set, number_of_openminds_files) = ("ds003", 143)


def test_example_datasets_click():
    test_dir = os.path.join("bids-examples", test_data_set)
    runner = CliRunner()
    result = runner.invoke(convert_click, [test_dir])
    assert result.exit_code == 0
    c = Collection()
    c.load(os.path.join(test_dir, "openminds.jsonld"))


def test_example_datasets_click_seperate_files():
    test_dir = os.path.join("bids-examples", test_data_set)
    path_openminds = os.path.join(test_dir, "openminds")
    if os.path.isdir(path_openminds):
        shutil.rmtree(path_openminds)
    runner = CliRunner()
    result = runner.invoke(convert_click, ["--multiple-files", test_dir])
    assert result.exit_code == 0
    numer_of_files = len(os.listdir(path_openminds))
    assert numer_of_files == number_of_openminds_files


def test_example_datasets_click_output_location():
    test_dir = os.path.join("bids-examples", test_data_set)
    openminds_file = os.path.join("bids-examples", "test_openminds.jsonld")
    runner = CliRunner()
    result = runner.invoke(
        convert_click, ["-o", openminds_file, test_dir])
    assert result.exit_code == 0
    c = Collection()
    c.load(openminds_file)
