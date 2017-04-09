from opv_api_client.ressource import Ressource


def test_ressource():
    from opv_api_client import RestClient

    # should not be used
    c = RestClient("http://a.base.url.com:5000")

    class TestRessource(Ressource):
        api_version = "v1"
        name = "test"
        primary_keys = ("p1", "p2")

    ress = TestRessource(c, (2, 1))

    assert ress.data == {"p1": 2, "p2": 1}
    assert ress.id == (2, 1)
