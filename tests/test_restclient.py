from unittest import mock
import json

from opv_api_client import restclient, ressources, RessourceEnum, Filter
from opv_api_client.filter import treat_query

def test_gen_id():
    assert restclient.RestClient("")._gen_id(2, 1) == "2-1"

def test_make_url():

    c = restclient.RestClient("localhost:5000")
    assert c._makeUrl("v1", "test_res") == "localhost:5000/api/v1/test_res"
    assert c._makeUrl("v1", "test_res", (2, 1)) == "localhost:5000/api/v1/test_res/2-1"

    # Yeah a strange URL
    c = restclient.RestClient("localhost:5000", api_rel_url='/test/{ressource}/{version}', api_id_part="/id:{id}")

    assert c._makeUrl("v1", "test_res") == "localhost:5000/test/test_res/v1"
    assert c._makeUrl("v1", "test_res", (2, 1)) == "localhost:5000/test/test_res/v1/id:2-1"

def test_make():
    c = restclient.RestClient("")

    # Using the enumeration
    ress = c.make(RessourceEnum.lot)
    assert isinstance(ress, ressources.Lot)

    # Using the class
    ress = c.make(ressources.Lot)
    assert isinstance(ress, ressources.Lot)

    with mock.patch.object(c, 'get') as mocked_get:
        ress = c.make(RessourceEnum.lot, 2, 1)

    mocked_get.assert_called_once_with(ress)

def test_save():
    c = restclient.RestClient("")
    ress = ressources.Lot(c, (2, 1))

    with mock.patch('opv_api_client.restclient.requests.patch') as mocked_patch:
        c.save(ress)
    mocked_patch.assert_called_once_with(c._makeUrlFromRessource(ress), json=ress.data)

def test_create():
    c = restclient.RestClient("")
    ress = ressources.Lot(c)

    with mock.patch('opv_api_client.restclient.requests.post') as mocked_post:
        c.create(ress)
    mocked_post.assert_called_once_with(c._makeUrlFromRessource(ress), json=ress.data)


def test_remove():
    c = restclient.RestClient("")
    ress = ressources.Lot(c, (2, 1))

    with mock.patch('opv_api_client.restclient.requests.delete') as mocked_del:
        c.remove(ress)
    mocked_del.assert_called_once_with(c._makeUrlFromRessource(ress))

def test_get():
    c = restclient.RestClient("")
    ress = ressources.Lot(c, (2, 1))

    # Failed
    r = mock.Mock(status_code=404)

    with mock.patch('opv_api_client.restclient.requests.get', return_value=r):
        assert r is c.get(ress)

    assert ress.data == {'id_lot': 2, 'id_malette': 1}

    # Worked
    r = mock.Mock(status_code=200, json=lambda: {"a": 1})
    with mock.patch('opv_api_client.restclient.requests.get', return_value=r):
        assert r is c.get(ress)

    assert ress.data == {"a": 1, 'id_lot': 2, 'id_malette': 1}

def test_make_all():
    c = restclient.RestClient("")

    responses1 = [  # no filter
        {"total_pages": 2, "objects": [{"machin": "truc"}, {"machin": "bidule"}]},
        {"total_pages": 2, "objects": [{"machin": "truc"}]}]

    responses2 = [  # filter
        {"total_pages": 1, "objects": [{"machin": "truc"}, {"machin": "truc"}]}]

    filters = treat_query(Filter("machin") == "truc")
    fparams = dict(q=json.dumps(dict(filters=filters)))

    waited1 = [ressources.Lot(c) for _ in range(3)]
    waited1[0].data = {"machin": "truc"}
    waited1[1].data = {"machin": "bidule"}
    waited1[2].data = {"machin": "truc"}

    waited2 = [ressources.Lot(c) for _ in range(2)]
    waited2[0].data = {"machin": "truc"}
    waited2[1].data = {"machin": "truc"}

    def get(url, params):
        if params == fparams:  # has filter
            v = responses2[params.get("page", 1) - 1]  # because page start at 1
        else:
            v = responses1[params.get("page", 1) - 1]

        return mock.Mock(status_code=200, json=lambda: v)

    with mock.patch('opv_api_client.restclient.requests.get', side_effect=get):
        a1 = c.make_all(ressources.Lot)
        a2 = c.make_all(ressources.Lot, filters)

    assert a1 == waited1
    assert a2 == waited2
