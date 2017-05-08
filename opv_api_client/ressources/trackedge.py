from opv_api_client.ressource import Ressource
from opv_api_client.ressource_list import RessourceProxy, register
from opv_api_client.relationship import Relationship

@register
class TrackEdge(Ressource):
    _api_version = "v1"
    _name = "trackedge"
    _primary_keys = ("id_track_edge", "id_malette")

    class _rel:
        panorama_to = Relationship(RessourceProxy("panorama"))
        panorama_from = Relationship(RessourceProxy("panorama"))
