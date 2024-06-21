# test for create_openminds_person function in the main
import pytest
from bids2openminds.main import create_openminds_person
import openminds.latest.core as omcore

# Test data: (full_name, given_name, family_name)
example_names = [("John Ronald Reuel Tolkien", "John Ronald Reuel", "Tolkien"),
                 ("Bilbo Baggins", "Bilbo", "Baggins"),
                 ("Xue, G.", "G.", "Xue"),
                 ("Arndís Þórarinsdóttir", "Arndís", "Þórarinsdóttir"),
                 ("Loïc Le Clézio", "Loïc", "Le Clézio"),
                 ("P Gandolf", "P", "Gandolf")]

example_not_names = ["42", "#", "", "A34 hajb"]


@pytest.mark.parametrize("full_name, given_name, family_name", example_names)
def test_create_openminds_person(full_name, given_name, family_name):
    openminds_person_object = omcore.Person(given_name=given_name,
                                            family_name=family_name)
    bids2openminds_person_object = create_openminds_person(full_name)
    assert openminds_person_object.given_name == bids2openminds_person_object.given_name, \
        f"Given names don't match for input '{full_name}'"
    assert openminds_person_object.family_name == bids2openminds_person_object.family_name, \
        f"Family names don't match for input '{full_name}'"
    assert openminds_person_object.type_ == bids2openminds_person_object.type_, \
        f"Person types don't match for input '{full_name}'"
    # assert openminds_person_object == bids2openminds_person_object


@pytest.mark.parametrize("full_not_name", example_not_names)
def test_create_openminds_person_not_names(full_not_name):
    bids2openminds_person_object = create_openminds_person(full_not_name)
    assert bids2openminds_person_object is None
