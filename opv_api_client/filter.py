def _make_op(op):
    def f(self, val):
        self.op(op)
        self.value(val)
        return self
    return f

class Filter:
    """Add primitives that simplify filtering in ressource

    This allow to use filters easily. Filter are (nowaday) constitued of 3 fields:
        - op
        - name
        - value
    To set those values, you can respectively use the `op`, `name` and `val`/`value` fonction to set those

    """
    def op(self, op):
        """Allow to set the op's field of the filter

        Args:
            op(str): The name of the operation
        Return:
            Filter: return the modifyed Filter(self)
        """
        self._op = op
        return self

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
        return {"name": self._name, "op": self._op, "val": str(self._value)}

    def __init__(self, name=None):
        self._name = name
        self._op = None
        self._value = None

    __eq__ = _make_op("eq")
    __ne__ = _make_op("neq")

    __lt__ = _make_op("lt")
    __gt__ = _make_op("gt")

    __le__ = _make_op("le")
    __ge__ = _make_op("ge")

    # TODO: like, is_null, is_not_null, like, has, any

def treat_query(query):
    """A fonction that get filters and transform it into a form understable by the API

    Will, for each founded Filter, do a filter.get() and will append the result to the final list.

    Args:
        query(:obj: list or :obj: Filter): The query to treat
    Returns:
        list: A list of filters, in a form understable by the API
    """
    if isinstance(query, Filter):
        return [query.get()]

    if isinstance(query, dict):
        return [query]

    try:
        iter(query)  # is iterable ?
    except TypeError:  # isn't iterable
        pass
    else:
        # recursively treat queries and flatten the list
        return sum((treat_query(q) for q in query), [])
