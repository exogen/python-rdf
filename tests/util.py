import os.path
from urllib.request import OpenerDirector

from rdf.namespace import Namespace
from rdf.testcases.opener import URItoFileOpener


def get_data_path(filename):
    return os.path.join(os.path.dirname(__file__), 'data', filename)

def open_data_file(filename, mode='r'):
    return open(get_data_path(filename), mode)

class NullOpener(OpenerDirector):
    def open(self, *args, **kwargs):
        return None

EX = Namespace('http://example.org/')
TESTS = Namespace('http://www.w3.org/2000/10/rdf-tests/rdfcore/')

PATH_MAP = {TESTS: get_data_path('rdf-testcases')}
TEST_OPENER = URItoFileOpener(PATH_MAP)
NULL_OPENER = NullOpener()

