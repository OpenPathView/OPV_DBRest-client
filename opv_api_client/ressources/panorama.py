from opv_api_client.ressource import Ressource
from opv_api_client.ressource_list import RessourceProxy, register
from opv_api_client.relationship import Relationship

@register
class Panorama(Ressource):
    _api_version = "v1"
    _name = "panorama"
    _primary_keys = ("id_panorama", "id_malette")

    class _rel:
        tiles = Relationship(RessourceProxy("tile"), many=True)
        cp = Relationship(RessourceProxy("cp"))
