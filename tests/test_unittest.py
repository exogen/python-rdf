import unittest
from xml.etree.ElementTree import XML

from rdf.namespace import Namespace, TEST
from rdf.testcases.document import Document
from rdf.testcases.test import Test
from rdf.testcases.unittest import RDFTestCase
from util import EX, TESTS, TEST_OPENER


class TestRDFTestCase(unittest.TestCase):
    def setUp(self):
        if getattr(self, 'test', None) is not None:
            self.test_case = RDFTestCase.from_test(self.test)
            self.test_case.opener = TEST_OPENER
            self.result = self.test_case.defaultTestResult()
            self.test_case.run(self.result)
        else:
            self.skipTest("'test' attribute not set. abstract test case?")

    def test_is_test_case(self):
        self.assert_(isinstance(self.test_case, RDFTestCase))

    def test_is_unittest_test_case(self):
        self.assert_(isinstance(self.test_case, unittest.TestCase))

class TestWithdrawnTestCase(TestRDFTestCase):
    test = Test(TEST.PositiveParserTest, EX.test)
    test.status = 'WITHDRAWN'

    def test_is_skipped_due_to_status(self):
        self.assertEqual(self.result.errors, [])
        self.assertEqual(self.result.failures, [])
        self.assertEqual(self.result.skipped,
                         [(self.test_case, "test status is WITHDRAWN")])
        self.assertEqual(self.result.testsRun, 1)

class TestObsoleteTestCase(TestRDFTestCase):
    test = Test(TEST.PositiveParserTest, EX.test)
    test.status = 'OBSOLETE'

    def test_is_skipped_due_to_status(self):
        self.assertEqual(self.result.errors, [])
        self.assertEqual(self.result.failures, [])
        self.assertEqual(self.result.skipped,
                         [(self.test_case, "test status is OBSOLETE")])
        self.assertEqual(self.result.testsRun, 1)

class TestPositiveParserTestCase(TestRDFTestCase):
    test = Test(TEST.PositiveParserTest, EX.test)
    test.status = 'APPROVED'
    test.input_documents = {Document(TEST['RDF-XML-Document'],
                                     TESTS['Manifest.rdf'])}
    test.output_document = Document(TEST['RDF-XML-Document'],
                                    TESTS['Manifest.rdf'])

    def test_runs_without_errors(self):
        self.assertEqual(self.result.errors, [])
        self.assertEqual(self.result.skipped, [])
        self.assertEqual(self.result.testsRun, 1)

class TestNegativeParserTestCase(TestRDFTestCase):
    test = Test(TEST.NegativeParserTest, EX.test)
    test.status = 'APPROVED'
    test.input_document = Document(TEST['RDF-XML-Document'],
                                   TESTS['Manifest.rdf'])
    
    def test_runs_without_errors(self):
        self.assertEqual(self.result.errors, [])
        self.assertEqual(self.result.skipped, [])
        self.assertEqual(self.result.testsRun, 1)

class TestPositiveEntailmentTestCase(TestRDFTestCase):
    pass

class TestNegativeEntailmentTestCase(TestRDFTestCase):
    pass

class TestMiscellaneousTestCase(TestRDFTestCase):
    test = Test(TEST.MiscellaneousTest, EX.test)
    test.status = 'APPROVED'

    def test_run_raises_exception(self):
        self.assertEqual(len(self.result.errors), 1)
        self.assertEqual(self.result.failures, [])
        self.assertEqual(self.result.skipped, [])
        self.assertEqual(self.result.testsRun, 1)
        self.assertEqual(self.result.wasSuccessful(), False)

class TestRDFTestSuite(unittest.TestCase):
    pass

