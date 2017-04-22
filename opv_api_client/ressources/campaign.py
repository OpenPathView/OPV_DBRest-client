from opv_api_client.ressource import Ressource
from opv_api_client.relationship import Relationship
from opv_api_client.ressource_list import RessourceProxy, register

@register
class Campaign(Ressource):
    _api_version = "v1"
    _name = "campaign"
    _primary_keys = ("id_campaign", "id_malette")

    class _rel:
        lots = Relationship(RessourceProxy("lot"), many=True)
