from opv_api_client.ressource import Ressource
from opv_api_client.ressource_list import RessourceEnum

class Cp(Ressource):
    _api_version = "v1"
    _name = RessourceEnum.cp
    _primary_keys = ("id_cp", "id_malette")
