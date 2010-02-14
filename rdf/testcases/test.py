import unittest
from xml.etree.ElementTree import QName

from rdf.uri import URI
from rdf.namespace import RDF, TEST
from rdf.testcases.document import Document


__all__ = ['Test', 'PositiveParserTest', 'NegativeParserTest',
           'PositiveEntailmentTest', 'NegativeEntailmentTest',
           'MiscellaneousTest']

class Test:
    TYPE_MAP = {}

    def __new__(cls, type, uri):
        type_class = cls.TYPE_MAP.get(type, cls)
        return super().__new__(type_class)

    def __init__(self, type, uri):
        self.type = type
        self.uri = uri
        self.status = None
        self.description = None
        self.warning = None

    @classmethod
    def from_element(cls, element):
        type = URI(QName(element.tag))
        uri = URI(element.get(QName(RDF, 'about')))
        type_class = cls.TYPE_MAP.get(type, cls)
        if cls is type_class:
            test = cls(type, uri)
            test.status = cls._status(element)
            test.description = cls._description(element)
            test.warning = cls._warning(element)
        else:
            test = type_class.from_element(element)
        return test

    @classmethod
    def _status(cls, element):
        element = element.find(str(QName(TEST, 'status')))
        if element is not None:
            return element.text

    @classmethod
    def _description(cls, element):
        element = element.find(str(QName(TEST, 'description')))
        if element is not None:
            return element.text

    @classmethod
    def _warning(cls, element):
        element = element.find(str(QName(TEST, 'warning')))
        if element is not None:
            return element.text

class ParserTest(Test):
    @classmethod
    def _input_documents(cls, element):
        for parent in element.findall(str(QName(TEST, 'inputDocument'))):
            for child in parent:
                yield Document.from_element(child)

class PositiveParserTest(ParserTest):
    def __init__(self, type, uri):
        super().__init__(type, uri)
        self.input_documents = set()
        self.output_document = None

    @classmethod
    def from_element(cls, element):
        test = super().from_element(element)
        test.input_documents = set(cls._input_documents(element))
        test.output_document = cls._output_document(element)
        return test

    @classmethod
    def _output_document(cls, element):
        for parent in element.findall(str(QName(TEST, 'outputDocument'))):
            for child in parent:
                return Document.from_element(child)

class NegativeParserTest(ParserTest):
    def __init__(self, type, uri):
        super().__init__(type, uri)
        self.input_document = None

    @classmethod
    def from_element(cls, element):
        test = super().from_element(element)
        test.input_document = next(iter(cls._input_documents(element)), None)
        return test

class EntailmentTest(Test):
    def __init__(self, type, uri):
        super().__init__(type, uri)
        self.entailment_rules = set()
        self.datatype_support = set()
        self.premise_documents = set()
        self.conclusion_document = None

    @classmethod
    def from_element(cls, element):
        test = super().from_element(element)
        test.entailment_rules = set(cls._entailment_rules(element))
        test.datatype_support = set(cls._datatype_support(element))
        test.premise_documents = set(cls._premise_documents(element))
        test.conclusion_document = cls._conclusion_document(element)
        return test

    @classmethod
    def _entailment_rules(cls, element):
        for child in element.findall(str(QName(TEST, 'entailmentRules'))):
            uri = child.get(QName(RDF, 'resource'))
            if uri is not None:
                yield URI(uri)

    @classmethod
    def _datatype_support(cls, element):
        for child in element.findall(str(QName(TEST, 'datatypeSupport'))):
            uri = child.get(QName(RDF, 'resource'))
            if uri is not None:
                yield URI(uri)

    @classmethod
    def _premise_documents(cls, element):
        for parent in element.findall(str(QName(TEST, 'premiseDocument'))):
            for child in parent:
                yield Document.from_element(child)

    @classmethod
    def _conclusion_document(cls, element):
        for parent in element.findall(str(QName(TEST, 'conclusionDocument'))):
            for child in parent:
                return Document.from_element(child)

class PositiveEntailmentTest(EntailmentTest):
    pass

class NegativeEntailmentTest(EntailmentTest):
    pass

class MiscellaneousTest(Test):
    def __init__(self, type, uri):
        super().__init__(type, uri)
        self.documents = set()
    
    @classmethod
    def from_element(cls, element):
        test = super().from_element(element)
        test.documents = set(cls._documents(element))
        return test

    @classmethod
    def _documents(cls, element):
        for parent in element.findall(str(QName(TEST, 'document'))):
            for child in parent:
                yield Document.from_element(child)

Test.TYPE_MAP.update({
    TEST.PositiveParserTest: PositiveParserTest,
    TEST.NegativeParserTest: NegativeParserTest,
    TEST.PositiveEntailmentTest: PositiveEntailmentTest,
    TEST.NegativeEntailmentTest: NegativeEntailmentTest,
    TEST.MiscellaneousTest: MiscellaneousTest})

