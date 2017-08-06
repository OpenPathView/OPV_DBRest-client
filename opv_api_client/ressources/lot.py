from opv_api_client.relationship import Relationship
from opv_api_client.ressource import Ressource
from opv_api_client.ressource_list import register, RessourceProxy

@register
class Lot(Ressource):
    _api_version = "v1"
    _name = "lot"
    _primary_keys = ("id_lot", "id_malette")

    class _rel:
        campaign = Relationship(RessourceProxy("campaign"))
        cps = Relationship(RessourceProxy("cp"), many=True)
        sensors = Relationship(RessourceProxy("sensors"))
        tile = Relationship(RessourceProxy("tile"))
