import pytest

from opv_api_client.helpers import PropertyAsDict

def make_prop_as_dict():
    p = PropertyAsDict({"test": "truc"})
    return p

def test_property_as_dict():
    p = make_prop_as_dict()

    assert p.test == "truc"

    p.test = "machin"
    assert p.test == "machin"

    p.alias = {"bidule": "test"}
    assert p.alias == {"bidule": "test"}

    with pytest.raises(AttributeError):
        p.a_thing_that_dont_exist

def test_property_as_dict_alias():
    p = make_prop_as_dict()

    p.alias = {"bidule": "test"}
    assert p.test is p.bidule

    p.bidule = "plouf"
    assert p.test == "plouf"
