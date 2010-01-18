from xml.etree.ElementTree import QName

from rdf.resource import Resource
from rdf.uri import URI
from rdf.namespace import RDF, TEST


class TestCase:
    def __init__(self, element):
        self._element = element

    @property
    def uri(self):
        return self._element.get(QName(RDF, 'about'))

    @property
    def status(self):
        element = self._element.find(str(QName(TEST, 'status')))
        if element is not None:
            return element.text

    @property
    def approval(self):
        element = self._element.find(str(QName(TEST, 'approval')))
        if element is not None:
            uri = element.get(QName(RDF, 'resource'))
            if uri is not None:
                return URI(uri)

    @property
    def description(self):
        element = self._element.find(str(QName(TEST, 'description')))
        if element is not None:
            return element.text

    @property
    def input_documents(self):
        element = self._element.find(str(QName(TEST, 'inputDocument')))
        if element is not None:
            for doc in element:
                yield Document(QName(doc.tag), doc.get(QName(RDF, 'about')))

    @property
    def output_document(self):
        element = self._element.find(str(QName(TEST, 'outputDocument')))
        if element is not None:
            for doc in element:
                return Document(QName(doc.tag), doc.get(QName(RDF, 'about')))


class Document:
    def __init__(self, type, uri):
        self.type = URI(type)
        self.uri = URI(uri)

    def __repr__(self):
        return "Document({!r}, {!r})".format(self.type, self.uri)

    def __eq__(self, other):
        return (isinstance(other, Document) and
                other.type == self.type and
                other.uri == self.uri)

    def __hash__(self):
        return hash(Document) ^ hash(self.type) ^ hash(self.uri)

