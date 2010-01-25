import unittest

from rdf.syntax.rdfxml import RDFXMLReader


class TestRDFXMLReader(unittest.TestCase):
    def setUp(self):
        self.reader = RDFXMLReader()


    def test_is_rdfxml_reader(self):
        self.assert_(isinstance(self.reader, RDFXMLReader))

