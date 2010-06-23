import sys

class UniversalSet(frozenset):
    """A set which (claims to) contain everything, even itself.

    The size of the set reported by len() is sys.maxsize, as no greater
    integer may be returned.

    """
    def __contains__(self, obj):
        return True

    def __len__(self):
        return sys.maxsize # Can't return infinity or greater than this.

