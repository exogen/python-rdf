import unittest

from rdf.resource import Resource
from rdf.blanknode import BlankNode


class TestBlankNode(unittest.TestCase):
    def setUp(self):
        self.b1 = BlankNode('b1')

    def test_is_resource(self):
        self.assert_(isinstance(self.b1, Resource))

    def test_is_created_with_node_id(self):
        self.assert_(isinstance(self.b1, BlankNode))

    def test_has_node_id(self):
        self.assert_(hasattr(self.b1, 'node_id'))
        self.assertEqual(self.b1.node_id, 'b1')

    def test_repr_shows_constructor(self):
        self.assertEqual(repr(self.b1), "BlankNode('b1')")

    def test_not_equal_to_string(self):
        self.assertNotEqual(self.b1, 'b1')

if __name__ == '__main__':
    unittest.main()
