import unittest

from rdf.blanknode import BlankNode
from rdf.uri import URI
from rdf.literal import PlainLiteral, TypedLiteral
from rdf.semantics.type import Type, ContainerMembershipPropertyType
from rdf.namespace import RDF


class TestType(unittest.TestCase):
    def setUp(self):
        self.predicates = Type(URI)
        self.subjects = Type((URI, BlankNode))

    def test_is_type(self):
        self.assert_(isinstance(self.predicates, Type))

    def test_uri_instance_in_uri_type(self):
        self.assert_(URI('test') in self.predicates)

    def test_blank_node_instance_not_in_uri_type(self):
        self.assert_(BlankNode() not in self.predicates)

    def test_uri_instance_not_in_uri_and_blank_node_type(self):
        self.assert_(URI('test') in self.subjects)

    def test_blank_node_instance_in_uri_and_blank_node_type(self):
        self.assert_(BlankNode() in self.subjects)

    def test_literal_instance_not_in_uri_and_blank_node_type(self):
        self.assert_(PlainLiteral("test") not in self.subjects)

class TestContainerMembershipPropertyType(unittest.TestCase):
    def setUp(self):
        self.cmp = ContainerMembershipPropertyType()

    def test_is_type(self):
        self.assert_(isinstance(self.cmp, Type))

    def test_cmp_uri_instance_in_type(self):
        self.assert_(RDF._0 in self.cmp)
        self.assert_(RDF._1 in self.cmp)
        self.assert_(RDF._42 in self.cmp)

    def test_cmp_uri_literal_not_in_type(self):
        self.assert_(PlainLiteral(str(RDF._1)) not in self.cmp)

    def test_blanknode_not_in_type(self):
        self.assert_(BlankNode() not in self.cmp)

