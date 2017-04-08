from opv_api_client.ressource import Ressource
from opv_api_client.ressource_list import RessourceEnum

class Lot(Ressource):
    api_version = "v1"
    name = RessourceEnum.lot
    primary_keys = ("id_lot", "id_malette")
