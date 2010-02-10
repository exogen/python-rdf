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
        yield None


            

