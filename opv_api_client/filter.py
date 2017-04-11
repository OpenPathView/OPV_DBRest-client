from functools import partial

def _make_op(op):
    def f(self, val):
        self.op(op)
        self.value(val)
        return self
    return f

class Filter:
    """Add primitives that simplify filtering in ressource"""
    def op(self, op):
        self._op = op
        return self

    def name(self, name):
        self._name = name
        return self

    def value(self, value):
        self._value = value
        return self

    val = value

    def get(self):
        """Return the filter """
        return {"name": self._name, "op": self._op, "val": str(self._value)}

    def __init__(self, name=None):
        if name:
            self._name = name

    __eq__ = _make_op("eq")
    __ne__ = _make_op("neq")

    __lt__ = _make_op("lt")
    __gt__ = _make_op("gt")

    __le__ = _make_op("le")
    __ge__ = _make_op("ge")

    # TODO: like, is_null, is_not_null, like, has, any

def treat_query(query):
    """a query may be: a list of query, """
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
