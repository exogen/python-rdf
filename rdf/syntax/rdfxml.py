import re
import sys
import urllib.parse
from io import BytesIO, StringIO

from lxml import etree
from lxml.etree import QName

from rdf.uri import URI
from rdf.blanknode import BlankNode
from rdf.literal import PlainLiteral, TypedLiteral
from rdf.namespace import Namespace, RDF, XML
from rdf.syntax.exceptions import ParseError


_XML_ATTRS = {QName(XML, 'base'), QName(XML, 'lang')}
_OLD_ATTRS = {QName(RDF, 'aboutEach'), QName(RDF, 'aboutEachPrefix'),
              QName(RDF, 'bagID')}
_SMP_NAME = "\U00010000-\U000EFFFF" if sys.maxunicode > 65535 else "" 
_NAME = re.compile("^(?:[:A-Z_a-z\xC0-\xD6\xD8-\xF6\u00F8-\u02FF\u0370-"
    "\u037D\u037F-\u1FFF\u200C-\u200D\u2070-\u218F\u2C00-\u2FEF\u3001-"
    "\uD7FF\uF900-\uFDCF\uFDF0-\uFFFD][-.0-9\xB7"
    "\u0300-\u036F\u203F-\u2040{0}]*)+$".format(_SMP_NAME))
_NCNAME = re.compile("^(?:[A-Z_a-z\xC0-\xD6\xD8-\xF6\u00F8-\u02FF\u0370-"
    "\u037D\u037F-\u1FFF\u200C-\u200D\u2070-\u218F\u2C00-\u2FEF\u3001-"
    "\uD7FF\uF900-\uFDCF\uFDF0-\uFFFD][-.0-9\xB7"
    "\u0300-\u036F\u203F-\u2040{0}]*)+$".format(_SMP_NAME))

class Element(etree.ElementBase):
    def _init(self):
        super()._init()
        self.uri = URI(QName(self.tag))
        self.subject = None
        self.base_uri = URI(self.base) if self.base is not None else None
        self.language = self.attrib.get(QName(XML, 'lang'))
        if self.language is None:
            parent = self.getparent()
            if parent is not None:
                self.language = parent.language

