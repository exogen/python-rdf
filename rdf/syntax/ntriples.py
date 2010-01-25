import re
from io import StringIO
from urllib.parse import urljoin

from rdf.blanknode import BlankNode
from rdf.uri import URI
from rdf.literal import PlainLiteral, TypedLiteral


class ParseError(Exception):
    pass

class InvalidEscapeSequence(ParseError):
    pass

class NTriplesReader:
    # Grammar adapted from: http://www.w3.org/TR/rdf-testcases/#ntrip_grammar
    _CHARACTER = r'[ -~]'
    _NAME = r'(?:[A-Za-z][A-Za-z0-9]*)'
    _NODE_ID = r'(?:_:{0})'.format(_NAME)
    _ABSOLUTE_URI = r'(?:{0}+)'.format(_CHARACTER)
    _URIREF = r'(?:<{0}>)'.format(_ABSOLUTE_URI)
    _LANGUAGE = r'(?:[a-z]+(?:-[a-z0-9]+)*)'
    _STRING = r'(?:(?:\\"|[ !#-~])*)'
    _LANG_STRING = r'(?:"{0}"(?:@{1})?)'.format(_STRING, _LANGUAGE)
    _DATATYPE_STRING = r'(?:"{0}"\^\^{1})'.format(_STRING, _URIREF)
    _LITERAL = r'(?:{0}|{1})'.format(_DATATYPE_STRING, _LANG_STRING)
    _SUBJECT = r'(?:{0}|{1})'.format(_URIREF, _NODE_ID)
    _PREDICATE = _URIREF
    _OBJECT = r'(?:{0}|{1}|{2})'.format(_URIREF, _NODE_ID, _LITERAL)
    _WS = r'[ \t]'
    _TRIPLE = r'(?:({0}){ws}+({1}){ws}+({2}){ws}*\.{ws}*)'.format(_SUBJECT,
                                                                  _PREDICATE,
                                                                  _OBJECT,
                                                                  ws=_WS)
    _EOLN = r'(?:\r\n|\r|\n|\Z)'
    _COMMENT = r'(?:#{0}*)'.format(_CHARACTER)
    _LINE = r'(?:{0}*(?:{1}|{2})?{3})'.format(_WS, _COMMENT, _TRIPLE, _EOLN)
    
    LINE = re.compile(_LINE)
    ESCAPE = re.compile(r'\\(u[0-9A-F]{4}|U[0-9A-F]{8}|.)')
    ESCAPE_MAP = {'t': '\t', 'n': '\n', 'r': '\r', '"': '"', '\\': '\\'}

    def read(self, lines, uri=None):
        if isinstance(lines, str):
            lines = StringIO(lines)

        for line_num, line in enumerate(lines):
            while line:
                match = self.LINE.match(line)
                if match:
                    triple = match.groups()
                    if None not in triple:
                        yield self._triple(triple, uri)
                    line = line[match.end():]
                else:
                    raise ParseError("Error parsing line {}".format(line_num))

    def _triple(self, tokens, uri):
        subject, predicate, object_ = tokens
        return (self._subject(subject, uri),
                self._predicate(predicate, uri),
                self._object(object_, uri))

    def _subject(self, token, uri):
        if token.startswith('<'):
            return self._uriref(token, uri)
        else:
            return self._node_id(token)
    
    def _predicate(self, token, uri):
        return self._uriref(token, uri)

    def _object(self, token, uri):
        if token.startswith('<'):
            return self._uriref(token, uri)
        elif token.startswith('_:'):
            return self._node_id(token)
        else:
            return self._literal(token, uri)

    def _uriref(self, token, uri):
        return URI(urljoin(uri or '', self._string(token[1:-1])))

    def _literal(self, token, uri):
        if token.endswith('>'):
            tokens = token.rsplit('^^', 1)
            lexical_form = self._string(tokens[0][1:-1])
            datatype = self._uriref(tokens[1], uri)
            return TypedLiteral(lexical_form, datatype)
        else:
            tokens = token.rsplit('@', 1)
            lexical_form = self._string(tokens[0][1:-1])
            if len(tokens) == 1:
                language = None
            else:
                language = tokens[1]
            return PlainLiteral(lexical_form, language)

    def _string(self, token):
        return self.ESCAPE.sub(self._unescape, token)

    def _unescape(self, match):
        seq = match.group(1)
        try:
            return self.ESCAPE_MAP[seq]
        except KeyError:
            if seq[0] in 'uU' and len(seq) > 1:
                return chr(int(seq[1:], 16))
        raise InvalidEscapeSequence("Invalid escape sequence: "
                                    "{!r}".format(seq))

    def _node_id(self, token):
        return BlankNode(token[2:])

