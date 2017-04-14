from opv_api_client.ressource import Ressource
from opv_api_client.ressource_list import RessourceEnum

class Campaign(Ressource):
    _api_version = "v1"
    _name = RessourceEnum.campaign
    _primary_keys = ("id_campaign", "id_malette")
