from opv_api_client.helpers import PropertyAsDict, MetaRessource

__all__ = ['Ressource']

class Ressource(PropertyAsDict, metaclass=MetaRessource):
    api_version = None
    name = None
    primary_keys = tuple()

    def __init__(self, rest_client, ids=None):
        """Warning, __init__ should be called at the very end of child's init - Won't works otherwise"""
        self.rest_client = rest_client

        if ids:
            data = {primary_key: id for primary_key, id in zip(self.primary_keys, ids)}
        else:
            data = {}

        # Create new attribute before this
        super().__init__(data)

    @property
    def id(self):
        """:obj: tuple or :obj: None: return the id of the ressource, if any"""
        try:
            return tuple(self.data[primary_key] for primary_key in self.primary_keys)
        except KeyError:  # Don't have a full ID, probably not created
            return None

    def __eq__(left, right):
        return left.data == right.data

    def __str__(self):
        return str(self.data)

    def save(self):
        """Allow to save locals changes to the server"""
        return self.rest_client.save(self)

    def get(self):
        """Allow to fetch datas from the server"""
        return self.rest_client.get(self)

    def remove(self):
        """Allow to delete the ressource on the server"""
        return self.rest_client.remove(self)

    def create(self):
        """Allow to create the ressource on the server"""
        return self.rest_client.create(self)

    @classmethod
    def where(cls, client, query):
        """Allow to get all instances of ressource that satisfy query (same format as RestClient.make_all)"""
        return client.make_all(cls.name, query)
