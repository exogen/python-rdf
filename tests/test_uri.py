import unittest
from xml.etree.ElementTree import QName

from rdf.resource import Resource
from rdf.uri import URI


class TestURI(unittest.TestCase):
    def setUp(self):
        self.uri = URI('test')

    def test_is_resource(self):
        self.assert_(isinstance(self.uri, Resource))

    def test_is_string(self):
        self.assert_(isinstance(self.uri, str))

    def test_is_created_with_string(self):
        self.assert_(isinstance(self.uri, URI))

    def test_repr_shows_constructor(self):
        self.assertEqual(repr(self.uri), "URI('test')")

    def test_equal_to_string(self):
        self.assertEqual(self.uri, "test")

    def test_resource_with_uri_is_uri(self):
        self.assert_(isinstance(Resource('test'), URI))

    def test_can_create_empty_uri(self):
        self.assertEqual(URI(), '')

    def test_converts_qname_to_uri(self):
        qname = QName('http://example.org/', 'test')
        uri = URI(qname)
        self.assertEqual(uri, URI('http://example.org/test'))

    def test_resource_with_qname_is_uri(self):
        qname = QName('http://example.org/', 'test')
        self.assertEqual(Resource(qname), URI('http://example.org/test'))

