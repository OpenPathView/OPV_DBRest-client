
__all__ = ["register", "RessourceProxy"]

class RessourceProxy:
    """A class that allow to reference a reference without crash if it don't exist for the moment"""
    def __init__(self, ressource_name):
        self.ressource_name = ressource_name

    def get(self):
        """Get the real version of the object"""
        return ressources[self.ressource_name]

def register(obj):
    """A decorator that append an object to the list of ressources"""
    ressources[obj._name] = obj
    return obj  # don't modify onject


ressources = {}
