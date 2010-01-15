class Literal:
    def __init__(self, lexical_form):
        self.lexical_form = lexical_form

class PlainLiteral(Literal):
    def __init__(self, lexical_form, language=None):
        super().__init__(lexical_form)
        self.language = language

    def __eq__(self, other):
        return (isinstance(other, PlainLiteral) and
                other.lexical_form == self.lexical_form and
                other.language == self.language)

class TypedLiteral(Literal):
    def __init__(self, lexical_form, datatype):
        super().__init__(lexical_form)
        self.datatype = datatype

    def __eq__(self, other):
        return (isinstance(other, TypedLiteral) and
                other.lexical_form == self.lexical_form and
                other.datatype == self.datatype)
