#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import json


from inspect import isclass

from opv_api_client.exceptions import RequestAPIException
from opv_api_client.ressource import Ressource
from opv_api_client.ressources import ressources
from opv_api_client.filter import treat_query

class RestClient:
    """A client that allow to connect to the rest API

    This class make easy to connect to an API and to work with her.
    This class mainly allow you to get ressources (see `make`)
    """
    def __init__(self, baseUrl, api_rel_url='/api/{version}/{ressource}', api_id_part='/{id}'):
        """ The initializer of :class RestClient:

        Args:
            baseURL: The path of the server on which is stored the API
            api_rel_url: The relative path, from the baseURL, where we can find the ressource
                         You can customize the URL, by version and by ressource, using, respectively
                         {version}, {ressource} instead of the version, ressource name
            api_id_part: The relative path, from the baseURL + api_rel_url, where we can find the ressource by ID
                         You can customize the URL, by ID using {id} instead of the ID
        """
        self.baseUrl = baseUrl
        self.api_rel_url = api_rel_url
        self.api_id_part = api_id_part

    def _makeUrlFromRessource(self, ressource):
        """A simple wrapper around makeUrl that makes it easier

        Params:
            ressource(Ressource): The ressource from which will be created the URL
        Returns:
            str: The final URL, that can be directly used.
        """
        id = ressource.id
        try:
            iter(id)
        except TypeError:
            id = None
        return self._makeUrl(ressource.api_version,
                             ressource.name.value,
                             id)

    def _makeUrl(self, api_version, api_ressource, api_ressource_id=None):
        """An internal fonction that generate the ressource URL

        This will just format the URL, as it is passed in __init__ to an usable URL

        Args:
            api_version(str): version of the ressource.
                {version} will be remplaced by ``api_version`` in ``RestClient.api_rel_url``

            api_ressource(RessourceEnum): name of the ressource.
                {ressource} will be remplaced by ``api_ressource``.value in ``RestClient.api_rel_url``

            api_ressource_id(tuple, optional): id of the ressource.
                {id} will be remplaced by ``api_ressource_id`` in ``RestClient.api_id_part`` after being
                treated by ``_gen_id``
                If api_ressource_id=None, do not care about the id part add will return

        Returns:
            str: The final URL, that can be directly used.
        """
        url = self.baseUrl
        url += self.api_rel_url.format(version=api_version, ressource=api_ressource)

        if api_ressource_id:
            url += self.api_id_part.format(id=self._gen_id(*api_ressource_id))
        return url

    def save(self, ressource):
        """Update the ressource - Do not use directly

        Don't use this directly, this will be done by Ressource

        Args:
            ressource(Ressource): the ressource to remove
        """
        url = self._makeUrlFromRessource(ressource)
        return requests.patch(url, json=ressource.data)

    def create(self, ressource):
        """Create the ressource - Do not use directly

        Don't use this directly, this will be done by Ressource
        Warning: Affect the server

        Args:
            ressource(Ressource): the ressource to create
        """
        url = self._makeUrlFromRessource(ressource)
        return requests.post(url, json=ressource.data)

    def remove(self, ressource):
        """Remove the ressource - Do not use directly

        Don't use this directly, this will be done by Ressource
        Warning: Affect the server

        Args:
            ressource(Ressource): the ressource to remove
        """
        url = self._makeUrlFromRessource(ressource)
        return requests.delete(url)

    def get(self, ressource):
        """Get the ressource - Do not use directly

        Don't use this directly, this will be done by Ressource
        Warning: Affect the server

        Args:
            ressource(Ressource): the ressource to get
        Returns:
            requests.Response: The response of the request
        Raises
            RequestAPIException: if the ressource can't be fetched
        """
        url = self._makeUrlFromRessource(ressource)
        r = requests.get(url)

        if r.status_code == 200:
            ressource.data.update(r.json())
            return r
        else:
            raise RequestAPIException("Can't get the ressource on the API", response=r)

    def _gen_id(self, id, id_malette):
        """An helper that generate an id from a composite id

        Params:
            id: an id -> May be id_lot, id_sensors...
            id_malette: The id of the malette

        Returns:
            str: id-id_malette
        """
        return "{}-{}".format(id, id_malette)

    def make(self, ressource, id_ress=None, id_malette=None):
        """Make a ressource

        This make a ``Ressource``. If the id is not None (i.e id_ress and id_malette != None),
            this will get the data from the server
            If the id is None, create a new ressource. To instanciate this ressource on the server,
            will need to call the ``create`` fonction of the ``Ressource``

        Params:
            ressource(:obj: RessourceEnum or :obj: Ressource): The type of the ressource to be created
            id_ress: the id of the ressource
            id_malette: the id_malette of the ressource

        Returns:
            Ressource: The new instanciated ressource
        """
        # get the class of the ressource to make
        if isclass(ressource) and issubclass(ressource, Ressource):
            ressource_class = ressource
        else:
            ressource_class = ressources[ressource]

        # if already exist (aka id is set), get the existing ressource otherwise create a new one
        if id_malette and id_ress:
            ress = ressource_class(self, (id_ress, id_malette))
            self.get(ress)
        else:
            ress = ressource_class(self)

        return ress

    def make_all(self, ressource, filters=None):
        """ make all ressource that are satisfying filters
        Args:
            ressource(Ressource): The ressource type that will be created
            filters(:obj: Filter or :obj: dict or :obj: list, optional): Any kind of filter accepted by filter.treat_query
        Returns:
            list: The list of all the ressource that satisfy filters
        """
        # get the class of the ressource to make
        if isclass(ressource) and issubclass(ressource, Ressource):
            ressource_class = ressource
        else:
            ressource_class = ressources[ressource]

        # The url of the ressource
        url = self._makeUrlFromRessource(ressource_class)

        # Create params that will be send
        if filters:
            filters = treat_query(filters)  # Filter is now a list of dict as accepted by the API
            params = dict(q=json.dumps(dict(filters=filters)))
        else:
            params = dict()

        # get first page - Allow to know the number of pages, etc
        r = requests.get(url, params=params)
        if r.status_code != 200:
            raise RequestAPIException("Can't get the list of ressources", response=r)
        j = r.json()

        # get nbr of page
        page_number = j.get("total_pages", 1)
        page = j

        list_ress = []

        # Get the list of ressource
        for x in range(1, page_number + 1):  # for page in all_pages
            for data in page["objects"]:  # for ressource in page
                ress = self.make(ressource_class)
                ress.data = data

                list_ress.append(ress)

            params["page"] = page_number
            page = requests.get(url, params=params).json()

        return list_ress
