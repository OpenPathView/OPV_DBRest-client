
class PropertyAsDict():
    """The internal dict self.data can be accessed as if it were a normal propoerty
    e.g:
    >>> p = PropertyAsDict()
    >>> p.data["truc"] = "bidule"
    >>> self.truc
    bidule
    >>> p.truc = "machin"
    >>> p.data['truc']
    machin

    Also provides alias via alias attribute
    e.g
    >>> p.alias = {"machin": "truc"}
    >>> p.truc is p.machin
    True
    """
    alias = {}
    def __init__(self, data=None):
        # after this, can't create new attribute in self -> will be create in self.data
        # can be bypassed, using __normal_setattr(item_name, new_value) / __normal_getattr(item_name)
        if data:
            self.data = data
        else:
            self.data = {}

        self._init = True

    # Adapted from http://code.activestate.com/recipes/389916-example-setattr-getattr-overloading/
    def __getattr__(self, item):
        """Maps values to attributes.
        Only called if there *isn't* an attribute with this name
        """
        try:
            return self.data[item]
        except KeyError:
            pass
        try:  # to find the item in alias
            return self.data[self.alias[item]]
        except KeyError:
            pass

        return self.__getattribute__(item)  # use normal way finally

    def __setattr__(self, item, value):
        """Maps attributes to values.
        Only if we are initialised
        """
        # allow to init some interns values in __init__
        if "_init" not in self.__dict__:
            super().__setattr__(item, value)

        # any normal attributes are handled normally
        elif item in self.__class__.__dir__(self):  # list all attribute, including class attribute (works better than __dict)
            super().__setattr__(item, value)

        # search now in self.data
        else:
            item = self.alias.get(item, item)  # if is an alias, get the real name
            self.data[item] = value

    def __normal_getattr(self, item):
        super().__getattribute__(item)

    def __normal_setattr(self, item, value):
        super().__setattr__(item, value)
