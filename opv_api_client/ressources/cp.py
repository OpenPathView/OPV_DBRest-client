from opv_api_client.ressource import Ressource
from opv_api_client.ressource_list import RessourceEnum

class Cp(Ressource):
    api_version = "v1"
    name = RessourceEnum.cp
    primary_keys = ("id_cp", "id_malette")
