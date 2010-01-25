import unittest
from urllib.request import URLError

import rdf.testcases.document
from rdf.namespace import Namespace, TEST
from rdf.syntax.ntriples import NTriplesReader
from rdf.syntax.rdfxml import RDFXMLReader
from rdf.testcases.document import Document
from rdf.testcases.opener import URItoFileOpener
from util import get_data_path, open_data_file, TESTS, TEST_OPENER


class TestDocument(unittest.TestCase):
    def setUp(self):
        if getattr(self, 'doc', None) is None:
            self.skipTest("'doc' attribute not set. abstract test case?")

    def test_is_document(self):
        self.assert_(isinstance(self.doc, Document))

    def test_repr_shows_constructor(self):
        self.assertEqual(repr(self.doc),
            "Document({!r}, {!r})".format(self.doc.type, self.doc.uri))

class TestFalseDocument(TestDocument):
    def setUp(self):
        self.doc = Document(TEST['False-Document'])
        super().setUp()

    def test_has_type(self):
        self.assertEqual(self.doc.type, TEST['False-Document'])

    def test_has_uri(self):
        self.assertEqual(self.doc.uri, None)

    def test_open_without_uri_raises_exception(self):
        self.assertRaises(URLError, self.doc.open, TEST_OPENER)

    def test_read_without_reader_raises_exception(self):
        self.assertRaises(RuntimeError, self.doc.read, TEST_OPENER)

class TestNTriplesDocument(TestDocument):
    def setUp(self):
        self.doc = Document(TEST['NT-Document'],
                            TESTS['datatypes-intensional/test002.nt'])
        self.file = open_data_file('rdf-testcases/datatypes-intensional/test002.nt')
        self.reader = NTriplesReader()
        super().setUp()

    def test_has_type(self):
        self.assertEqual(self.doc.type, TEST['NT-Document'])

    def test_has_uri(self):
        self.assertEqual(self.doc.uri,
                         TESTS['datatypes-intensional/test002.nt'])

    def test_open_with_unmatched_uri_raises_exception(self):
        opener = URItoFileOpener({})
        self.assertRaises(URLError, self.doc.open, opener)

    def test_open_opens_referenced_file(self):
        self.assertEqual(self.doc.open(TEST_OPENER).read(), self.file.read())

    def test_read_yields_triples_from_file(self):
        self.assertSameElements(self.doc.read(TEST_OPENER),
                                self.reader.read(self.file))

class TestRDFXMLDocument(TestDocument):
    def setUp(self):
        self.doc = Document(TEST['RDF-XML-Document'],
                            TESTS['rdf-charmod-literals/test001.rdf'])
        self.file = open_data_file('rdf-testcases/rdf-charmod-literals/test001.rdf')
        self.reader = RDFXMLReader()
        super().setUp()

    def test_has_type(self):
        self.assertEqual(self.doc.type, TEST['RDF-XML-Document'])

    def test_has_uri(self):
        self.assertEqual(self.doc.uri,
                         TESTS['rdf-charmod-literals/test001.rdf'])

    def test_open_with_unmatched_uri_raises_exception(self):
        opener = URItoFileOpener({})
        self.assertRaises(URLError, self.doc.open, opener)

    def test_open_opens_referenced_file(self):
        self.assertEqual(self.doc.open(TEST_OPENER).read(), self.file.read())

    def test_read_yields_triples_from_file(self):
        self.assertSameElements(self.doc.read(TEST_OPENER),
                                self.reader.read(self.file))

