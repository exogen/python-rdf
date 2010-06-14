from collections import defaultdict
from itertools import product

from rdf.blanknode import BlankNode
from rdf.semantics.type import Type, TypedLiteralType


class Rule:
    def __init__(self, antecedent, consequent, name=None):
        self.antecedent = set(Pattern(pattern) for pattern in antecedent)
        self.consequent = set(Pattern(pattern) for pattern in consequent)
        self.name = name

    def apply(self, graph):
        if self.antecedent:
            bindings = defaultdict(list)
            for pattern in self.antecedent:
                for triple in graph:
                    if pattern.matches(triple):
                        binding = {}
                        for type_or_token, token in zip(pattern, triple):
                            if isinstance(type_or_token, Type):
                                binding[type_or_token] = token
                        bindings[pattern].append(binding)
                if pattern not in bindings:
                    break
            if len(bindings) == len(self.antecedent):
                for candidate in product(*bindings.values()):
                    merged_binding = {}
                    for binding in candidate:
                        for type_, token in binding.items():
                            merged_token = merged_binding.get(type_)
                            if (merged_token is not None and
                                merged_token != token):
                                break
                        else:
                            merged_binding.update(binding)
                            continue
                        break
                    else:
                        for pattern in self.consequent:
                            yield pattern.tokenize(merged_binding)
        else:
            for triple in self.consequent:
                yield triple

class Pattern(tuple):
    def matches(self, triple):
        for type_or_token, token in zip(self, triple):
            if isinstance(type_or_token, Type):
                if token not in type_or_token:
                    return False
            elif token != type_or_token:
                return False
        return True

    def tokenize(self, binding):
        bnode_markers = set(type_.blank_node for type_ in binding)
        bnodes = {}
        tokens = []
        for type_or_token in self:
            token = binding.get(type_or_token)
            if token is not None:
                tokens.append(token)
            elif type_or_token in bnode_markers:
                bnode = bnodes.get(type_or_token)
                if bnode is None:
                    bnode = bnodes.setdefault(type_or_token, BlankNode())
                tokens.append(bnode)
            else:
                tokens.append(type_or_token)
        return tuple(tokens)

