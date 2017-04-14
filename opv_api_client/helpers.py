from opv_api_client.filter import Filter

class MetaPropertyAsDict(type):
    def __call__(*args, **kwargs):  # called when you do a ClassName()
        obj = type.__call__(*args, **kwargs)
        obj._init = True
        return obj

class MetaRessource(MetaPropertyAsDict):
    def __getattr__(cls, name):
        """Getters used when the class isn't instancied
        Allow to make filtering easy
        e.g ressources.Lot.id_malette == 1 same as Filter("id_malette").op("eq").value(1)
        """
        return Filter(name)

class PropertyAsDict(metaclass=MetaPropertyAsDict):
    """
    A class that
    Thanks to the Metaclass, when __init__ is ended, you can't create new varible, except thanks to __normal_setattr
    """
    _alias = {}

    def __init__(self, data=None):
        if data:
            self._data = data
        else:
            self._data = {}

    def __getattr__(self, item):
        try:
            return self._data[item]
        except KeyError:
            pass
        try:  # to find the item in alias
            return self._data[self._alias[item]]
        except KeyError:
            pass

        return self.__getattribute__(item)  # use normal way finally

    def __setattr__(self, item, value):
        """Set to value self.item if it exists, otherwise, self.data[item].
        If self._init = False, then set to value self.item in any case"""

        # _init is set, set self.item to value
        if "_init" not in self.__dict__:
            super().__setattr__(item, value)

        # set self.item to value
        # self.__class__.__dir__ list all statics attributes
        # self.__dict__ list all instances attributes
        elif item in self.__class__.__dir__(self) + list(self.__dict__.values()):
            super().__setattr__(item, value)

        # search now in self.data
        else:
            item = self._alias.get(item, item)  # if is an alias, get the real name
            self._data[item] = value

    def __normal_getattr(self, item):
        super().__getattribute__(item)

    def __normal_setattr(self, item, value):
        super().__setattr__(item, value)
