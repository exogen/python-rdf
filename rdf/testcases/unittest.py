import unittest

from rdf.namespace import TEST
from rdf.graph import Graph
from rdf.testcases.test import Test
from rdf.syntax.exceptions import ParseError
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
    pass

class PositiveEntailmentTestCase(EntailmentTestCase):
    pass

class NegativeEntailmentTestCase(EntailmentTestCase):
    pass

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

