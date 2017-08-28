from opv_api_client.relationship import Relationship
from opv_api_client.ressource import Ressource
from opv_api_client.ressource_list import register, RessourceProxy

@register
class Sensors(Ressource):
    _api_version = "v1"
    _name = "sensors"
    _primary_keys = ("id_sensors", "id_malette")

    class _rel:
        lot = Relationship(RessourceProxy("lot"))
