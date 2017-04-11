#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import json

from opv_api_client.ressources import ressources
from opv_api_client.filter import treat_query

class RestClient:
    """A client that allow to connect to the rest API"""
    def __init__(self, baseUrl, api_rel_url='/api/{version}/{ressource}', api_id_part='/{id}'):
        self.baseUrl = baseUrl
        self.api_rel_url = api_rel_url
        self.api_id_part = api_id_part

    def _makeUrl(self, api_version, api_ressource, api_ressource_id=None):
        url = self.baseUrl
        url += self.api_rel_url.format(version=api_version, ressource=api_ressource)
        if api_ressource_id:
            url += self.api_id_part.format(id=self._gen_id(*api_ressource_id))
        return url

    def save(self, ressource):
        """Update the ressource"""
        url = self._makeUrl(
           ressource.api_version,
           ressource.name.value,
           ressource.id)
        return requests.patch(url, json=ressource)

    def create(self, ressource):
        """Create the ressource"""
        url = self._makeUrl(
           ressource.api_version,
           ressource.name.value)
        return requests.post(url, json=ressource)

    def remove(self, ressource):
        """return the ressource"""
        url = self._makeUrl(
           ressource.api_version,
           ressource.name.value,
           ressource.id)
        return requests.delete(url)

    def get(self, ressource):
        """update the ressource, return the return of request"""
        url = self._makeUrl(
           ressource.api_version,
           ressource.name.value,
           ressource.id)
        r = requests.get(url)

        if r.status_code == 200:
            ressource.update(r.json())
        return r

    def _gen_id(self, id, id_malette):
        return "{}-{}".format(id, id_malette)

    def make(self, ressource_name, id_ress=None, id_malette=None):
        ressource_class = ressources[ressource_name]
        ress = ressource_class(self, (id_ress, id_malette))

        if id_malette and id_ress:
            self.get(ress)

        return ress

    def make_all(self, ressource_name, filters=None):
        """
        Get all the ressources of name ressource_name
        Filter is of the same form than the flask_restless
            -> cf http://flask-restless.readthedocs.io/en/stable/searchformat.html
        """
        ressource_class = ressources[ressource_name]
        url = self._makeUrl(ressource_class.api_version,
                ressource_class.name.value)

        # Create params
        filters = treat_query(filters)
        params = dict()
        if filters:
            params = dict(q=json.dumps(
                          dict(filters=filters)))


        print(params)

        # get first page
        r = requests.get(url, params=params)
        if r.status_code != 200:
            return []
        j = r.json()

        # get nbr of page
        page_number = j.get("total_pages", 1)
        page = j

        list_ress = []

        # Get the list of ressource
        for x in range(1, page_number + 1):  # for page in all_pages
            for data in page["objects"]:  # for ressource in page
                ress = self.make(ressource_name)
                ress.data = data

                list_ress.append(ress)

            params["page"] = page_number
            page = requests.get(url, params=params)

        return list_ress
