import unittest

from rdf.blanknode import BlankNode
from rdf.namespace import RDF, RDFS
from rdf.graph import Graph
from rdf.semantics.type import uuu, aaa, xxx, llt
from rdf.semantics.entailment import rdfD1

from util import EX


#class TestRuleD1(unittest.TestCase):
#    def setUp(self):
#        self.graph = Graph({(EX.a, RDF.type, RDFS.Datatype),
#                            (EX.b, EX.property, EX.c)})
#
#    def test_consequent_is_blank_node_with_datatype(self):
#        consequent = Graph(rdfD1.apply(self.graph))
#        self.assertEqual(consequent, Graph({(BlankNode(), RDF.type, EX.c)}))
