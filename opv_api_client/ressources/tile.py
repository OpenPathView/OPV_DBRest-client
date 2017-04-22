from opv_api_client.ressource import Ressource
from opv_api_client.ressource_list import RessourceProxy, register
from opv_api_client.relationship import Relationship

@register
class Tile(Ressource):
    _api_version = "v1"
    _name = "tile"
    _primary_keys = ("id_tile", "id_malette")

    class _rel:
        panorama = Relationship(RessourceProxy("panorama"))
