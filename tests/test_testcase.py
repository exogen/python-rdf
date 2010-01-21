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
from util import open_data_file, TESTS, PATH_MAP


class TestTestCase(unittest.TestCase):
    tag = None

    def setUp(self):
        xml = open_data_file('Manifest.rdf').read()
        self.manifest = ElementTree.XML(xml)
        if self.tag is not None:
            self.element = self.manifest.find(str(self.tag))
            self.test = TestCase.from_element(self.element)
        else:
            self.skipTest("abstract test case (tag not set)")

    def assertTextEqual(self, a, b):
        ws = re.compile(r'\s+')
        return self.assertEqual(ws.sub(' ', a), ws.sub(' ', b))

    def test_is_test_case(self):
        self.assert_(isinstance(self.test, TestCase))

    def test_is_unittest_test_case(self):
        self.assert_(isinstance(self.test, unittest.TestCase))

class TestPositiveParserTest(TestTestCase):
    tag = ElementTree.QName(TEST, 'PositiveParserTest')

    def test_has_uri(self):
        self.assertEqual(self.test.uri,
                         TESTS['amp-in-url/Manifest.rdf#test001'])

    def test_has_type(self):
        self.assertEqual(self.test.type, TEST.PositiveParserTest)

    def test_has_status(self):
        self.assertEqual(self.test.status, 'APPROVED')

    def test_has_description(self):
        self.assertEqual(self.test.description, None)

    def test_has_input_documents(self):
        self.assertEqual(set(self.test.input_documents),
                         {Document(TEST['RDF-XML-Document'],
                                   TESTS['amp-in-url/test001.rdf'])})

    def test_has_output_document(self):
        self.assertEqual(self.test.output_document,
                         Document(TEST['NT-Document'],
                                  TESTS['amp-in-url/test001.nt']))

class TestNegativeEntailmentTest(TestTestCase):
    tag = ElementTree.QName(TEST, 'NegativeEntailmentTest')

    def test_has_uri(self):
        self.assertEqual(self.test.uri,
            TESTS['datatypes-intensional/Manifest.rdf#xsd-integer-decimal-compatible'])

    def test_has_type(self):
        self.assertEqual(self.test.type, TEST.NegativeEntailmentTest)

    def test_has_status(self):
        self.assertEqual(self.test.status, 'APPROVED')

    def test_has_description(self):
        self.assertTextEqual(self.test.description,
            " The claim that xsd:integer is a subClassOF xsd:decimal is not"
            " incompatible with using the intensional semantics for datatypes. ")

    def test_has_entailment_rules(self):
        self.assertEqual(set(self.test.entailment_rules),
                         {RDF, RDFS, TESTS['datatypes#']})

    def test_has_datatype_support(self):
        self.assertEqual(set(self.test.datatype_support),
                         {XSD.integer, XSD.decimal})

    def test_has_premise_documents(self):
        self.assertEqual(set(self.test.premise_documents),
                         {Document(TEST['NT-Document'],
                                   TESTS['datatypes-intensional/test001.nt'])})

    def test_has_conclusion_document(self):
        self.assertEqual(self.test.conclusion_document,
                         Document(TEST['False-Document']))

class TestPositiveEntailmentTest(TestTestCase):
    tag = ElementTree.QName(TEST, 'PositiveEntailmentTest')

    def test_has_uri(self):
        self.assertEqual(self.test.uri,
            TESTS['datatypes-intensional/Manifest.rdf#xsd-integer-string-incompatible'])

    def test_has_type(self):
        self.assertEqual(self.test.type, TEST.PositiveEntailmentTest)

    def test_has_status(self):
        self.assertEqual(self.test.status, 'APPROVED')

    def test_has_description(self):
        self.assertTextEqual(self.test.description,
            " The claim that xsd:integer is a subClassOF xsd:string is"
            " incompatible with using the intensional semantics for datatypes. ")

    def test_has_entailment_rules(self):
        self.assertEqual(set(self.test.entailment_rules),
                         {RDF, RDFS, TESTS['datatypes#']})

    def test_has_datatype_support(self):
        self.assertEqual(set(self.test.datatype_support),
                         {XSD.integer, XSD.string})

    def test_has_premise_documents(self):
        self.assertEqual(set(self.test.premise_documents),
                         {Document(TEST['NT-Document'],
                                   TESTS['datatypes-intensional/test002.nt'])})

    def test_has_conclusion_document(self):
        self.assertEqual(self.test.conclusion_document,
                         Document(TEST['False-Document']))

class TestNegativeParserTest(TestTestCase):
    tag = ElementTree.QName(TEST, 'NegativeParserTest')

    def setUp(self):
        super().setUp()
        self.test.path_map = PATH_MAP

    def test_has_uri(self):
        self.assertEqual(self.test.uri, TESTS['rdf-charmod-literals/Manifest.rdf#error001'])

    def test_has_type(self):
        self.assertEqual(self.test.type, TEST.NegativeParserTest)

    def test_has_status(self):
        self.assertEqual(self.test.status, 'WITHDRAWN')

    def test_has_description(self):
        self.assertTextEqual(self.test.description,
            " Does the treatment of literals conform to charmod ?"
            " Test for failure for literal not in Normal Form C"
            " This test case has been WITHDRAWN in light of changes to NFC handling in concepts ")

    def test_has_input_documents(self):
        self.assertEqual(set(self.test.input_documents),
                         {Document(TEST['RDF-XML-Document'],
                                   TESTS['rdf-charmod-literals/error001.rdf'])})

    def test_is_skipped_due_to_status(self):
        result = self.test.defaultTestResult()
        self.test.run(result)
        self.assertEqual(result.skipped,
                         [(self.test, "test status is WITHDRAWN")])
        self.assertEqual(result.testsRun, 1)

