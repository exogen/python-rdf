from rdf.uri import URI


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

class TypedLiteral(Literal):
    __slots__ = 'datatype'

    def __init__(self, lexical_form, datatype):
        super().__init__(lexical_form)
        self.datatype = datatype

    def __eq__(self, other):
        return (isinstance(other, TypedLiteral) and
                other.lexical_form == self.lexical_form and
                other.datatype == self.datatype)

    def __hash__(self):
        return (hash(TypedLiteral) ^
                hash(self.lexical_form) ^
                hash(self.datatype))

    def __repr__(self):
        return "TypedLiteral({!r}, {!r})".format(self.lexical_form,
                                                 self.datatype)
