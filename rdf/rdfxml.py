from rdf.namespace import Namespace


RDF = Namespace('http://www.w3.org/1999/02/22-rdf-syntax-ns#')
XML = Namespace('http://www.w3.org/XML/1998/namespace')

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
        return iter([])