class RDFXMLReader:
    CORE_SYNTAX_TERMS = {RDF.RDF, RDF.ID, RDF.about, RDF.parseType,
                         RDF.resource, RDF.nodeID, RDF.datatype}
    SYNTAX_TERMS = CORE_SYNTAX_TERMS | {RDF.Description, RDF.li}
    OLD_TERMS = {RDF.aboutEach, RDF.aboutEachPrefix, RDF.bagID}
    XML_TERMS = {XML.base, XML.lang}

    ILLEGAL_NODE_TAGS = CORE_SYNTAX_TERMS | {RDF.li} | OLD_TERMS
    ILLEGAL_PROPERTY_TAGS = CORE_SYNTAX_TERMS | {RDF.Description} | OLD_TERMS
    ILLEGAL_PROPERTY_ATTRS = SYNTAX_TERMS | OLD_TERMS

    _PARSER_LOOKUP = etree.ElementDefaultClassLookup(element=Element)
    
    def __init__(self, parser=None):
        if parser is None:
            parser = etree.XMLParser(remove_comments=True, remove_pis=True)
            parser.set_element_class_lookup(self._PARSER_LOOKUP)
        self.parser = parser
    
    def read(self, lines, base_uri=None):
        root = etree.parse(lines, self.parser, base_url=base_uri).getroot()
        ids = set()
        # rdf:RDF is not necessarily the root element.
        for element in root if root.uri == RDF.RDF else [root]:
            self._validate(element)
            for triple in self._node_element(element, ids):
                yield triple

    def _validate(self, element):
        for attr, value in element.items():
            attr = QName(attr)
            # Ignore unknown and reserved XML attributes.
            if attr.namespace is None or (attr.namespace == XML and
                                          attr not in _XML_ATTRS):
                del element.attrib[attr]
            # Validate but ignore old syntax terms.
            elif attr == QName(RDF, 'bagID'):
                if not _NCNAME.match(value):
                    raise ParseError("rdf:bagID does not match NCName: {!r}".format(value))
                del element.attrib[attr]
            elif attr in _OLD_ATTRS:
                raise ParseError

    def _node_element(self, element, ids):
        # 7.2.11 Production nodeElement
        self._validate(element)
        if element.uri in self.ILLEGAL_NODE_TAGS:
            raise ParseError("Illegal node element: {!s}".format(element.tag))

        element.subject = self._subject(element, ids)

        # 2.13 Typed Node Elements
        if element.uri != RDF.Description:
            yield (element.subject, RDF.type, element.uri)

        for triple in self._property_attrs(element):
            yield triple

        for triple in self._property_elements(element, ids):
            yield triple
    
    def _subject(self, element, ids):
        id_ = self._id(element, ids)
        node_id = element.get(QName(RDF, 'nodeID'))
        about = element.get(QName(RDF, 'about'))
        if id_ is not None:
            if node_id is None:
                if about is None:
                    return id_
                raise ParseError
            raise ParseError
        elif node_id is not None:
            if about is None:
                if _NCNAME.match(node_id):
                    return BlankNode(node_id)
                raise ParseError
            raise ParseError
        elif about is not None:
            return self._uri(about, element.base_uri)
        return BlankNode()

    def _uri(self, uri, base_uri=None):
        if base_uri and not uri:
            base_uri = base_uri.rsplit('#', 1)[0]
        return URI(urllib.parse.urljoin(base_uri or '', uri))

    def _id(self, element, ids):
        name = element.get(QName(RDF, 'ID'))
        if name is not None:
            if _NCNAME.match(name):
                uri = self._uri('#' + name, element.base_uri)
                if uri not in ids:
                    ids.add(uri)
                    return uri
                else:
                    raise ParseError("rdf:ID is not unique: {!r}".format(uri))
            else:
                raise ParseError("rdf:ID does not match NCName: {!r}".format(name))

    def _property_attrs(self, element):
        # 2.5 Property Attributes
        for attr, value in element.items():
            if attr not in _XML_ATTRS:
                predicate = URI(QName(attr))
                if predicate not in self.ILLEGAL_PROPERTY_ATTRS:
                    if predicate != RDF.type:
                        object_ = PlainLiteral(value, element.language)
                    else:
                        object_ = URI(value)
                    yield (element.subject, predicate, object_)
                elif predicate == RDF.li:
                    raise ParseError("rdf:li is not allowed as attribute")

    def _property_elements(self, parent, ids):
        # 7.2.13 Production propertyEltList
        li_counter = 1
        for element in parent:
            # 7.2.14 Production propertyElt
            self._validate(element)
            if element.uri in self.ILLEGAL_PROPERTY_TAGS:
                raise ParseError("Illegal property element: {!s}".format(element.tag))
            elif element.uri == RDF.li:
                # Container Membership Property Elements: rdf:li and rdf:_n
                element.uri = RDF['_' + str(li_counter)]
                li_counter += 1

            parse_type = element.attrib.get(QName(RDF, 'parseType'))
            legal_attrs = _XML_ATTRS | {QName(RDF, 'ID')}
            if parse_type is not None:
                legal_attrs.add(QName(RDF, 'parseType'))
                if any(attr not in legal_attrs for attr in element.keys()):
                    raise ParseError
                elif parse_type == 'Resource':
                    triples = self._parse_type_resource_property(element, parent, ids)
                elif parse_type == 'Collection':
                    triples = self._parse_type_collection_property(element, parent, ids)
                else:
                    triples = self._parse_type_literal_property(element, parent, ids)
            elif len(element) == 1:
                if all(attr not in legal_attrs for attr in element.keys()):
                    triples = self._resource_property(element, parent, ids)
                else:
                    raise ParseError
            elif len(element) == 0:
                if element.text:
                    legal_attrs.add(QName(RDF, 'datatype'))
                    if all(attr in legal_attrs for attr in element.keys()):
                        triples = self._literal_property(element, parent, ids)
                    else:
                        raise ParseError
                else:
                    triples = self._empty_property(element, parent, ids)
            for triple in triples:
                yield triple

    def _reify(self, uri, triple):
        yield (uri, RDF.type, RDF.Statement)
        yield (uri, RDF.subject, triple[0])
        yield (uri, RDF.predicate, triple[1])
        yield (uri, RDF.object, triple[2])

    def _resource_property(self, element, parent, ids):
        # 7.2.15 Production resourcePropertyElt
        node_element = element[0]
        for triple in self._node_element(node_element, ids):
            yield triple
        triple = (parent.subject, element.uri, node_element.subject)
        yield triple
        id_ = self._id(element, ids)
        if id_ is not None:
            # 7.3 Reification Rules
            for triple in self._reify(id_, triple):
                yield triple

    def _literal_property(self, element, parent, ids):
        # 7.2.16 Production literalPropertyElt
        datatype = element.get(QName(RDF, 'datatype'))
        if datatype is not None:
            object_ = TypedLiteral(element.text, URI(datatype))
        else:
            object_ = PlainLiteral(element.text, element.language)
        triple = (parent.subject, element.uri, object_)
        yield triple
        id_ = self._id(element, ids)
        if id_ is not None:
            # 7.3 Reification Rules
            for triple in self._reify(id_, triple):
                yield triple

    def _parse_type_resource_property(self, element, parent, ids):
        # 7.2.18 Production parseTypeResourcePropertyElt
        node_element = element.makeelement(QName(RDF, 'Description'))
        node_element[:] = element
        for triple in self._node_element(node_element, ids):
            yield triple
        triple = (parent.subject, element.uri, node_element.subject)
        yield triple
        id_ = self._id(element, ids)
        if id_ is not None:
            # 7.3 Reification Rules
            for triple in self._reify(id_, triple):
                yield triple

    def _parse_type_collection_property(self, element, parent, ids):
        # 7.2.19 Production parseTypeCollectionPropertyElt
        node_ids = []
        for node_element in element:
            for triple in self._node_element(node_element, ids):
                yield triple
            node_ids.append((node_element, BlankNode()))
        for node_element, object_ in node_ids:
            break
        else:
            object_ = RDF.nil
        triple = (parent.subject, element.uri, object_)
        yield triple
        id_ = self._id(element, ids)
        if id_ is not None:
            # 7.3 Reification Rules
            for triple in self._reify(id_, triple):
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

    def _parse_type_literal_property(self, element, parent, ids):
        literal = element.text or ""
        if len(element):
            tree = etree.ElementTree(element[0])
            bytes_io = BytesIO()
            tree.write_c14n(bytes_io, exclusive=True, with_comments=True)
            literal += bytes_io.getvalue().decode('utf-8')
            literal += element[0].tail or ""
        object_ = TypedLiteral(literal, RDF.XMLLiteral)
        triple = (parent.subject, element.uri, object_)
        yield triple
        id_ = self._id(element, ids)
        if id_ is not None:
            # 7.3 Reification Rules
            for triple in self._reify(id_, triple):
                yield triple

    def _empty_property(self, element, parent, ids):
        # 7.2.21 Production emptyPropertyElt
        id_ = self._id(element, ids)
        literal_attrs = _XML_ATTRS | {QName(RDF, 'ID')}
        if all(attr in literal_attrs for attr in element.keys()):
            object_ = PlainLiteral("", element.language)
            triple = (parent.subject, element.uri, object_)
            yield triple
            if id_ is not None:
                for triple in self._reify(id_, triple):
                    yield triple
        else:
            resource = element.attrib.get(QName(RDF, 'resource'))
            node_id = element.attrib.get(QName(RDF, 'nodeID'))
            if resource is not None:
                if node_id is None:
                    object_ = self._uri(resource, element.base_uri)
                else:
                    raise ParseError
            elif node_id is not None:
                if _NCNAME.match(node_id):
                    object_ = BlankNode(node_id)
                else:
                    raise ParseError("rdf:nodeID does not match NCName: {!r}".format(node_id))
            else:
                object_ = BlankNode()
            triple = (parent.subject, element.uri, object_)
            yield triple
            if id_ is not None:
                for triple in self._reify(id_, triple):
                    yield triple
            subject = object_
            property_attrs = set(element.keys())
            property_attrs -= literal_attrs | {QName(RDF, 'resource'),
                                               QName(RDF, 'nodeID')}
            for attr in property_attrs:
                predicate = URI(QName(attr))
                if predicate in self.XML_TERMS:
                    continue
                elif predicate in self.ILLEGAL_PROPERTY_ATTRS:
                    raise ParseError
                value = element.get(attr)
                if predicate != RDF.type:
                    object_ = PlainLiteral(value, element.language)
                else:
                    object_ = self._uri(value, element.base_uri)
                yield (subject, predicate, object_)

