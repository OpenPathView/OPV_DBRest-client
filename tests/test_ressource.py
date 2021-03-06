from unittest import mock

from opv_api_client import restclient, ressources

def test_ressource():
    # should not be used
    c = restclient.RestClient("http://a.base.url.com:5000")

    ress = ressources.Lot(c, (2, 1))

    assert ress._data == {"id_lot": 2, "id_malette": 1}
    assert ress.id == {"id_lot": 2, "id_malette": 1}
