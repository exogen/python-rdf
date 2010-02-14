import unittest

from rdf.blanknode import BlankNode
from rdf.uri import URI
from rdf.literal import Literal
from rdf.namespace import XSD


class TestBlankNode(unittest.TestCase):
    def setUp(self):
        self.bnode = BlankNode()

    def test_is_blank_node(self):
        self.assert_(isinstance(self.bnode, BlankNode))

    def test_default_node_id_is_none(self):
        self.assertEqual(self.bnode.node_id, None)

    def test_repr_without_node_id_shows_id(self):
        hex_id = hex(id(self.bnode))
        self.assertEqual(repr(self.bnode), "<BlankNode at {}>".format(hex_id))

    def test_not_equal_to_blank_node_without_node_id(self):
        self.assertNotEqual(self.bnode, BlankNode())

    def test_hash_not_equal_to_blank_node_without_node_id(self):
        self.assertNotEqual(hash(self.bnode), hash(BlankNode()))

    def test_equal_to_same_instance(self):
        self.assertEqual(self.bnode, self.bnode)

    def test_hash_equal_to_hash_of_same_instance(self):
        self.assertEqual(hash(self.bnode), hash(self.bnode))

    def test_compares_greater_than_none(self):
        self.assert_(self.bnode > None)

    def test_compares_less_than_uri(self):
        self.assert_(self.bnode < URI('test'))

    def test_compares_less_than_plain_literal(self):
        self.assert_(self.bnode < Literal("test"))

    def test_compares_less_than_typed_literal(self):
        self.assert_(self.bnode < Literal("0", XSD.integer))

class TestBlankNodeWithNodeID(unittest.TestCase):
    def setUp(self):
        self.bnode = BlankNode('b1')

    def test_is_blank_node(self):
        self.assert_(isinstance(self.bnode, BlankNode))

    def test_constructor_sets_node_id(self):
        self.assertEqual(self.bnode.node_id, 'b1')

    def test_repr_shows_constructor(self):
        self.assertEqual(repr(self.bnode), "BlankNode('b1')")

    def test_equal_to_blank_node_with_same_node_id(self):
        self.assertEqual(self.bnode, BlankNode('b1'))

    def test_hash_equal_to_blank_node_with_same_node_id(self):
        self.assertEqual(hash(self.bnode), hash(BlankNode('b1')))

    def test_not_equal_to_blank_node_with_different_node_id(self):
        self.assertNotEqual(self.bnode, BlankNode('b2'))

    def test_hash_not_equal_to_blank_node_with_different_node_id(self):
        self.assertNotEqual(hash(self.bnode), hash(BlankNode('b2')))

    def test_not_equal_to_blank_node_without_node_id(self):
        self.assertNotEqual(self.bnode, BlankNode())

    def test_hash_not_equal_to_blank_node_without_node_id(self):
        self.assertNotEqual(hash(self.bnode), hash(BlankNode()))

    def test_not_equal_to_string(self):
        self.assertNotEqual(self.bnode, 'b1')

    def test_equal_to_same_instance(self):
        self.assertEqual(self.bnode, self.bnode)

    def test_hash_equal_to_hash_of_same_instance(self):
        self.assertEqual(hash(self.bnode), hash(self.bnode))

