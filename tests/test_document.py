import unittest

from rdf.namespace import Namespace, TEST
from rdf.ntriples import NTriplesReader
from rdf.rdfxml import RDFXMLReader
from rdf.testcases.document import Document
from util import get_data_path, open_data_file, TESTS, PATH_MAP


class TestFalseDocument(unittest.TestCase):
    def setUp(self):
        self.doc = Document(TEST['False-Document'])

    def test_has_type(self):
        self.assertEqual(self.doc.type, TEST['False-Document'])

    def test_has_uri(self):
        self.assertEqual(self.doc.uri, None)

    def test_open_without_uri_raises_exception(self):
        self.assertRaises(RuntimeError, self.doc.open, PATH_MAP)

    def test_read_without_uri_raises_exception(self):
        self.assertRaises(RuntimeError, self.doc.read, PATH_MAP)

class TestNTriplesDocument(unittest.TestCase):
    def setUp(self):
        self.doc = Document(TEST['NT-Document'],
                            TESTS['datatypes-intensional/test002.nt'])
        self.file = open_data_file(
            'rdf-testcases/datatypes-intensional/test002.nt')
        self.reader = NTriplesReader()

    def test_has_type(self):
        self.assertEqual(self.doc.type, TEST['NT-Document'])

    def test_has_uri(self):
        self.assertEqual(self.doc.uri,
                         TESTS['datatypes-intensional/test002.nt'])

    def test_open_with_unmatched_uri_raises_exception(self):
        self.assertRaises(RuntimeError, self.doc.open, {})

    def test_open_opens_referenced_file(self):
        self.assertMultiLineEqual(self.doc.open(PATH_MAP).read(),
                                  self.file.read())

    def test_read_yields_triples_from_file(self):
        self.assertSameElements(self.doc.read(PATH_MAP),
                                self.reader.read(self.file))

class TestRDFXMLDocument(unittest.TestCase):
    def setUp(self):
        self.doc = Document(TEST['RDF-XML-Document'],
                            TESTS['rdf-charmod-literals/test001.rdf'])
        self.file = open_data_file(
            'rdf-testcases/rdf-charmod-literals/test001.rdf')
        self.reader = RDFXMLReader()

    def test_has_type(self):
        self.assertEqual(self.doc.type, TEST['RDF-XML-Document'])

    def test_has_uri(self):
        self.assertEqual(self.doc.uri,
                         TESTS['rdf-charmod-literals/test001.rdf'])

    def test_open_with_unmatched_uri_raises_exception(self):
        self.assertRaises(RuntimeError, self.doc.open, {})

    def test_open_opens_referenced_file(self):
        self.assertMultiLineEqual(self.doc.open(PATH_MAP).read(),
                                  self.file.read())

    def test_read_yields_triples_from_file(self):
        self.assertSameElements(self.doc.read(PATH_MAP),
                                self.reader.read(self.file))

