## How to use
```python
import opv_client_api

# create the client with API at localhost:5000
c = opv_api_client.RestClient("http://127.0.0.1:5000")

# get the lot with id_lot = 2,  id_malette = 1
lot = c.make(opv_api_client.RessourceEnum.lot, 2, 1)

# get taken_lot
lot.taken_date

# or get taken_lot (1st way is better) -- May be remove soon, don't use it (except for debug - maybe)
lot['taken_date']

# set goprofailed
lot.goprofailed = 11100

# commit changes
lot.save()

# create a new campaign
campaign = c.make(opv_api_client.RessourceEnum.campaign)

# set id_malette
campaign.id_malette = 1

# create in DB
campaign.create() 

# delete it 
campaign.delete()

# get all lot of campaign with id_campaign == 1 -> cf http://flask-restless.readthedocs.io/en/stable/searchformat.html
#                                                  To get the format for filters
lots = c.make_all(opv_api_client.RessourceEnum.lot, filters=[{"name":"id_campaign", "op":"eq", "val":"1"}])
```

TODO: create helpers fcts for filters

delete, create, save... return the response of resquests

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
    alias = {"test": "decription"}
```
