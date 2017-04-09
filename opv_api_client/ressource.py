from opv_api_client.helpers import PropertyAsDict

__all__ = ['Ressource']

class Ressource(PropertyAsDict):
    api_version = None
    name = None
    primary_keys = tuple()

    def __init__(self, rest_client, ids=None):
        """Warning, __init__ should be called at the very end of child's init - Won't works otherwise"""
        self.rest_client = rest_client

        data = {primary_key: id for primary_key, id in zip(self.primary_keys, ids)}

        # Create new attribute before this
        super().__init__(data)

    @property
    def id(self):
        return tuple(self.data[primary_key] for primary_key in self.primary_keys)

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
