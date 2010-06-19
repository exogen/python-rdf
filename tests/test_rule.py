import unittest

from rdf.blanknode import BlankNode
from rdf.namespace import RDF
from rdf.graph import Graph
from rdf.semantics.type import uuu, aaa, xxx
from rdf.semantics.rule import Rule, Context

from util import EX


class TestRule(unittest.TestCase):
    def setUp(self):
        self.rule = Rule({}, {(RDF.type, RDF.type, RDF.Property)})
        self.rule_se1 = Rule({(uuu, aaa, xxx)},
                             {(uuu, aaa, xxx.nnn)}, name='se1')
        self.empty_graph = Graph()
        self.graph = Graph({(EX.a, EX.property, EX.b),
                            (EX.b, EX.property, EX.c)})
        self.context = Context()

    def test_first_arg_sets_antecedent(self):
        self.assertEqual(self.rule_se1.antecedent, {(uuu, aaa, xxx)})

    def test_antecedent_can_be_empty(self):
        self.assertEqual(self.rule.antecedent, set())

    def test_second_arg_sets_consequent(self):
        self.assertEqual(self.rule.consequent,
                         {(RDF.type, RDF.type, RDF.Property)})
        self.assertEqual(self.rule_se1.consequent, {(uuu, aaa, xxx.nnn)})

    def test_name_arg_sets_name(self):
        self.assertEqual(self.rule_se1.name, 'se1')

    def test_default_name_is_none(self):
        self.assertEqual(self.rule.name, None)

    def test_apply_empty_antecedent_to_empty_graph_yields_consequent(self):
        graph = Graph(self.rule.apply(self.empty_graph, self.context))
        self.assertEqual(graph, Graph({(RDF.type, RDF.type, RDF.Property)}))

    def test_apply_empty_antecedent_to_graph_yields_consequent(self):
        graph = Graph(self.rule.apply(self.graph, self.context))
        self.assertEqual(graph, Graph({(RDF.type, RDF.type, RDF.Property)}))

    def test_apply_with_empty_antecedent_to_empty_graph_does_not_yield_consequent(self):
        graph = Graph(self.rule_se1.apply(self.empty_graph, self.context))
        self.assertEqual(graph, Graph())

    def test_apply_to_graph_yields_consequent(self):
        graph = Graph(self.rule_se1.apply(self.graph, self.context))
        self.assertEqual(graph, Graph({(EX.a, EX.property, BlankNode()),
                                       (EX.b, EX.property, BlankNode())}))


