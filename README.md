[![Build Status](https://travis-ci.org/OpenPathView/OPV_DBRest-client.svg?branch=master)](https://travis-ci.org/OpenPathView/OPV_DBRest-client)
[![codecov](https://codecov.io/gh/OpenPathView/OPV_DBRest-client/branch/master/graph/badge.svg)](https://codecov.io/gh/OpenPathView/OPV_DBRest-client)
## How to use
```python
from  opv_api_client import RestClient, Filter, RessourceEnum

# create the client with API at localhost:5000
c = RestClient("http://127.0.0.1:5000")

# get the lot with id_lot = 2,  id_malette = 1
lot = c.make(RessourceEnum.lot, 2, 1)

# get taken_lot
lot.taken_date

# set goprofailed
lot.goprofailed = 11100

# commit changes
lot.save()

# create a new campaign
campaign = c.make(RessourceEnum.campaign)

# set id_malette
campaign.id_malette = 1

# create in DB
campaign.create() 

# delete it 
campaign.delete()

# get all lot of campaign with id_campaign == 1 
lots = c.make_all(RessourceEnum.lot, filters=(Filter("id_campaign") == 1))

# get all lot of campaign with id_campaign == 1 and id_malette == 2
lots = c.make_all(RessourceEnum.lot, filters=(Filter("id_campaign") == 1, Filter("id_malette") == 2))
```
## How to maintain
### Add a ressource
e.g with campaign
in ressources/campaign.py
```python
from opv_api_client.ressource import Ressource
from opv_api_client.ressource_list import RessourceEnum

class Campaign(Ressource):
    api_version = "v1"
    name = RessourceEnum.campaign
    primary_keys = ('id_campaign', 'id_malette')
```
in ressource_list.py in RessourceEnum add: `campaign = "campaign"`

in ressources/__init__.py add 
```
...
from opv_api_client.ressources.campaign import Campaign
...

ressources = {
    RessourceEnum.campaign: Campaign,
    ...
}
```
### create an alias
e.g with campaign 
alias test to decription:
in ressources/campaign.py
```
class Campaign(Ressource):
    api_version = "v1"
    name = RessourceEnum.campaign
    primary_keys = ('id_campaign', 'id_malette')
    alias = {"test": "decription"}
```
