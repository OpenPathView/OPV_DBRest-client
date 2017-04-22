from opv_api_client.filter import Filter

class MetaRessource(type):
    def __getattr__(cls, name):
        """Getters used when the class isn't instancied
        Allow to make filtering easy
        e.g ressources.Lot.id_malette == 1 same as Filter("id_malette").op("eq").value(1)
        """
        return Filter(name)

class PropertyAsDict():
    """
    All properties are fetch in data, except if they start with _
    """
    _alias = {}

    def __getattr__(self, item):
        if item.startswith('_'):
            return self.__getattribute__(item)

        item = self._alias.get(item, item)  # if is an alias, get the real name
        try:
            return self._data[item]
        except KeyError:
            return super().__getattribute__(item)  # will raise AttributeError

    def __setattr__(self, item, value):
        """If item startwith _, set self.item else, set self._raw_data[item]"""
        if item.startswith('_'):
            super().__setattr__(item, value)
            return

        item = self._alias.get(item, item)  # if is an alias, get the real name
        self._data[item] = value

    def _normal_getattr(self, item):
        return super().__getattribute__(item)

    def _normal_setattr(self, item, value):
        super().__setattr__(item, value)
