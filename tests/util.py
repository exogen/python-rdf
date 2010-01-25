from rdf.namespace import Namespace
from rdf.testcases.opener import URItoFileOpener
import os.path



def get_data_path(filename):
    return os.path.join(os.path.dirname(__file__), 'data', filename)

def open_data_file(filename, mode='r'):
    return open(get_data_path(filename), mode)

EX = Namespace('http://example.org/')
TESTS = Namespace('http://www.w3.org/2000/10/rdf-tests/rdfcore/')

PATH_MAP = {TESTS: get_data_path('rdf-testcases')}
TEST_OPENER = URItoFileOpener(PATH_MAP)

