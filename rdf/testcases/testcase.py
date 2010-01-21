import unittest
from xml.etree.ElementTree import QName

from rdf.resource import Resource
from rdf.uri import URI
from rdf.namespace import RDF, TEST
from rdf.testcases.document import Document


class TestCase(unittest.TestCase):
    _element = None
    path_map = None

    @classmethod
    def from_element(cls, element):
        type = URI(QName(element.tag))
        cls = {TEST.PositiveParserTest: PositiveParserTest,
               TEST.NegativeParserTest: NegativeParserTest,
               TEST.PositiveEntailmentTest: PositiveEntailmentTest,
               TEST.NegativeEntailmentTest: NegativeEntailmentTest}.get(type, cls)
        test = cls()
        test._element = element
        return test

    def setUp(self):
        if self._element is None:
            self.skipTest("_element not set: no test data found")
        elif self.status != 'APPROVED':
            self.skipTest("test status is {0.status}".format(self))

    def runTest(self):
        raise NotImplementedError

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
    def description(self):
        element = self._element.find(str(QName(TEST, 'description')))
        if element is not None:
            return element.text

    @property
    def warning(self):
        element = self._element.find(str(QName(TEST, 'warning')))
        if element is not None:
            return element.text

class ParserTest(TestCase):
    @property
    def input_documents(self):
        element = self._element.find(str(QName(TEST, 'inputDocument')))
        if element is not None:
            for doc in element:
                yield Document(QName(doc.tag), doc.get(QName(RDF, 'about')))

    def setUp(self):
        super().setUp()

class PositiveParserTest(ParserTest):
    @property
    def output_document(self):
        element = self._element.find(str(QName(TEST, 'outputDocument')))
        if element is not None:
            for doc in element:
                return Document(QName(doc.tag), doc.get(QName(RDF, 'about')))

    def setUp(self):
        super().setUp()

class NegativeParserTest(ParserTest):
    def runTest(self):
        for input_document in self.input_documents:
            file = input_document.open(self.path_map)
            reader = input_document.get_reader()
            self.assertRaises(reader.ParseError, reader.read, file)

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

    @property
    def premise_documents(self):
        element = self._element.find(str(QName(TEST, 'premiseDocument')))
        if element is not None:
            for doc in element:
                yield Document(QName(doc.tag), doc.get(QName(RDF, 'about')))
    @property
    def conclusion_document(self):
        element = self._element.find(str(QName(TEST, 'conclusionDocument')))
        if element is not None:
            for doc in element:
                return Document(QName(doc.tag), doc.get(QName(RDF, 'about')))

class PositiveEntailmentTest(EntailmentTest):
    pass

class NegativeEntailmentTest(EntailmentTest):
    pass

