import os
from openminds import Collection
from bids2openminds.converter import convert_click
from click.testing import CliRunner



def test_example_datasets_click():
    test_dir = os.path.join("bids-examples", "ds003")
    runner = CliRunner()
    result = runner.invoke(convert_click, [test_dir])
    assert result.exit_code == 0
    c = Collection()
    c.load(os.path.join(test_dir, "openminds.jsonld"))
