from opv_api_client.ressource import Ressource
from opv_api_client.ressource_list import RessourceEnum

class Sensors(Ressource):
    _api_version = "v1"
    _name = RessourceEnum.sensors
    _primary_keys = ("id_sensors", "id_malette")
