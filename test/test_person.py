# test for create_openminds_person function in the main
import pytest

from openminds import Collection

import bids2openminds.openminds_version as om
from bids2openminds.main import create_openminds_person, create_persons

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
    openminds_person_object = om.core.Person(given_name=given_name,
                                            family_name=family_name)
    bids2openminds_person_object = create_openminds_person(full_name)
    assert openminds_person_object.given_name == bids2openminds_person_object.given_name, \
        f"Given names don't match for input '{full_name}'"
    assert openminds_person_object.family_name == bids2openminds_person_object.family_name, \
        f"Family names don't match for input '{full_name}'"
    assert openminds_person_object.type_ == bids2openminds_person_object.type_, \
        f"Person types don't match for input '{full_name}'"
    # assert openminds_person_object == bids2openminds_person_object


def test_create_openminds_person_citation_explicit():
    citation = {
        "authors": [
            {
                "family-names": "Awart",
                "given-names": "Peter",
                "affiliation": "Place1",
                "orcid": "https://orcid.org/1234-5678-9123-4567"
            },
            {
                "family-names": "Detienne",
                "given-names": "Franck",
                "affiliation": "Place1; Place2"
            }
        ]
    }

    persons = create_persons(citation, Collection())
    author1 = persons[0]
    author2 = persons[1]

    # Expected objects
    expected_author1 = om.core.Person(
        given_name="Peter",
        family_name="Awart",
        affiliations=[
            om.core.Affiliation(member_of=om.core.Organization(full_name="Place1"))
        ],
        digital_identifiers=[om.core.ORCID(identifier="https://orcid.org/1234-5678-9123-4567")]
    )

    expected_author2 = om.core.Person(
        given_name="Franck",
        family_name="Detienne",
        affiliations=[
            om.core.Affiliation(member_of=om.core.Organization(full_name="Place1")),
            om.core.Affiliation(member_of=om.core.Organization(full_name="Place2"))
        ]
    )

    assert author1.given_name == expected_author1.given_name
    assert author1.family_name == expected_author1.family_name
    assert author1.digital_identifiers[0].identifier == expected_author1.digital_identifiers[0].identifier
    assert author2.given_name == expected_author2.given_name
    assert author2.family_name == expected_author2.family_name

    # Single affiliation
    assert author1.affiliations[0].member_of.full_name == expected_author1.affiliations[0].member_of.full_name

    # Multiple affiliations
    assert author2.affiliations[0].member_of.full_name == expected_author2.affiliations[0].member_of.full_name
    assert author2.affiliations[1].member_of.full_name == expected_author2.affiliations[1].member_of.full_name


@pytest.mark.parametrize("full_not_name", example_not_names)
def test_create_openminds_person_not_names(full_not_name):
    bids2openminds_person_object = create_openminds_person(full_not_name)
    assert bids2openminds_person_object is None
