from opv_api_client.relationship import Relationship
from opv_api_client.ressource import Ressource
from opv_api_client.ressource_list import RessourceProxy, register

@register
class Cp(Ressource):
    _api_version = "v1"
    _name = "cp"
    _primary_keys = ("id_cp", "id_malette")

    class _rel:
        panorama = Relationship(RessourceProxy("panorama"), many=True)
        lot = Relationship(RessourceProxy("lot"))
