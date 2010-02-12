import urllib.parse
from xml.etree import ElementTree
from xml.etree.ElementTree import QName

from rdf.uri import URI
from rdf.blanknode import BlankNode
from rdf.literal import PlainLiteral, TypedLiteral
from rdf.namespace import Namespace, RDF, XML
from rdf.syntax.exceptions import ParseError


class RDFXMLReader:
    CORE_SYNTAX_TERMS = {RDF.RDF, RDF.ID, RDF.about, RDF.parseType,
                         RDF.resource, RDF.nodeID, RDF.datatype}
    SYNTAX_TERMS = CORE_SYNTAX_TERMS | {RDF.Description, RDF.li}
    OLD_TERMS = {RDF.aboutEach, RDF.aboutEachPrefix, RDF.bagID}

    ILLEGAL_NODE_TAGS = CORE_SYNTAX_TERMS | {RDF.li} | OLD_TERMS
    ILLEGAL_PROPERTY_TAGS = CORE_SYNTAX_TERMS | {RDF.Description} | OLD_TERMS
    ILLEGAL_PROPERTY_ATTRS = SYNTAX_TERMS | OLD_TERMS
    
    def read(self, lines, base_uri=None):
        if isinstance(lines, str):
            root = ElementTree.XML(lines)
        else:
            root = ElementTree.parse(lines).getroot()
        self._init_element(root)
        if root.base_uri is None:
            root.base_uri = base_uri
        # rdf:RDF is not necessarily the root element.
        for element in root if root.uri == RDF.RDF else [root]:
            if element is not root:
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
            raise ParseError("Illegal node tag: {!s}".format(element.uri))

        element.subject = self._subject(element)

        # 2.13 Typed Node Elements
        if element.uri != RDF.Description:
            yield (element.subject, RDF.type, element.uri)

        # 2.5 Property Attributes
        type_attr = element.attrib.pop(QName(RDF, 'type'), None)
        if type_attr is not None:
            yield (element.subject, RDF.type, URI(type_attr))

        for attr, value in element.items():
            predicate = URI(QName(attr))
            if predicate not in self.ILLEGAL_PROPERTY_ATTRS:
                yield (element.subject, predicate, PlainLiteral(value, element.language))

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
                raise ParseError
            raise ParseError
        elif node_id is not None:
            if about is None:
                return BlankNode(node_id)
            raise ParseError
        elif about is not None:
            return self._uri(about, element.base_uri)
        return BlankNode()

    def _uri(self, uri, base_uri=None):
        if base_uri and not uri:
            base_uri = base_uri.rsplit('#', 1)[0]
        return URI(urllib.parse.urljoin(base_uri or '', uri))

    def _property_elements(self, element):
        # 7.2.13 Production propertyEltList
        for property_element in element:
            # 7.2.14 Production propertyElt
            self._init_element(property_element, parent=element)
            # Container Membership Property Elements: rdf:li and rdf:_n
            if property_element.uri == RDF.li:
                property_element.uri = RDF['_' + str(element.li_counter)]
                element.li_counter += 1

            id_ = property_element.attrib.pop(QName(RDF, 'ID'), None)
            parse_type = property_element.attrib.pop(QName(RDF, 'parseType'), None)
            if parse_type == "Resource":
                # 7.2.18 Production parseTypeResourcePropertyElt
                node_element = ElementTree.Element(str(QName(RDF, 'Description')))
                node_element[:] = property_element
                self._init_element(node_element, parent=property_element)
                for triple in self._node_element(node_element):
                    yield triple
                triple = (element.subject, property_element.uri, node_element.subject)
                yield triple
                if id_ is not None:
                    # 7.3 Reification Rules
                    statement_uri = self._uri('#' + id_, property_element.base_uri)
                    for triple in self._reify(statement_uri, triple):
                        yield triple
            elif parse_type == "Collection":
                # 7.2.19 Production parseTypeCollectionPropertyElt
                node_ids = []
                for node_element in property_element:
                    self._init_element(node_element, parent=property_element)
                    for triple in self._node_element(node_element):
                        yield triple
                    node_ids.append((node_element, BlankNode()))
                for node_element, object_ in node_ids:
                    break
                else:
                    object_ = RDF.nil
                triple = (element.subject, property_element.uri, object_)
                yield triple
                if id_ is not None:
                    # 7.3 Reification Rules
                    statement_uri = self._uri('#' + id_, property_element.base_uri)
                    for triple in self._reify(statement_uri, triple):
                        yield triple
                for i, (node_element, object_) in enumerate(node_ids):
                    yield (object_, RDF.first, node_element.subject)
                    try:
                        next_pair = node_ids[i + 1]
                    except IndexError:
                        next_object = RDF.nil
                    else:
                        next_element, next_object = next_pair
                    yield (object_, RDF.rest, next_object)
            elif parse_type == "Literal" or parse_type is not None:
                pass
            elif len(property_element) == 1:
                # 7.2.15 Production resourcePropertyElt
                node_element = property_element[0]
                self._init_element(node_element, parent=property_element)
                for triple in self._node_element(node_element):
                    yield triple
                triple = (element.subject, property_element.uri, node_element.subject)
                yield triple
                if id_ is not None:
                    # 7.3 Reification Rules
                    statement_uri = self._uri('#' + id_, property_element.base_uri)
                    for triple in self._reify(statement_uri, triple):
                        yield triple
            elif len(property_element) == 0:
                if property_element.text:
                    # 7.2.16 Production literalPropertyElt
                    datatype = property_element.get(QName(RDF, 'datatype'))
                    if datatype is not None:
                        object_ = TypedLiteral(property_element.text, datatype)
                    else:
                        object_ = PlainLiteral(property_element.text, property_element.language)
                    triple = (element.subject, property_element.uri, object_)
                    yield triple
                    if id_ is not None:
                        # 7.3 Reification Rules
                        statement_uri = self._uri('#' + id_, property_element.base_uri)
                        for triple in self._reify(statement_uri, triple):
                            yield triple
                else:
                    # 7.2.21 Production emptyPropertyElt
                    if not property_element.attrib:
                        object_ = PlainLiteral("", property_element.language)
                        triple = (element.subject, property_element.uri, object_)
                        yield triple
                        if id_ is not None:
                            statement_uri = self._uri('#' + id_, property_element.base_uri)
                            for triple in self._reify(statement_uri, triple):
                                yield triple
                    else:
                        resource = property_element.attrib.pop(QName(RDF, 'resource'), None)
                        node_id = property_element.attrib.pop(QName(RDF, 'nodeID'), None)
                        if resource is not None:
                            if node_id is None:
                                object_ = self._uri(resource, property_element.base_uri)
                            else:
                                raise ParseError
                        elif node_id is not None:
                            object_ = BlankNode(node_id)
                        else:
                            object_ = BlankNode()
                        triple = (element.subject, property_element.uri, object_)
                        yield triple
                        if id_ is not None:
                            statement_uri = self._uri('#' + id_, property_element.base_uri)
                            for triple in self._reify(statement_uri, triple):
                                yield triple
                        subject = object_
                        for attr, value in property_element.items():
                            predicate = URI(QName(attr))
                            if predicate != RDF.type:
                                object_ = PlainLiteral(value, property_element.language)
                            else:
                                object_ = self._uri(value, property_element.base_uri)
                            yield (subject, predicate, object_)

    def _reify(self, uri, triple):
        yield (uri, RDF.type, RDF.Statement)
        yield (uri, RDF.subject, triple[0])
        yield (uri, RDF.predicate, triple[1])
        yield (uri, RDF.object, triple[2])

