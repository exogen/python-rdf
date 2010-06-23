import unittest
import pprint

from rdf.namespace import TEST, RDF, RDFS
from rdf.graph import Graph
from rdf.testcases.test import Test
from rdf.syntax.exceptions import ParseError
from rdf.semantics.entailment import Entailment, SIMPLE_ENTAILMENT, \
    SIMPLE_ENTAILMENT_LG, RDF_ENTAILMENT, RDFS_ENTAILMENT, DATATYPE_ENTAILMENT
from util import TESTS


class RDFTestCase(unittest.TestCase):
    TYPE_MAP = {}
    test = None

    @classmethod
    def from_test(cls, test):
        cls = cls.TYPE_MAP.get(test.type, cls)
        test_case = cls()
        test_case.test = test
        if test.description:
            test_case.runTest.__func__.__doc__ = test.description.strip()
        return test_case

    def setUp(self):
        if self.test is None:
            self.skipTest("'test' attribute not set. abstract test case?")
        elif self.test.status != 'APPROVED':
            self.skipTest("test status is {0}".format(self.test.status))

    def runTest(self):
        raise NotImplementedError

    def id(self):
        if self.test is not None:
            return str(self.test.uri)
        return super().id()

    def shortDescription(self):
        if self.test is not None:
            if self.test.description:
                description_lines = self.test.description.strip().splitlines()
                first_line = description_lines[0].rstrip()
                if first_line:
                    return "{0!s}\n{1}".format(self.test.uri, first_line)
            else:
                return str(self.test.uri)
        else:
            return super().shortDescription()

class ParserTestCase(RDFTestCase):
    pass

class PositiveParserTestCase(RDFTestCase):
    def setUp(self):
        super().setUp()
        self.input_graph = Graph()
        for document in self.test.input_documents:
            self.input_graph.update(document.read(self.opener))
        self.output_graph = Graph(self.test.output_document.read(self.opener))

    def runTest(self):
        self.assertEqual(self.input_graph, self.output_graph)

class NegativeParserTestCase(ParserTestCase):
    def setUp(self):
        super().setUp()
        self.file = self.test.input_document.open(self.opener)
        self.reader = self.test.input_document.get_reader()

    def runTest(self):
        base_uri = self.test.input_document.uri
        with self.assertRaises(ParseError):
            for triple in self.reader.read(self.file, base_uri):
                pass

class EntailmentTestCase(RDFTestCase):
    ENTAILMENT_RULES = {TEST.simpleEntailment: SIMPLE_ENTAILMENT_LG,
                        RDF: RDF_ENTAILMENT,
                        RDFS: RDFS_ENTAILMENT,
                        TESTS['datatypes#']: DATATYPE_ENTAILMENT}

    def setUp(self):
        super().setUp()
        self.premise = Graph()
        for premise_document in self.test.premise_documents:
            if premise_document.type != TEST['False-Document']:
                self.premise.update(premise_document.read(self.opener))
            else:
                self.premise = False

        self.entailments = []
        for rules_uri in self.test.entailment_rules:
            entailment = self.ENTAILMENT_RULES[rules_uri]
            self.entailments.append(entailment)
        if (SIMPLE_ENTAILMENT not in self.entailments and
            SIMPLE_ENTAILMENT_LG not in self.entailments):
            self.entailments.append(SIMPLE_ENTAILMENT_LG)

        self.merged_entailment = Entailment()
        for entailment in self.entailments:
            self.merged_entailment.conditions += entailment.conditions
            self.merged_entailment.axioms |= entailment.axioms
            self.merged_entailment.rules += entailment.rules

        self.merged_entailment.axioms |= {
            (datatype, RDF.type, RDFS.Datatype) for datatype in
            self.test.datatype_support}

        if self.test.conclusion_document.type != TEST['False-Document']:
            self.conclusion = Graph(
                self.test.conclusion_document.read(self.opener))
        else:
            self.conclusion = False

class PositiveEntailmentTestCase(EntailmentTestCase):
    def runTest(self):
        if self.conclusion != False:
            self.assert_(self.merged_entailment.entails(self.premise,
                                                        self.conclusion),
                         "\n{0} does not entail \n{1}".format(
                             pprint.pformat(self.premise),
                             pprint.pformat(self.conclusion)))

class NegativeEntailmentTestCase(EntailmentTestCase):
    def runTest(self):
        if self.conclusion != False:
            for entailment in self.entailments:
                self.assert_(not entailment.entails(self.premise,
                                                    self.conclusion))

class MiscellaneousTestCase(RDFTestCase):
    pass

RDFTestCase.TYPE_MAP.update({
    TEST.PositiveParserTest: PositiveParserTestCase,
    TEST.NegativeParserTest: NegativeParserTestCase,
    TEST.PositiveEntailmentTest: PositiveEntailmentTestCase,
    TEST.NegativeEntailmentTest: NegativeEntailmentTestCase,
    TEST.MiscellaneousTest: MiscellaneousTestCase})

class RDFTestSuite(unittest.TestSuite):
    @classmethod
    def from_manifest(cls, manifest, opener=None):
        suite = cls()
        for test in manifest:
            test_case = RDFTestCase.from_test(test)
            if opener is not None:
                test_case.opener = opener
            suite.addTest(test_case)
        return suite

