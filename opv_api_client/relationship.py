__all__ = ["Relationship"]

class Relationship:

    """A class that allow to modelize Relationships between ressources"""

    def __init__(self, ressource_type, *, many=False):
        """The initializer of the Relationship

        Arg:
            ressource_type(RessourceEnum): The type of the ressource linked by the Relationship
        Kwarg:
            many (bool): A boolean value that allow to say if it's a single value or a list of values
        """
        self.ressource_type = ressource_type
        self.many = many
