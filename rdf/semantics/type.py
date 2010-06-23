from rdf.blanknode import BlankNode
from rdf.uri import URI
from rdf.literal import Literal, PlainLiteral, TypedLiteral, is_well_typed_xml
from rdf.namespace import RDF, XSD
from rdf.util import UniversalSet


class TypeDescriptor:
    def __init__(self, type):
        self.type = type

class BlankNodeDescriptor(TypeDescriptor):
    def __call__(self, obj, context):
        return context.allocate(obj)

class Type:
    def __init__(self, class_set):
        if isinstance(class_set, type):
            class_set = (class_set,)
        self.class_set = set(class_set)
        self.blank_node = self.nnn = BlankNodeDescriptor(self)

    def __repr__(self):
        return "Type({!r})".format(self.class_set)

    def __contains__(self, obj):
        if not isinstance(obj, Type):
            return isinstance(obj, tuple(self.class_set))
        else:
            return obj.class_set <= self.class_set

    def __lt__(self, other):
        return hash(self) < hash(other)

    def __gt__(self, other):
        return hash(self) > hash(other)

class ContainerMembershipPropertyType(Type):
    def __init__(self):
        super().__init__(URI)

    def __contains__(self, obj):
        if isinstance(obj, ContainerMembershipPropertyType):
            return True
        elif super().__contains__(obj):
            head, sep, tail = obj.rpartition('_')
            return head == RDF and tail.isdigit()
        else:
            return False

    def __repr__(self):
        return "<ContainerMembershipPropertyType {rdf:_1, rdf:_2, ...}>"

class DatatypeDescriptor(TypeDescriptor):
    def __call__(self, obj, context):
        return obj.datatype

class LiteralDescriptor(TypeDescriptor):
    def __init__(self, type, datatype=None):
        super().__init__(type)
        self.datatype = datatype

    def __call__(self, obj, context):
        if self.datatype is None:
            return PlainLiteral(obj.lexical_form)
        else:
            return TypedLiteral(obj.lexical_form, self.datatype)

class LiteralType(Type):
    def __init__(self):
        super().__init__(Literal)

    def literal(self, datatype=None):
        return LiteralDescriptor(self, datatype)

    sss = literal

class TypedLiteralType(LiteralType):
    def __init__(self, datatype=None):
        super(LiteralType, self).__init__(TypedLiteral)
        if datatype is None:
            datatype = UniversalSet()
        elif isinstance(datatype, (str, Type)):
            datatype = {datatype}
        if not isinstance(datatype, (set, frozenset)):
            datatype = set(datatype)
        self.datatype_set = datatype
        self.datatype = self.ddd = DatatypeDescriptor(self)

    def __contains__(self, obj):
        return super().__contains__(obj) and obj.datatype in self.datatype_set

class PlainLiteralType(LiteralType):
    def __init__(self, language=None):
        super(LiteralType, self).__init__(PlainLiteral)
        if language is None:
            language = UniversalSet()
        elif isinstance(language, str):
            language = {language}
        if not isinstance(language, (set, frozenset)):
            language = set(language)
        self.language_set = language

    def __contains__(self, obj):
        return super().__contains__(obj) and obj.language in self.language_set

class WellTypedXMLLiteralType(Type):
    def __init__(self):
        super().__init__(Literal)

    def __contains__(self, obj):
        return super().__contains__(obj) and is_well_typed_xml(obj)

aaa = Type(URI)
bbb = Type(URI)
ddd = Type(URI)
eee = Type(URI)
uuu = Type({URI, BlankNode})
vvv = Type({URI, BlankNode})
www = Type({URI, BlankNode})
zzz = Type({URI, BlankNode})
xxx = Type({URI, BlankNode, Literal})
yyy = Type({URI, BlankNode, Literal})
lll = Type(Literal)
llp = PlainLiteralType()
llt = TypedLiteralType()
lls = TypedLiteralType(XSD.string)
lld = TypedLiteralType(ddd)
llx = WellTypedXMLLiteralType()
cmp = ContainerMembershipPropertyType()

