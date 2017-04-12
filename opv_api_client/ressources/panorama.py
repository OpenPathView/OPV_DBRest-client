from opv_api_client.ressource import Ressource
from opv_api_client.ressource_list import RessourceEnum

class Panorama(Ressource):
    api_version = "v1"
    name = RessourceEnum.panorama
    primary_keys = ("id_panorama", "id_malette")
