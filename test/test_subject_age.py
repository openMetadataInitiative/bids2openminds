import pandas as pd
import pytest
from bids2openminds.main import create_openminds_age
import bids2openminds.openminds_version as om

example_ages = [("89+", "QuantitativeValueRange"),
                (45, "QuantitativeValue"), ("XX", None)]


@ pytest.mark.parametrize("age,age_type", example_ages)
def test_subject_age(age, age_type):
    data_subject_table = pd.DataFrame(data={'age': [age]})
    openminds_age = create_openminds_age(data_subject_table)
    if age_type == "QuantitativeValueRange":
        assert openminds_age.type_ == 'https://openminds.om-i.org/types/QuantitativeValueRange'
        assert openminds_age.max_value is None
        assert openminds_age.min_value == 89
    if age_type == "QuantitativeValue":
        assert openminds_age.type_ == 'https://openminds.om-i.org/types/QuantitativeValue'
        assert openminds_age.value == age
    if age_type == None:
        assert openminds_age is None


@pytest.mark.parametrize("age,age_type", [("89+", "QuantitativeValueRange"), (45, "QuantitativeValue")])
def test_subject_age_v5(age, age_type):
    om.configure("v5")
    data_subject_table = pd.DataFrame(data={'age': [age]})
    specimen_age = create_openminds_age(data_subject_table)

    assert specimen_age.type_.endswith("SpecimenAge")
    assert specimen_age.reference.name == "birth"

    inner = specimen_age.age
    if age_type == "QuantitativeValueRange":
        assert inner.type_.endswith("QuantitativeValueRange")
        assert inner.max_value is None
        assert inner.min_value == 89
    else:
        assert inner.type_.endswith("QuantitativeValue")
        assert inner.value == age


def test_subject_age_unknown_v5():
    om.configure("v5")
    data_subject_table = pd.DataFrame(data={'age': ["XX"]})
    assert create_openminds_age(data_subject_table) is None
