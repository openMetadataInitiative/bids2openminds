# Tests for choosing the openMINDS output version (v4 vs v5).
import os

import pytest
from openminds import Collection

import bids2openminds.converter
import bids2openminds.main as main
import bids2openminds.openminds_version as om


def test_configure_rebinds_modules():
    om.configure("v5")
    assert om.version == "v5"
    assert om.core.__name__ == "openminds.v5.core"
    assert om.controlled_terms.__name__ == "openminds.v5.controlled_terms"

    om.configure("v4")
    assert om.version == "v4"
    assert om.core.__name__ == "openminds.v4.core"
    assert om.controlled_terms.__name__ == "openminds.v4.controlled_terms"


def test_configure_rejects_unknown_version():
    with pytest.raises(ValueError):
        om.configure("v3")


def test_authors_to_contributions():
    om.configure("v5")
    person_1 = main.create_openminds_person("Jane Doe")
    person_2 = main.create_openminds_person("John Smith")

    # No authors -> no contributions.
    assert main._authors_to_contributions(None) is None
    assert main._authors_to_contributions([]) is None

    # A single Person (not wrapped in a list) is normalised to a list.
    single = main._authors_to_contributions(person_1)
    assert len(single) == 1
    assert single[0].contributors == [person_1]
    assert single[0].type.name == "authoring"

    # A list of Persons is kept as-is.
    multiple = main._authors_to_contributions([person_1, person_2])
    assert len(multiple) == 1
    assert multiple[0].contributors == [person_1, person_2]


def test_convert_v5_uses_contributions_and_is_version_of(tmp_path):
    output_path = os.path.join(str(tmp_path), "openminds")
    bids2openminds.converter.convert(
        os.path.join("bids-examples", "ds005"),
        save_output=True,
        output_path=output_path,
        multiple_files=True,
        quiet=True,
        openminds_version="v5",
    )

    # Reloading with the matching version must succeed.
    collection = Collection()
    collection.load(output_path, version="v5")

    dataset_version = None
    dataset = None
    for item in collection:
        if item.type_.endswith("/DatasetVersion"):
            dataset_version = item
        elif item.type_.endswith("/Dataset"):
            dataset = item

    assert dataset_version is not None
    assert dataset is not None

    # v5-specific structure: authors are expressed as contributions and the
    # version links back to the dataset via is_version_of.
    assert dataset_version.contributions
    assert dataset_version.is_version_of is not None
    assert dataset.contributions

    # v4-only properties must not exist on v5 objects.
    assert not hasattr(dataset_version, "authors")
    assert not hasattr(dataset_version, "behavioral_protocols")
    assert not hasattr(dataset, "has_versions")
