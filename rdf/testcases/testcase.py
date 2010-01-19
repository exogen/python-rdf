from xml.etree.ElementTree import QName

from rdf.resource import Resource
from rdf.uri import URI
from rdf.namespace import RDF, TEST


class TestCase:
    def __new__(cls, element):
        type = URI(QName(element.tag))
        cls = {TEST.PositiveParserTest: PositiveParserTest,
               TEST.NegativeParserTest: NegativeParserTest,
               TEST.PositiveEntailmentTest: PositiveEntailmentTest,
               TEST.NegativeEntailmentTest: NegativeEntailmentTest}.get(type, cls)
        return super().__new__(cls)

    def __init__(self, element):
        self._element = element

    @property
    def type(self):
        return URI(QName(self._element.tag))

    @property
    def uri(self):
        return URI(self._element.get(QName(RDF, 'about')))

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

class ParserTest(TestCase):
    @property
    def input_documents(self):
        element = self._element.find(str(QName(TEST, 'inputDocument')))
        if element is not None:
            for doc in element:
                yield Document(QName(doc.tag), doc.get(QName(RDF, 'about')))

class PositiveParserTest(ParserTest):
    @property
    def output_document(self):
        element = self._element.find(str(QName(TEST, 'outputDocument')))
        if element is not None:
            for doc in element:
                return Document(QName(doc.tag), doc.get(QName(RDF, 'about')))

class NegativeParserTest(ParserTest):
    pass

class EntailmentTest(TestCase):
    @property
    def entailment_rules(self):
        for element in self._element.findall(str(QName(TEST, 'entailmentRules'))):
            uri = element.get(QName(RDF, 'resource'))
            if uri is not None:
                yield URI(uri)

    @property
    def datatype_support(self):
        for element in self._element.findall(str(QName(TEST, 'datatypeSupport'))):
            uri = element.get(QName(RDF, 'resource'))
            if uri is not None:
                yield URI(uri)

class PositiveEntailmentTest(EntailmentTest):
    pass

class NegativeEntailmentTest(EntailmentTest):
    pass

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

