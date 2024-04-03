import os
from openminds import Collection
import bids2openminds.converter


def test_example_datasets():
    test_dir = os.path.join("bids-examples", "ds003")
    bids2openminds.converter.convert(test_dir)
    c = Collection()
    c.load(os.path.join(test_dir, "openminds.jsonld"))
