import urllib.parse
from xml.etree import ElementTree
from xml.etree.ElementTree import QName

from rdf.uri import URI
from rdf.blanknode import BlankNode
from rdf.literal import PlainLiteral, TypedLiteral
from rdf.namespace import Namespace, RDF, XML


class RDFXMLReader:
    CORE_SYNTAX_TERMS = {RDF.RDF, RDF.ID, RDF.about, RDF.parseType,
                         RDF.resource, RDF.nodeID, RDF.datatype}
    SYNTAX_TERMS = CORE_SYNTAX_TERMS | {RDF.Description, RDF.li}
    OLD_TERMS = {RDF.aboutEach, RDF.aboutEachPrefix, RDF.bagID}

    ILLEGAL_NODE_TAGS = CORE_SYNTAX_TERMS | {RDF.li} | OLD_TERMS
    ILLEGAL_PROPERTY_TAGS = CORE_SYNTAX_TERMS | {RDF.Description} | OLD_TERMS
    ILLEGAL_PROPERTY_ATTRS = SYNTAX_TERMS | OLD_TERMS
    
    class ParseError(Exception):
        pass

    def read(self, lines, base_uri=None):
        if isinstance(lines, str):
            root = ElementTree.XML(lines)
        else:
            root = ElementTree.parse(lines).getroot()
        self._init_element(root)
        if root.base_uri is None:
            root.base_uri = base_uri
        for element in root:
            self._init_element(element, parent=root)
            for triple in self._node_element(element):
                yield triple

    def _init_element(self, element, parent=None):
        element.uri = URI(QName(element.tag))
        element.base_uri = element.attrib.pop(QName(XML, 'base'), None)
        if element.base_uri is None and parent is not None:
            element.base_uri = parent.base_uri
        element.language = element.attrib.pop(QName(XML, 'lang'), None)
        if element.language is None and parent is not None:
            element.language = parent.language
        element.li_counter = 1

    def _node_element(self, element):
        # 7.2.11 Production nodeElement
        if element.uri in self.ILLEGAL_NODE_TAGS:
            raise self.ParseError("Illegal node tag: {!s}".format(element.uri))

        element.subject = self._subject(element)

        # 2.13 Typed Node Elements
        if element.uri != RDF.Description:
            yield (element.subject, RDF.type, element.uri)

        # 2.5 Property Attributes
        type_attr = element.get(QName(RDF, 'type'))
        if type_attr is not None:
            yield (element.subject, RDF.type, URI(type_attr))

        for attr, value in element.items():
            attr = URI(QName(attr))
            if attr not in self.ILLEGAL_PROPERTY_ATTRS and attr != RDF.type:
                yield (element.subject, attr, PlainLiteral(value))

        for triple in self._property_elements(element):
            yield triple
    
    def _subject(self, element):
        id_ = element.get(QName(RDF, 'ID'))
        node_id = element.get(QName(RDF, 'nodeID'))
        about = element.get(QName(RDF, 'about'))
        if id_ is not None:
            if node_id is None:
                if about is None:
                    return self._uri('#' + id_, element.base_uri)
                raise self.ParseError
            raise self.ParseError
        elif node_id is not None:
            if about is None:
                return BlankNode(node_id)
            raise self.ParseError
        elif about is not None:
            return self._uri(about, element.base_uri)
        return BlankNode()

    def _uri(self, uri, base_uri=None):
        if base_uri and not uri:
            base_uri = base_uri.rsplit('#', 1)[0]
        return URI(urllib.parse.urljoin(base_uri or '', uri))

    def _property_elements(self, element):
        # 7.2.13 Production propertyEltList
        for child in element:
            # 7.2.14 Production propertyElt
            self._init_element(child, parent=element)
            # Container Membership Property Elements: rdf:li and rdf:_n
            if child.uri == RDF.li:
                child.uri = RDF['_' + str(element.li_counter)]
                element.li_counter += 1

            if len(child) == 1:
                # 7.2.15 Production resourcePropertyElt
                node_element = child[0]
                self._init_element(node_element, parent=child)
                for triple in self._node_element(node_element):
                    yield triple
                yield (element.subject, child.uri, node_element.subject)
            elif len(child) == 0:
                if child.text:
                    # 7.2.16 Production literalPropertyElt
                    datatype = child.get(QName(RDF, 'datatype'))
                    if datatype is not None:
                        literal = TypedLiteral(child.text, datatype)
                    else:
                        literal = PlainLiteral(child.text, child.language)
                else:
                    # 7.2.21 Production emptyPropertyElt
                    resource = child.get(QName(RDF, 'resource'))
                    if resource is not None:
                        object_ = self._uri(resource, child.base_uri)
                        yield (element.subject, child.uri, object_)



