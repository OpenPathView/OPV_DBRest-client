from opv_api_client.helpers import PropertyAsDict, MetaRessource
from collections import OrderedDict


__all__ = ['Ressource']

class Ressource(PropertyAsDict, metaclass=MetaRessource):
    _api_version = None
    _name = None
    _primary_keys = tuple()

    class _rel:
        """A class that allow to add relationships"""

    def __init__(self, rest_client, ids=None):
        """Warning, __init__ should be called at the very end of child's init - Won't works otherwise"""
        self._rest_client = rest_client

        if ids:
            data = {primary_key: id for primary_key, id in zip(self._primary_keys, ids)}
        else:
            data = {}

        # Create new attribute before this
        super().__init__(data)

    @property
    def id(self):
        """:obj: tuple or :obj: None: return the id of the ressource, if any"""
        try:
            return OrderedDict((primary_key, self._data[primary_key]) for primary_key in self._primary_keys)
        except KeyError:  # Don't have a full ID, probably not created
            return None

    @classmethod
    def from_id(cls, c, data):
        ids = (data.get(i) for i in cls._primary_keys)
        return cls(c, ids)

    def load_data(self, data):
        """Load data into the ressource
        Args:
            data: the data to treat

        Returns:
            the treated data
        """

        def convert(key, val):
            """Convert data into a ressource -> foreign key"""
            # have to be treated ?
            try:
                rel = getattr(self._rel, key)
            except AttributeError:
                return val

            # -> have to be treated
            if rel.many and isinstance(val, list):
                return [rel.ressource_type.get().from_id(self._rest_client, ress_id) for ress_id in val]
            else:
                return rel.ressource_type.get().from_id(self._rest_client, val)

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

    def __eq__(left, right):
        return left._data == right._data

    def __str__(self):
        return str(self._data)

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
