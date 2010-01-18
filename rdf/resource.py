import abc
from xml.etree.ElementTree import QName

from rdf.blanknode import BlankNode
from rdf.uri import URI

class Resource(metaclass=abc.ABCMeta):
    def __new__(cls, uri=None):
        if uri is not None:
            return URI(uri)
        else:
            return BlankNode()

Resource.register(BlankNode)
Resource.register(URI)
