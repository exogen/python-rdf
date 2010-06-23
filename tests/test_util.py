import sys
import unittest

from rdf.util import UniversalSet


class TestUniversalSet(unittest.TestCase):
    def setUp(self):
        self.set = UniversalSet()

    def test_is_frozenset(self):
        self.assert_(isinstance(self.set, frozenset))

    def test_contains_everything(self):
        self.assert_(1 in self.set)
        self.assert_(None in self.set)
        self.assert_([] in self.set)
        self.assert_(self.set in self.set)
        self.assert_("blah" in self.set)

    def test_size_is_sys_maxsize(self):
        self.assertEqual(len(self.set), sys.maxsize)

