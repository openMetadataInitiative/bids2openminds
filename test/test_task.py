import pytest
from bids import BIDSLayout
from openminds import Collection
import os
from bids2openminds.main import create_behavioral_protocol

(datasets, tasks) = ("ds002", ("deterministicclassification",
                               "mixedeventrelatedprobe", "probabilisticclassification"))


@pytest.fixture
def creating_behavioral_protocols():
    c = Collection()
    test_dir = os.path.join("bids-examples", datasets)
    bids_layout = BIDSLayout(test_dir)
    _, behavioral_protocols_dict = create_behavioral_protocol(
        bids_layout, c)
    return behavioral_protocols_dict


def test_behavioral_protocols(creating_behavioral_protocols):
    assert len(tasks) == len(creating_behavioral_protocols)
    for item in creating_behavioral_protocols:
        assert item in tasks
        assert creating_behavioral_protocols[item].internal_identifier == item
