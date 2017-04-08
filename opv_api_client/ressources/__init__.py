from opv_api_client.ressources.lot import Lot
from opv_api_client.ressources.campaign import Campaign
from opv_api_client.ressource_list import RessourceEnum

ressources = {
    RessourceEnum.lot: Lot,
    RessourceEnum.campaign: Campaign}
