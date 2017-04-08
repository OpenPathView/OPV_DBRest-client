class Ressource(dict):
    api_version = None
    name = None
    primary_keys = tuple()
    alias = {}  # Allow to alias things. e.g alias = {"a": "b"} -> ress["a"] will return ress["b"]

    def __init__(self, rest_client, ids=None):
        """Warning, __init__ should be called at the very end of child's init - Won't works otherwise"""
        self.rest_client = rest_client
        super().__init__()

        self.update({primary_key: id for primary_key, id in zip(self.primary_keys, ids)})

        self._init = True

    @property
    def id(self):
        return tuple(self[primary_key] for primary_key in self.primary_keys)

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

    # Adapted from http://code.activestate.com/recipes/389916-example-setattr-getattr-overloading/
    def __getattr__(self, item):
        """Maps values to attributes.
        Only called if there *isn't* an attribute with this name
        """
        try:
            return self.__getitem__(item)
        except KeyError:
            pass

        return self.__getattribute__(item)  # use normal way finally

    def __getitem__(self, item):
        try:
            return self.__getitem__(self.alias[item])
        except KeyError:
            pass

        return super().__getitem__(item)

    def __setattr__(self, item, value):
        """Maps attributes to values.
        Only if we are initialised
        """
        if "_init" not in self.__dict__:  # allow to init some interns values in __init__
            dict.__setattr__(self, item, value)
        if item in self.__dict__:       # any normal attributes are handled normally
            dict.__setattr__(self, item, value)
        else:
            self.__setitem__(item, value)

    def __setitem__(self, item, value):
        """If item is an alias, change the real value"""
        item = self.alias.get(item, item)
        super().__setitem__(item, value)
