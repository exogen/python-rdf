import unittest
from xml.etree import ElementTree
from urllib.parse import urljoin

from rdf.resource import Resource
from rdf.uri import URI
from rdf.namespace import TEST
from rdf.testcases.testcase import TestCase, Document
from util import open_data_file




class TestTestCase(unittest.TestCase):
    def setUp(self):
        self.tree = ElementTree.parse(open_data_file('Manifest.rdf'))

    def _get_test(self, index):
        for i, element in enumerate(self.tree.getroot()):
            if i == index:
                return TestCase(element)
        raise IndexError

class TestPositiveParserTestCase(TestTestCase):
    def test_test_1_is_test_case(self):
        test = self._get_test(0)
        self.assert_(isinstance(test, TestCase))

    def test_test_1_uri(self):
        test = self._get_test(0)
        self.assertEqual(test.uri,
            urljoin(TEST, 'amp-in-url/Manifest.rdf#test001'))

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

    def test_test_1_input_document_is_document(self):
        test = self._get_test(0)
        self.assert_(isinstance(next(iter(test.input_documents)), Document))

    def test_test_1_input_document_uri(self):
        test = self._get_test(0)
        self.assertEqual(set(test.input_documents),
            {Document(TEST['RDF-XML-Document'],
                      urljoin(TEST, 'amp-in-url/test001.rdf'))})

    def test_test_1_output_document_is_document(self):
        test = self._get_test(0)
        self.assert_(isinstance(test.output_document, Document))

    def test_test_1_output_document_uri(self):
        test = self._get_test(0)
        self.assertEqual(test.output_document,
            Document(TEST['NT-Document'],
                     urljoin(TEST, 'amp-in-url/test001.nt')))

class TestNegativeEntailmentTestCase(TestTestCase):
    pass

