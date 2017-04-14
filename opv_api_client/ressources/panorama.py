from opv_api_client.ressource import Ressource
from opv_api_client.ressource_list import RessourceEnum

class Panorama(Ressource):
    _api_version = "v1"
    _name = RessourceEnum.panorama
    _primary_keys = ("id_panorama", "id_malette")
