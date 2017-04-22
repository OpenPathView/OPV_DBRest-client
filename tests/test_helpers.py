import pytest

from opv_api_client.helpers import PropertyAsDict

def make_prop_as_dict():
    p = PropertyAsDict()
    p._data = {"test": "truc"}
    return p

def test_property_as_dict():
    p = make_prop_as_dict()

    assert p.test == "truc"

    p.test = "machin"
    assert p.test == "machin"

    p._alias = {"bidule": "test"}
    assert p._alias == {"bidule": "test"}

    with pytest.raises(AttributeError):
        p.a_thing_that_dont_exist

def test_property_as_dict_alias():
    p = make_prop_as_dict()

    p._alias = {"bidule": "test"}
    assert p.test is p.bidule

    p.bidule = "plouf"
    assert p.test == "plouf"
