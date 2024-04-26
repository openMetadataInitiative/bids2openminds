import os
from openminds import Collection
from bids2openminds.converter import convert_click
from click.testing import CliRunner

(test_data_set,number_of_openminds_files)= ("ds003",98)

def test_example_datasets_click():
    test_dir = os.path.join("bids-examples",test_data_set)
    runner = CliRunner()
    result = runner.invoke(convert_click, [test_dir])
    assert result.exit_code == 0
    c = Collection()
    c.load(os.path.join(test_dir, "openminds.jsonld"))

#todo This section has a problem which have been solved in pull request number 32
""" def test_example_datasets_click_seperate_files():
    test_dir = os.path.join("bids-examples", test_data_set)
    runner = CliRunner()
    result = runner.invoke(convert_click, ["--multiple-file",test_dir])
    assert result.exit_code == 0
    path_openminds=os.path.join(test_dir, "openminds")
    numer_of_files=len(os.listdir(path_openminds))
    assert numer_of_files==number_of_openminds_files """

def test_example_datasets_click_output_location():
    test_dir = os.path.join("bids-examples", test_data_set)
    runner = CliRunner()
    result = runner.invoke(convert_click, ["-o","test_openminds.jsonld",test_dir])
    assert result.exit_code == 0
    c = Collection()
    c.load("test_openminds.jsonld")
