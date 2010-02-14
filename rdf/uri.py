import re
from xml.etree.ElementTree import QName
from lxml import etree

from rdf.blanknode import BlankNode


class URI(str):
    QNAME = re.compile(r'\{([^}]*)\}(.*)')

    def __new__(cls, uri=''):
        if isinstance(uri, (QName, etree.QName)):
            uri = str(uri)
            match = cls.QNAME.match(uri)
            if match:
                uri = match.group(1) + match.group(2)
        return super().__new__(cls, uri)

    def __repr__(self):
        return "URI({!r})".format(str(self))

    def __lt__(self, other):
        if other is None or isinstance(other, BlankNode):
            return False
        elif isinstance(other, URI):
            return super().__lt__(other)
        else:
            return NotImplemented

    def __gt__(self, other):
        if other is None or isinstance(other, BlankNode):
            return True
        elif isinstance(other, URI):
            return super().__gt__(other)
        else:
            return NotImplemented

