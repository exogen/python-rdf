import urllib.parse
from xml.etree import ElementTree
from xml.etree.ElementTree import QName

from rdf.uri import URI
from rdf.namespace import Namespace, RDF, XML


class RDFXMLReader:
    RESERVED_ATTRS = {RDF.about, RDF.resource, RDF.ID, RDF.nodeID, XML.lang,
                      XML.base}
    ILLEGAL_ATTRS = {RDF.aboutEachPrefix, RDF.aboutEach, RDF.li}
    ILLEGAL_TAGS = {RDF.RDF, RDF.ID, RDF.about, RDF.bagID, RDF.parseType,
                    RDF.resource, RDF.nodeID, RDF.aboutEach,
                    RDF.aboutEachPrefix}
    ILLEGAL_NODES = ILLEGAL_TAGS | {RDF.li}
    ILLEGAL_PROPERTIES = ILLEGAL_TAGS | {RDF.Description}

    class ParseError(Exception):
        pass

    def read(self, lines, uri=None):
        if isinstance(lines, str):
            root = ElementTree.XML(lines)
        else:
            root = ElementTree.parse(lines).getroot()
        for element in root:
            for triple in self._node_element(element):
                yield triple

    def _node_element(self, element):
        if URI(QName(element.tag)) in self.ILLEGAL_NODES:
            raise self.ParseError("Illegal node tag: {!r}".format(element.tag))

        subject = self._subject(element)
        # 2.2 Node Elements and Property Elements
        for triple in self._property_elements(element, subject):
            yield triple

    def _subject(self, element):
        about = element.get(QName(RDF, 'about'))
        if about is not None:
            return self._uri(about)

    def _uri(self, uri, base=None):
        return URI(urllib.parse.urljoin(base or '', uri))

    def _property_elements(self, element, subject):
        for child in element:
            predicate = URI(QName(child.tag))
            if predicate in self.ILLEGAL_PROPERTIES:
                raise ParseError("Illegal property tag: {!r}".format(predicate))

            predicate = URI(QName(child.tag))

        # TODO: Finish this.
        return []

