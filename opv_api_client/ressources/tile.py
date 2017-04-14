from opv_api_client.ressource import Ressource
from opv_api_client.ressource_list import RessourceEnum

class Tile(Ressource):
    _api_version = "v1"
    _name = RessourceEnum.tile
    _primary_keys = ("id_tile", "id_malette")
