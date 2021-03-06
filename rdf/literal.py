import io
from decimal import Decimal

import lxml.etree

from rdf.blanknode import BlankNode
from rdf.uri import URI
from rdf.namespace import XSD
from rdf.exceptions import UnsupportedDatatype, IllTypedLiteral


class Literal:
    __slots__ = 'lexical_form'

    def __new__(cls, lexical_form, language_or_datatype=None):
        if cls is Literal:
            if isinstance(language_or_datatype, URI):
                cls = TypedLiteral
            else:
                cls = PlainLiteral
        return super().__new__(cls)

    def __init__(self, lexical_form):
        self.lexical_form = lexical_form

    def __lt__(self, other):
        if other is None or isinstance(other, (BlankNode, URI)):
            return False
        else:
            return NotImplemented

    def __gt__(self, other):
        if other is None or isinstance(other, (BlankNode, URI)):
            return True
        else:
            return NotImplemented

class PlainLiteral(Literal):
    __slots__ = 'language'

    def __init__(self, lexical_form, language=None):
        super().__init__(lexical_form)
        self.language = language and language.lower()

    def __repr__(self):
        if self.language is None:
            return "PlainLiteral({!r})".format(self.lexical_form)
        else:
            return "PlainLiteral({!r}, {!r})".format(self.lexical_form,
                                                     self.language)

    def __eq__(self, other):
        return (isinstance(other, PlainLiteral) and
                other.lexical_form == self.lexical_form and
                other.language == self.language)

    def __hash__(self):
        return (hash(PlainLiteral) ^
                hash(self.lexical_form) ^
                hash(self.language))
    
    def __lt__(self, other):
        if (isinstance(other, PlainLiteral) and
            self.language is None and other.language is None):
            return self.lexical_form < other.lexical_form
        elif (isinstance(other, TypedLiteral) and
              other.datatype == XSD.string and
              self.lexical_form == other.lexical_form):
            return True
        else:
            return super().__lt__(other)
    
    def __gt__(self, other):
        if (isinstance(other, PlainLiteral) and
            self.language is None and other.language is None):
            return self.lexical_form > other.lexical_form
        elif (isinstance(other, TypedLiteral) and
              other.datatype == XSD.string and
              self.lexical_form == other.lexical_form):
            return False
        else:
            return super().__gt__(other)

LEXICAL_VALUE_MAP = {XSD.string: str,
                     XSD.integer: int,
                     XSD.decimal: Decimal}

class TypedLiteral(Literal):
    __slots__ = 'datatype'

    def __init__(self, lexical_form, datatype):
        super().__init__(lexical_form)
        if isinstance(datatype, str):
            if not isinstance(datatype, URI):
                datatype = URI(datatype)
            self.datatype = datatype
        else:
            raise TypeError("datatype must be a string")

    def __repr__(self):
        return "TypedLiteral({!r}, {!r})".format(self.lexical_form,
                                                 self.datatype)

    def __eq__(self, other):
        return (isinstance(other, TypedLiteral) and
                other.lexical_form == self.lexical_form and
                other.datatype == self.datatype)

    def __hash__(self):
        return (hash(TypedLiteral) ^
                hash(self.lexical_form) ^
                hash(self.datatype))

    def __lt__(self, other):
        if (isinstance(other, TypedLiteral) and
            self.datatype == other.datatype == XSD.string):
            return self.lexical_form < other.lexical_form
        else:
            return super().__lt__(other)

    def __gt__(self, other):
        if (isinstance(other, TypedLiteral) and
            self.datatype == other.datatype == XSD.string):
            return self.lexical_form > other.lexical_form
        else:
            return super().__gt__(other)

    def value(self, lexical_value_map=LEXICAL_VALUE_MAP):
        parser = lexical_value_map.get(self.datatype)
        if parser is not None:
            try:
                return parser(self.lexical_form)
            except Exception as e:
                raise IllTypedLiteral(self) from e
        else:
            raise UnsupportedDatatype(self.datatype)

def is_well_typed_xml(str_or_literal):
    if isinstance(str_or_literal, Literal):
        str_or_literal = str_or_literal.lexical_form
    try:
        element = lxml.etree.XML(str_or_literal)
    except lxml.etree.XMLSyntaxError:
        return False
    else:
        tree = lxml.etree.ElementTree(element)
        f = io.BytesIO()
        tree.write_c14n(f, exclusive=True, with_comments=True)
        return str_or_literal.encode('utf-8') == f.getvalue()

