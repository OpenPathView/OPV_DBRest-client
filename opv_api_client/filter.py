class Filter:
    """Add primitives that simplify filtering in ressource

    This allow to use filters easily. Filter are (nowaday) constitued of 3 fields:
        - name
        - value
    To set those values, you can respectively use the `name` and `val`/`value` fonction to set those

    """
    _url_modifier = 0
    _eq = 1

    def name(self, name):
        """Allow to set the name's field of the filter

        Args:
            name(str): The name of the field on which will be applied the operation
        Return:
            Filter: return the modifyed Filter(self)
        """
        self._name = name
        return self

    def value(self, value):
        """Allow to set the value's field of the filter

        Args:
            value: the value
        Return:
            Filter: return the modifyed Filter(self)
        """
        self._value = value
        return self

    val = value
    """A shortcut for `value`"""

    def get(self):
        """Return the filter

        Allow to get the final filter, in a form that can directly be used by the API
        """
        if self._type == self._url_modifier:
            return {"_url": self._url}

        return {self._name: self._value}

    @classmethod
    def within(cls, ids, meters):
        """Returns a filter that allow to integrate with ST_within"""
        f = cls()

        f._type = cls._url_modifier
        f._url = "/" + "/".join(map(str, ids)) + "/within/" + str(meters)  # should use client._gen_id
        return f

    def __init__(self, name=None):
        self._name = name
        self._value = None
        self._type = self._eq

    __eq__ = value

def treat_query(query):
    """A fonction that get filters and transform it into a form understable by the API

    Will, for each founded Filter, do a filter.get() and will append the result to the final list.

    Args:
        query(:obj: list or :obj: Filter): The query to treat
    Returns:
        dict: A dict of filters, in a form understable by the API -> now is a the param dict
    """
    if isinstance(query, Filter):
        return query.get()

    # recursively treat queries and flatten the dict
    return dict(
        sum(  # get a list of keys/value (tuple)
            (list(q.get().items()) for q in query),
            []
        )
    )
