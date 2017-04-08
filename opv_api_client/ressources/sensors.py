from opv_api_client.ressource import Ressource
from opv_api_client.ressource_list import RessourceEnum

class Sensors(Ressource):
    api_version = "v1"
    name = RessourceEnum.sensors
