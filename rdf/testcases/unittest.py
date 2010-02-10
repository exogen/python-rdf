import unittest

from rdf.namespace import TEST
from rdf.testcases.test import Test


class RDFTestCase(unittest.TestCase):
    TYPE_MAP = {}

    @classmethod
    def from_test(cls, test):
        cls = cls.TYPE_MAP.get(test.type, cls)
        test_case = cls()
        test_case.test = test
        return test_case

    def setUp(self):
        if getattr(self, 'test', None) is None:
            self.skipTest("'test' attribute not set. abstract test case?")
        elif self.test.status != 'APPROVED':
            self.skipTest("test status is {0}".format(self.test.status))

    def runTest(self):
        raise NotImplementedError

class ParserTestCase(RDFTestCase):
    pass

class PositiveParserTestCase(RDFTestCase):
    def setUp(self):
        super().setUp()
        self.input_triples = set()
        for document in self.test.input_documents:
            self.input_triples.update(document.read(self.opener))
        self.output_triples = set(self.test.output_document.read(self.opener))

    def runTest(self):
        self.assertSetEqual(self.input_triples, self.output_triples)

class NegativeParserTestCase(ParserTestCase):
    def setUp(self):
        super().setUp()
        self.file = self.test.input_document.open(self.opener)
        self.reader = self.test.input_document.get_reader()

    def runTest(self):
        self.assertRaises(self.reader.ParseError, self.reader.read, self.file)

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
    TEST.PositiveEntailment: PositiveEntailmentTestCase,
    TEST.NegativeEntailment: NegativeEntailmentTestCase,
    TEST.MiscellaneousTest: MiscellaneousTestCase})

class RDFTestSuite(unittest.TestSuite):
    @classmethod
    def from_manifest(cls, manifest):
        return cls(RDFTestCase.from_test(test) for test in manifest)

