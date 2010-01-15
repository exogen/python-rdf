import unittest

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


if __name__ == '__main__':
    unittest.main()

