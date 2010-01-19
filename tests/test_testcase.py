import unittest
import re
from xml.etree import ElementTree

from rdf.resource import Resource
from rdf.uri import URI
from rdf.namespace import Namespace, TEST, RDF, RDFS, XSD
from rdf.testcases.testcase import TestCase, Document
from util import open_data_file


_TEST = Namespace('http://www.w3.org/2000/10/rdf-tests/rdfcore/')

class TestTestCase(unittest.TestCase):
    def setUp(self):
        self.tree = ElementTree.parse(open_data_file('Manifest.rdf'))

    def _get_test(self, index):
        for i, element in enumerate(self.tree.getroot()):
            if i == index:
                return TestCase(element)
        raise IndexError
    
    def assertTextEqual(self, a, b):
        ws = re.compile(r'\s+')
        return self.assertEqual(ws.sub(' ', a), ws.sub(' ', b))

class TestPositiveParserTest(TestTestCase):
    def test_test_1_is_test_case(self):
        test = self._get_test(0)
        self.assert_(isinstance(test, TestCase))

    def test_test_1_uri(self):
        test = self._get_test(0)
        self.assertEqual(test.uri, _TEST['amp-in-url/Manifest.rdf#test001'])

    def test_test_1_type(self):
        test = self._get_test(0)
        self.assertEqual(test.type, TEST.PositiveParserTest)

    def test_test_1_status(self):
        test = self._get_test(0)
        self.assertEqual(test.status, 'APPROVED')

    def test_test_1_approval(self):
        test = self._get_test(0)
        self.assertEqual(test.approval,
            URI('http://lists.w3.org/Archives/Public/w3c-rdfcore-wg/2001Sep/0326.html'))

    def test_test_1_description(self):
        test = self._get_test(0)
        self.assertEqual(test.description, None)

    def test_test_1_input_documents(self):
        test = self._get_test(0)
        self.assertEqual(set(test.input_documents),
            {Document(TEST['RDF-XML-Document'],
                      _TEST['amp-in-url/test001.rdf'])})

    def test_test_1_output_document(self):
        test = self._get_test(0)
        self.assertEqual(test.output_document,
            Document(TEST['NT-Document'], _TEST['amp-in-url/test001.nt']))

class TestNegativeEntailmentTest(TestTestCase):
    def test_test_2_is_test_case(self):
        test = self._get_test(1)
        self.assert_(isinstance(test, TestCase))

    def test_test_2_uri(self):
        test = self._get_test(1)
        self.assertEqual(test.uri,
            _TEST['datatypes-intensional/Manifest.rdf#xsd-integer-decimal-compatible'])

    def test_test_2_type(self):
        test = self._get_test(1)
        self.assertEqual(test.type, TEST.NegativeEntailmentTest)

    def test_test_2_status(self):
        test = self._get_test(1)
        self.assertEqual(test.status, 'APPROVED')

    def test_test_2_approval(self):
        test = self._get_test(1)
        self.assertEqual(test.approval,
            URI('http://lists.w3.org/Archives/Public/w3c-rdfcore-wg/2003Sep/0093.html'))

    def test_test_2_description(self):
        test = self._get_test(1)
        self.assertTextEqual(test.description,
            " The claim that xsd:integer is a subClassOF xsd:decimal is not "
            "incompatible with using the intensional semantics for datatypes. ")

    def test_test_2_entailment_rules(self):
        test = self._get_test(1)
        self.assertEqual(set(test.entailment_rules),
            {RDF, RDFS, _TEST['datatypes#']})

    def test_test_2_datatype_support(self):
        test = self._get_test(1)
        self.assertEqual(set(test.datatype_support),
            {XSD.integer, XSD.decimal})

    def test_test_2_premise_documents(self):
        test = self._get_test(1)
        self.assertEqual(set(test.premise_documents),
            {Document(TEST['NT-Document'],
                      _TEST['datatypes-intensional/test001.nt'])})

    def test_test_2_conclusion_document(self):
        test = self._get_test(1)
        self.assertEqual(test.conclusion_document,
            Document(TEST['False-Document']))

