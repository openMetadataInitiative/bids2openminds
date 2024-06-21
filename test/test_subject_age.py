import pandas as pd
import pytest
from bids2openminds.main import create_openminds_age

example_ages = [("89+", "QuantitativeValueRange"),
                (45, "QuantitativeValue"), ("XX", None)]


@ pytest.mark.parametrize("age,age_type", example_ages)
def test_subject_age(age, age_type):
    data_subject_table = pd.DataFrame(data={'age': [age]})
    openminds_age = create_openminds_age(data_subject_table)
    if age_type == "QuantitativeValueRange":
        assert openminds_age.type_ == 'https://openminds.ebrains.eu/core/QuantitativeValueRange'
        assert openminds_age.max_value is None
        assert openminds_age.min_value == 89
    if age_type == "QuantitativeValue":
        assert openminds_age.type_ == 'https://openminds.ebrains.eu/core/QuantitativeValue'
        assert openminds_age.value == age
    if age_type == None:
        assert openminds_age is None
