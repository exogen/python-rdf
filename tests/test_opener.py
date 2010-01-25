import unittest
from urllib.request import OpenerDirector, BaseHandler, URLError

from rdf.namespace import TEST
from rdf.testcases.opener import URItoFileOpener, URItoFileHandler
from util import open_data_file, EX, TESTS, PATH_MAP, TEST_OPENER


class TestHandler(unittest.TestCase):
    def setUp(self):
        self.handler = URItoFileHandler(PATH_MAP)
        self.manifest_file = open_data_file('rdf-testcases/Manifest.rdf')

    def tearDown(self):
        self.manifest_file.close()

    def test_is_handler(self):
        self.assert_(isinstance(self.handler, BaseHandler))
        
    def test_opening_unmapped_uri_raises_exception(self):
        self.assertRaises(URLError, self.handler.default_open, EX.test)
    
    def test_opening_mapped_uri_returns_file(self):
        manifest_file = self.handler.default_open(TESTS['Manifest.rdf'])
        self.assertEqual(manifest_file.read(), self.manifest_file.read())

class TestOpener(unittest.TestCase):
    def setUp(self):
        self.opener = URItoFileOpener(PATH_MAP)
        self.manifest_file = open_data_file('rdf-testcases/Manifest.rdf')

    def test_is_opener_director(self):
        self.assert_(isinstance(self.opener, OpenerDirector))

    def test_open_with_handler_returns_file(self):
        manifest_file = self.opener.open(TESTS['Manifest.rdf'])
        self.assertEqual(manifest_file.read(), self.manifest_file.read())

    def test_open_without_handler_returns_none(self):
        opener = URItoFileOpener()
        manifest_file = opener.open(TESTS['Manifest.rdf'])
        self.assertEqual(manifest_file, None)

