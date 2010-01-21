import os.path
from urllib.request import urlopen

from rdf.uri import URI
from rdf.namespace import TEST
from rdf.rdfxml import RDFXMLReader
from rdf.ntriples import NTriplesReader

class Document:
    def __init__(self, type, uri=None):
        if uri is not None:
            uri = URI(uri)
        self.type = URI(type)
        self.uri = uri

    def __repr__(self):
        return "Document({!r}, {!r})".format(self.type, self.uri)

    def __eq__(self, other):
        return (isinstance(other, Document) and
                other.type == self.type and
                other.uri == self.uri)

    def __hash__(self):
        return hash(Document) ^ hash(self.type) ^ hash(self.uri)

    def open(self, path_map=None, mode='r'):
        if self.uri is not None:
            if path_map is not None:
                return open(self.get_path(path_map), mode=mode)
            else:
                return urlopen(self.uri)
        else:
            raise RuntimeError("Document cannot be opened (no URI)")

    def read(self, path_map=None, mode='r'):
        return self.get_reader().read(self.open(path_map, mode))

    def get_path(self, path_map):
        for prefix, head in path_map.items():
            if self.uri.startswith(prefix):
                tail = self.uri[len(prefix):]
                return os.path.join(head, tail)
        raise RuntimeError("No mapping for URI: {!s}".format(self.uri))

    def get_reader(self):
        if self.type == TEST['NT-Document']:
            return NTriplesReader()
        elif self.type == TEST['RDF-XML-Document']:
            return RDFXMLReader()
        else:
            raise RuntimeError("No reader for type {!s}".format(self.type))

