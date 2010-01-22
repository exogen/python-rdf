import unittest

import rdf.testcases.document
from rdf.namespace import Namespace, TEST
from rdf.ntriples import NTriplesReader
from rdf.rdfxml import RDFXMLReader
from rdf.testcases.document import Document
from util import get_data_path, open_data_file, TESTS, PATH_MAP


class TestDocument(unittest.TestCase):
    doc = None

    def setUp(self):
        if self.doc is None:
            self.skipTest("abstract test case (doc not set)")

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
        self.assertRaises(RuntimeError, self.doc.open, PATH_MAP)

    def test_read_without_uri_raises_exception(self):
        self.assertRaises(RuntimeError, self.doc.read, PATH_MAP)

class TestNTriplesDocument(TestDocument):
    def setUp(self):
        self.doc = Document(TEST['NT-Document'],
                            TESTS['datatypes-intensional/test002.nt'])
        self.file = open_data_file(
            'rdf-testcases/datatypes-intensional/test002.nt', mode='rb')
        self.reader = NTriplesReader()
        super().setUp()

    def test_has_type(self):
        self.assertEqual(self.doc.type, TEST['NT-Document'])

    def test_has_uri(self):
        self.assertEqual(self.doc.uri,
                         TESTS['datatypes-intensional/test002.nt'])

    def test_open_with_unmatched_uri_raises_exception(self):
        self.assertRaises(RuntimeError, self.doc.open, {})

    def test_open_opens_referenced_file(self):
        self.assertEqual(self.doc.open(PATH_MAP, mode='rb').read(),
                         self.file.read())

    def test_read_yields_triples_from_file(self):
        self.assertSameElements(self.doc.read(PATH_MAP),
                                self.reader.read(self.file))

class TestRDFXMLDocument(TestDocument):
    def setUp(self):
        self.doc = Document(TEST['RDF-XML-Document'],
                            TESTS['rdf-charmod-literals/test001.rdf'])
        self.file = open_data_file(
            'rdf-testcases/rdf-charmod-literals/test001.rdf', mode='rb')
        self.reader = RDFXMLReader()
        super().setUp()

    def test_has_type(self):
        self.assertEqual(self.doc.type, TEST['RDF-XML-Document'])

    def test_has_uri(self):
        self.assertEqual(self.doc.uri,
                         TESTS['rdf-charmod-literals/test001.rdf'])

    def test_open_with_unmatched_uri_raises_exception(self):
        self.assertRaises(RuntimeError, self.doc.open, {})

    def test_open_opens_referenced_file(self):
        self.assertEqual(self.doc.open(PATH_MAP, mode='rb').read(),
                         self.file.read())

    def test_read_yields_triples_from_file(self):
        self.assertSameElements(self.doc.read(PATH_MAP),
                                self.reader.read(self.file))

