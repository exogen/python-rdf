import re
from xml.etree.ElementTree import QName


class URI(str):
    QNAME = re.compile(r'\{([^}]*)\}(.*)')

    def __new__(cls, uri=''):
        if isinstance(uri, QName):
            uri = str(uri)
            match = cls.QNAME.match(uri)
            if match:
                uri = match.group(1) + match.group(2)
        return super().__new__(cls, uri)

    def __repr__(self):
        return "URI({!r})".format(str(self))

