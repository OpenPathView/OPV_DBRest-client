from opv_api_client.helpers import PropertyAsDict, MetaRessource
from collections import OrderedDict


__all__ = ['Ressource']

class Ressource(PropertyAsDict, metaclass=MetaRessource):
    _api_version = None
    _name = None
    _primary_keys = tuple()

    class _rel:
        """A class that allow to add relationships"""

    ###
    # Initializers
    ###

    def __init__(self, rest_client, ids=None, lazy=False):
        """Warning, __init__ should be called at the very end of child's init - Won't works otherwise

        Args:
            rest_client: the rest_client used by create, ...
            ids(tuple): a tuple of ids
            lazy(bool): if True, will only to do a get when trying to get the datas or when explicitly doing a get
                Don't use it when ids = None
        """
        self._rest_client = rest_client
        self._lazy = lazy

        if ids:
            self._data = {primary_key: id for primary_key, id in zip(self._primary_keys, ids)}
        else:
            self._data = {}

    @classmethod
    def from_id(cls, c, data, lazy=False):
        ids = (data.get(i) for i in cls._primary_keys)
        return cls(c, ids, lazy)

    ###
    # Helpers to get data from the ressource
    ###

    @property
    def id(self):
        """:obj: tuple or :obj: None: return the id of the ressource, if any"""
        try:
            return OrderedDict((primary_key, self._data[primary_key]) for primary_key in self._primary_keys)
        except KeyError:  # Don't have a full ID, probably not created
            return None

    @property
    def data(self):
        """Use to get the _data internal dict"""
        if self._lazy:
            self.get()
        return self._data

    ###
    # helpers to import/export data
    ###

    def load_data(self, data):
        """Load data into the ressource
        Args:
            data: the data to treat

        Returns:
            the treated data
        """
        self._lazy = False

        def idsNotNone(idsDict):
            """
            Test ids value are not none.

            :param idsDict: ids dict
            :return: True if None value found in the dict.
            """
            for idLabel, idvalue in idsDict.items():
                if idvalue is None:
                    return False
            return True

        def getRessource(rel, idRessource):
            """
            Get a ressource if ids aren't None

            :param rel: ressource subclass rel.
            :param idRessource: dict of ids of the ressource.
            :return: None if the ressources ids are None, the ressource instance if they aren't None.
            """
            if idsNotNone(idRessource):
                return rel.ressource_type.get().from_id(self._rest_client, idRessource, lazy=True)
            else:
                return None

        def convert(key, val):
            """Convert data into a ressource -> foreign key"""
            # have to be treated ?
            try:
                rel = getattr(self._rel, key)
            except AttributeError:
                return val

            # -> have to be treated
            if rel.many and isinstance(val, list):
                return [getRessource(rel, ress_id) for ress_id in val]
            else:
                return getRessource(rel, val)

        self._data = {k: convert(k, v) for k, v in data.items()}
        return self._data

    def dump_data(self):
        """Dump ressource to an understable form for the API"""
        def convert(key, val):
            """Convert a ressource into an understable form -> foreign keys"""
            # have to be treated ?
            try:
                rel = getattr(self._rel, key)
            except AttributeError:
                return val

            # -> have to be treated
            if rel.many and isinstance(val, list):
                return [ress.id for ress in val]
            else:
                return val.id

        data = {k: convert(k, v) for k, v in self._data.items()}

        return data


    ####
    # Wrappers around RestClient
    ####
    def save(self):
        """Allow to save locals changes to the server"""
        return self._rest_client.save(self)

    def get(self):
        """Allow to fetch datas from the server"""
        return self._rest_client.get(self)

    def remove(self):
        """Allow to delete the ressource on the server"""
        return self._rest_client.remove(self)

    def create(self):
        """Allow to create the ressource on the server"""
        return self._rest_client.create(self)

    @classmethod
    def where(cls, client, query):
        """Allow to get all instances of ressource that satisfy query (same format as RestClient.make_all)"""
        return client.make_all(cls._name, query)

    ###
    # Surcharge getter and setter for lazyness
    ###

    def __getattr__(self, item):
        if not item.startswith("_") and self._normal_getattr("_lazy"):
            self.get()
        return super().__getattr__(item)

    def __setattr__(self, item, value):
        if not item.startswith("_") and self._normal_getattr("_lazy"):
            self.get()
        return super().__setattr__(item, value)

    ####
    # Some special functions that are redefined
    ####

    def __eq__(left, right):
        return left._data == right._data

    def __str__(self):
        return str(self._data)

    def __repr__(self):
        return "{}({}, {}, lazy={})".format(self.__class__.__name__, self._rest_client, self.id, self._lazy)
