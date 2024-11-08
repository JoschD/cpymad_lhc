""" 
Input/Output Tools
------------------

Tools to enable easy input and output operations with cpymad.
"""

class PathContainer:
    """ Class for easy access to stored paths and conversion to strings. """
    @classmethod
    def get(self, key, *args):
        return getattr(self, key).joinpath(*args)
        
    @classmethod
    def str(self, key, *args):
        return str(self.get(key, *args))