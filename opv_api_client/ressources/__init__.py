from opv_api_client.ressources.lot import Lot
from opv_api_client.ressources.campaign import Campaign
from opv_api_client.ressources.cp import Cp
from opv_api_client.ressources.panorama import Panorama
from opv_api_client.ressources.tile import Tile
from opv_api_client.ressources.sensors import Sensors


from opv_api_client.ressource_list import RessourceEnum

ressources = {RessourceEnum.lot: Lot,
              RessourceEnum.campaign: Campaign,
              RessourceEnum.panorama: Panorama,
              RessourceEnum.sensors: Sensors,
              RessourceEnum.tile: Tile,
              RessourceEnum.cp: Cp}
