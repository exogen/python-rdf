import unittest
import re
try:
    from xml.etree import cElementTree as ElementTree
except ImportError:
    from xml.etree import ElementTree

from rdf.resource import Resource
from rdf.uri import URI
from rdf.namespace import Namespace, TEST, RDF, RDFS, XSD
from rdf.testcases.testcase import TestCase, Document
from util import open_data_file


TESTS = Namespace('http://www.w3.org/2000/10/rdf-tests/rdfcore/')

class TestTestCase(unittest.TestCase):
    def setUp(self):
        xml = open_data_file('Manifest.rdf').read()
        self.manifest = ElementTree.XML(xml)
        self.test = TestCase(self.manifest.find(str(self.tag)))

    def assertTextEqual(self, a, b):
        ws = re.compile(r'\s+')
        return self.assertEqual(ws.sub(' ', a), ws.sub(' ', b))

class TestPositiveParserTest(TestTestCase):
    def setUp(self):
        self.tag = ElementTree.QName(TEST, 'PositiveParserTest')
        super().setUp()

    def test_test_is_test_case(self):
        self.assert_(isinstance(self.test, TestCase))

    def test_test_uri(self):
        self.assertEqual(self.test.uri,
            TESTS['amp-in-url/Manifest.rdf#test001'])

    def test_test_type(self):
        self.assertEqual(self.test.type, TEST.PositiveParserTest)

    def test_test_status(self):
        self.assertEqual(self.test.status, 'APPROVED')

    def test_test_description(self):
        self.assertEqual(self.test.description, None)

    def test_test_input_documents(self):
        self.assertEqual(set(self.test.input_documents),
            {Document(TEST['RDF-XML-Document'],
                      TESTS['amp-in-url/test001.rdf'])})

    def test_test_output_document(self):
        self.assertEqual(self.test.output_document,
            Document(TEST['NT-Document'], TESTS['amp-in-url/test001.nt']))

class TestNegativeEntailmentTest(TestTestCase):
    def setUp(self):
        self.tag = ElementTree.QName(TEST, 'NegativeEntailmentTest')
        super().setUp()

    def test_test_is_test_case(self):
        self.assert_(isinstance(self.test, TestCase))

    def test_test_uri(self):
        self.assertEqual(self.test.uri,
            TESTS['datatypes-intensional/Manifest.rdf#xsd-integer-decimal-compatible'])

    def test_test_type(self):
        self.assertEqual(self.test.type, TEST.NegativeEntailmentTest)

    def test_test_status(self):
        self.assertEqual(self.test.status, 'APPROVED')

    def test_test_description(self):
        self.assertTextEqual(self.test.description,
            " The claim that xsd:integer is a subClassOF xsd:decimal is not"
            " incompatible with using the intensional semantics for datatypes. ")

    def test_test_entailment_rules(self):
        self.assertEqual(set(self.test.entailment_rules),
            {RDF, RDFS, TESTS['datatypes#']})

    def test_test_datatype_support(self):
        self.assertEqual(set(self.test.datatype_support),
            {XSD.integer, XSD.decimal})

    def test_test_premise_documents(self):
        self.assertEqual(set(self.test.premise_documents),
            {Document(TEST['NT-Document'],
                      TESTS['datatypes-intensional/test001.nt'])})

    def test_test_conclusion_document(self):
        self.assertEqual(self.test.conclusion_document,
            Document(TEST['False-Document']))

class TestPositiveEntailmentTest(TestTestCase):
    def setUp(self):
        self.tag = ElementTree.QName(TEST, 'PositiveEntailmentTest')
        super().setUp()

    def test_test_is_test_case(self):
        self.assert_(isinstance(self.test, TestCase))

    def test_test_uri(self):
        self.assertEqual(self.test.uri,
            TESTS['datatypes-intensional/Manifest.rdf#xsd-integer-string-incompatible'])

    def test_test_type(self):
        self.assertEqual(self.test.type, TEST.PositiveEntailmentTest)

    def test_test_status(self):
        self.assertEqual(self.test.status, 'APPROVED')

    def test_test_description(self):
        self.assertTextEqual(self.test.description,
            " The claim that xsd:integer is a subClassOF xsd:string is"
            " incompatible with using the intensional semantics for datatypes. ")

    def test_test_entailment_rules(self):
        self.assertEqual(set(self.test.entailment_rules),
            {RDF, RDFS, TESTS['datatypes#']})

    def test_test_datatype_support(self):
        self.assertEqual(set(self.test.datatype_support),
            {XSD.integer, XSD.string})

    def test_test_premise_documents(self):
        self.assertEqual(set(self.test.premise_documents),
            {Document(TEST['NT-Document'],
                      TESTS['datatypes-intensional/test002.nt'])})

    def test_test_conclusion_document(self):
        self.assertEqual(self.test.conclusion_document,
            Document(TEST['False-Document']))

class TestNegativeParserTest(TestTestCase):
    def setUp(self):
        self.tag = ElementTree.QName(TEST, 'NegativeParserTest')
        super().setUp()

    def test_test_is_test_case(self):
        self.assert_(isinstance(self.test, TestCase))

    def test_test_uri(self):
        self.assertEqual(self.test.uri, TESTS['rdf-charmod-literals/Manifest.rdf#error001'])

    def test_test_type(self):
        self.assertEqual(self.test.type, TEST.NegativeParserTest)

    def test_test_status(self):
        self.assertEqual(self.test.status, 'WITHDRAWN')

    def test_test_description(self):
        self.assertTextEqual(self.test.description,
            " Does the treatment of literals conform to charmod ?"
            " Test for failure for literal not in Normal Form C"
            " This test case has been WITHDRAWN in light of changes to NFC handling in concepts ")

    def test_test_input_documents(self):
        self.assertEqual(set(self.test.input_documents),
            {Document(TEST['RDF-XML-Document'],
                      TESTS['rdf-charmod-literals/error001.rdf'])})

