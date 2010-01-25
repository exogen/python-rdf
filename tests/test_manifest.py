import unittest
from collections import defaultdict

from rdf.namespace import TEST
from rdf.testcases.test import Test
from rdf.testcases.manifest import Manifest
from util import open_data_file


class TestManifest(unittest.TestCase):
    def setUp(self):
        self.file = open_data_file('Manifest.rdf')
        self.manifest = Manifest(self.file)

    def test_is_manifest(self):
        self.assert_(isinstance(self.manifest, Manifest))

    def test_iterating_manifest_yields_tests(self):
        self.assert_(all(isinstance(test, Test) for test in self.manifest))

    def test_length_is_number_of_tests(self):
        tests = list(self.manifest)
        self.assertEqual(len(self.manifest), len(tests))
        self.assertEqual(len(tests), 266)

    def test_has_tests_with_status(self):
        statuses = defaultdict(int)
        for test in self.manifest:
            statuses[test.status] += 1
        self.assertEqual(statuses, {'APPROVED': 212,
                                    'NOT_APPROVED': 14,
                                    'WITHDRAWN': 3,
                                    'OBSOLETE': 36,
                                    'OBSOLETED': 1})

    def test_has_tests_with_type(self):
        types = defaultdict(int)
        for test in self.manifest:
            types[test.type] += 1
        self.assertEqual(types, {TEST.PositiveParserTest: 158,
                                 TEST.NegativeParserTest: 58,
                                 TEST.PositiveEntailmentTest: 26,
                                 TEST.NegativeEntailmentTest: 23,
                                 TEST.MiscellaneousTest: 1})

class TestManifestFromString(TestManifest):
    def setUp(self):
        self.string = open_data_file('Manifest.rdf').read()
        self.manifest = Manifest(self.string)

