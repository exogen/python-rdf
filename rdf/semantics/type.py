from rdf.blanknode import BlankNode
from rdf.uri import URI
from rdf.literal import Literal, PlainLiteral, TypedLiteral, is_well_typed_xml
from rdf.namespace import RDF


class Type:
    def __init__(self, class_set):
        if isinstance(class_set, type):
            class_set = (class_set,)
        self.class_set = frozenset(class_set)
        self.blank_node = self.nnn = object()

    def __contains__(self, obj):
        return isinstance(obj, tuple(self.class_set))

class ContainerMembershipPropertyType(Type):
    def __init__(self):
        super().__init__(URI)

    def __contains__(self, obj):
        if super().__contains__(obj):
            head, sep, tail = obj.rpartition('_')
            return head == RDF and tail.isdigit()
        else:
            return False

class TypedLiteralType(Type):
    def __init__(self):
        super().__init__(TypedLiteral)
        self.lexical_form = self.sss = object()
        self.datatype = self.ddd = object()

class WellTypedXMLLiteralType(Type):
    def __init__(self):
        super().__init__(Literal)

    def __contains__(self, obj):
        return super().__contains__(obj) and is_well_typed_xml(obj)

aaa = Type(URI)
bbb = Type(URI)
ddd = Type(URI)
eee = Type(URI)
uuu = Type((URI, BlankNode))
vvv = Type((URI, BlankNode))
xxx = Type((URI, BlankNode, Literal))
yyy = Type((URI, BlankNode, Literal))
lll = Type(Literal)
llp = Type(PlainLiteral)
llt = TypedLiteralType()
llx = WellTypedXMLLiteralType()
cmp = ContainerMembershipPropertyType()

