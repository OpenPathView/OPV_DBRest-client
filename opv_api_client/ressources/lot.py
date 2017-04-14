from opv_api_client.ressource import Ressource
from opv_api_client.ressource_list import RessourceEnum

class Lot(Ressource):
    _api_version = "v1"
    _name = RessourceEnum.lot
    _primary_keys = ("id_lot", "id_malette")
