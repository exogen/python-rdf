from xml.etree import ElementTree

from rdf.testcases.test import Test


class Manifest:
    def __init__(self, lines):
        if isinstance(lines, str):
            self._element = ElementTree.XML(lines)
        else:
            self._element = ElementTree.parse(lines).getroot()

    def __iter__(self):
        for element in self._element:
            yield Test.from_element(element)

    def __len__(self):
        return len(self._element)

