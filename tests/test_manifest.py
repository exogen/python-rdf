import unittest

from rdf.testcases.testcase import TestCase
from rdf.testcases.manifest import Manifest
from util import open_data_file


class TestManifest(unittest.TestCase):
    def setUp(self):
        self.manifest = Manifest.read(open_data_file('Manifest.rdf'))

    def test_is_manifest(self):
        self.assert_(isinstance(self.manifest, Manifest))

    def test_test_1_positive_parser_test(self):
        pass

