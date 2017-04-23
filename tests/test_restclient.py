from unittest import mock
import pytest
import json
from collections import OrderedDict

from opv_api_client import restclient, ressources, Filter
from opv_api_client.exceptions import RequestAPIException
from opv_api_client.filter import treat_query

def test_gen_id():
    assert restclient.RestClient("")._gen_id(OrderedDict((("a", 2), ("b", 1)))) == "2/1"

def test_make_url():

    c = restclient.RestClient("localhost:5000")
    assert c._makeUrl("v1", "test_res") == "localhost:5000/v1/test_res"
    assert c._makeUrl("v1", "test_res", OrderedDict((("a", 2), ("b", 1)))) == "localhost:5000/v1/test_res/2/1"

    # Yeah a strange URL
    c = restclient.RestClient("localhost:5000", api_rel_url='/test/{ressource}/{version}', api_id_part="/id:{id}")

    assert c._makeUrl("v1", "test_res") == "localhost:5000/test/test_res/v1"
    assert c._makeUrl("v1", "test_res", OrderedDict((("a", 2), ("b", 1)))) == "localhost:5000/test/test_res/v1/id:2/1"

def test_makeUrlFromRessource():
    c = restclient.RestClient("localhost:5000")
    ress = ressources.Lot(c)
    assert c._makeUrlFromRessource(ress) == "localhost:5000/v1/lot"

def test_make_success():
    c = restclient.RestClient("")

    ress = c.make(ressources.Lot)
    assert isinstance(ress, ressources.Lot)

    with mock.patch.object(c, 'get') as mocked_get:
        ress = c.make(ressources.Lot, 2, 1)

    mocked_get.assert_called_once_with(ress)

def test_make_fail():
    c = restclient.RestClient("")

    r = mock.Mock(status_code=404)

    with mock.patch('opv_api_client.restclient.requests.get', return_value=r):
        with pytest.raises(RequestAPIException):
            c.make(ressources.Lot, 2, 1)

def test_save():
    c = restclient.RestClient("")
    ress = ressources.Lot(c, (2, 1))

    with mock.patch('opv_api_client.restclient.requests.patch') as mocked_patch:
        c.save(ress)
    mocked_patch.assert_called_once_with(c._makeUrlFromRessource(ress), json=ress._data)

def test_create():
    c = restclient.RestClient("")
    ress = ressources.Lot(c)

    m = mock.Mock(status_code=201, json=lambda: {})

    with mock.patch('opv_api_client.restclient.requests.post', return_value=m) as mocked_post:
        c.create(ress)
    mocked_post.assert_called_once_with(c._makeUrlFromRessource(ress), json=ress._data)

def test_remove():
    c = restclient.RestClient("")
    ress = ressources.Lot(c, (2, 1))

    with mock.patch('opv_api_client.restclient.requests.delete') as mocked_del:
        c.remove(ress)
    mocked_del.assert_called_once_with(c._makeUrlFromRessource(ress))

def test_get_success():
    c = restclient.RestClient("")
    ress = ressources.Lot(c, (2, 1))

    r = mock.Mock(status_code=200, json=lambda: {"a": 1})
    with mock.patch('opv_api_client.restclient.requests.get', return_value=r):
        assert r is c.get(ress)

    assert ress._data == {"a": 1}  # Will remplace and not update

def test_get_fail():
    c = restclient.RestClient("")
    ress = ressources.Lot(c, (2, 1))

    r = mock.Mock(status_code=404)

    with mock.patch('opv_api_client.restclient.requests.get', return_value=r):
        with pytest.raises(RequestAPIException):
            c.get(ress)

def test_make_all():
    c = restclient.RestClient("")

    responses1 = {  # no filter
        "objects":
        [{"machin": "truc"}, {"machin": "bidule"}, {"machin": "chouette"}]
    }

    responses2 = {  # filter
        "objects":
        [{"machin": "truc"}, {"machin": "truc"}]
    }

    filters = Filter("machin") == "truc"
    fparams = treat_query(filters)

    waited1 = [ressources.Lot(c) for _ in range(3)]
    waited1[0]._data = {"machin": "truc"}
    waited1[1]._data = {"machin": "bidule"}
    waited1[2]._data = {"machin": "chouette"}

    waited2 = [ressources.Lot(c) for _ in range(2)]
    waited2[0]._data = {"machin": "truc"}
    waited2[1]._data = {"machin": "truc"}

    def get(url, params):
        if params == fparams:  # has filter
            return mock.Mock(status_code=200, json=lambda: responses2)
        else:
            return mock.Mock(status_code=200, json=lambda: responses1)

    with mock.patch('opv_api_client.restclient.requests.get', side_effect=get):
        a1 = c.make_all(ressources.Lot)
        a2 = c.make_all(ressources.Lot, filters)

    assert a1 == waited1
    assert a2 == waited2

def test_make_all_fail():
    c = restclient.RestClient("")

    r = mock.Mock(status_code=404)

    with mock.patch('opv_api_client.restclient.requests.get', return_value=r):
        with pytest.raises(RequestAPIException):
            c.make_all(ressources.Lot)
