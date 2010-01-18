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
                resource = Resource(doc.get(QName(RDF, 'about')))
                resource.type = TEST['RDF-XML-Document']
                yield resource

    @property
    def output_document(self):
        element = self._element.find(str(QName(TEST, 'outputDocument')))
        if element is not None:
            return element.text

