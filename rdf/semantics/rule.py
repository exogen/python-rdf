from collections import defaultdict
from itertools import product

from rdf.blanknode import BlankNode
from rdf.semantics.type import Type, TypeDescriptor, TypedLiteralType, cmp
from rdf.namespace import RDFS


class Context:
    def __init__(self):
        self.blank_node_allocations = {}

    def allocate(self, node, blank_node=None):
        if blank_node is None:
            blank_node = BlankNode()
        return self.blank_node_allocations.setdefault(node, blank_node)

class Rule:
    def __init__(self, antecedent, consequent, name=None):
        self.antecedent = set(Pattern(pattern) for pattern in antecedent)
        self.consequent = set(Pattern(pattern) for pattern in consequent)
        self.name = name

    def apply(self, graph, context):
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
                            if merged_token is not None:
                                if isinstance(token, Type):
                                    if merged_token not in token:
                                        break
                                elif merged_token != token:
                                    break
                        else:
                            merged_binding.update(binding)
                            continue
                        break
                    else:
                        for pattern in self.consequent:
                            yield pattern.tokenize(merged_binding, context)
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

    def tokenize(self, binding, context):
        tokens = []
        for type_or_token in self:
            token = binding.get(type_or_token)
            if token is None:
                if isinstance(type_or_token, TypeDescriptor):
                    type_token = binding[type_or_token.type]
                    token = type_or_token(type_token, context)
                else:
                    token = type_or_token
            tokens.append(token)
        return tuple(tokens)

