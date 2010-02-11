import os.path
from xml.etree.ElementTree import QName
from urllib.request import urlopen, OpenerDirector, URLError

from rdf.uri import URI
from rdf.namespace import RDF, TEST
from rdf.syntax.rdfxml import RDFXMLReader
from rdf.syntax.ntriples import NTriplesReader


class Document:
    def __init__(self, type, uri=None):
        self.type = URI(type)
        self.uri = URI(uri) if uri is not None else uri

    @classmethod
    def from_element(cls, element):
        return cls(QName(element.tag), element.get(QName(RDF, 'about')))

    def __repr__(self):
        return "Document({!r}, {!r})".format(self.type, self.uri)

    def __eq__(self, other):
        return (isinstance(other, Document) and
                other.type == self.type and
                other.uri == self.uri)

    def __hash__(self):
        return hash(Document) ^ hash(self.type) ^ hash(self.uri)

    def open(self, opener=urlopen):
        if self.uri is not None:
            if isinstance(opener, OpenerDirector):
                opener = opener.open
            return opener(self.uri)
        else:
            raise URLError(self.uri)

    def read(self, opener=urlopen):
        return self.get_reader().read(self.open(opener), self.uri)

    def get_reader(self):
        if self.type == TEST['NT-Document']:
            return NTriplesReader()
        elif self.type == TEST['RDF-XML-Document']:
            return RDFXMLReader()
        else:
            raise RuntimeError("No reader for type {!s}".format(self.type))

