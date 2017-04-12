from opv_api_client.ressource import Ressource
from opv_api_client.ressource_list import RessourceEnum

class Tile(Ressource):
    api_version = "v1"
    name = RessourceEnum.tile
    primary_keys = ("id_tile", "id_malette")
