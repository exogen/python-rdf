from rdf.namespace import RDF, RDFS, XSD
from rdf.graph import Graph
from rdf.semantics.rule import Rule, Pattern, Context
from rdf.semantics.type import aaa, bbb, ddd, eee, uuu, vvv, www, zzz, xxx, \
                               yyy, lll, llp, llt, lls, llx, cmp


class Entailment:
    def __init__(self, rules=(), axioms=(), conditions=()):
        self.rules = list(rules)
        self.axioms = {Pattern(axiom) for axiom in axioms}
        self.conditions = list(conditions)

    def entails(self, s, e):
        if s >= e:
            return True
        entailed = Graph(s | self.axioms)
        context = Context()
        num_triples = -1
        while len(entailed) != num_triples:
            num_triples = len(entailed)
            for rule in self.rules:
                entailed.update(rule.apply(entailed, context))
                if len(entailed) != num_triples:
                    if e <= entailed:
                        return True
        for triple in e:
            if triple not in entailed:
                for entailed_triple in entailed:
                    pattern = Pattern(entailed_triple)
                    if pattern.matches(triple):
                        break
                else:
                    return False
        return True

# Simple entailment rules
# http://www.w3.org/TR/rdf-mt/#simpleRules
se1 = Rule({(uuu, aaa, xxx)}, {(uuu, aaa, xxx.nnn)}, name='se1')
se2 = Rule({(uuu, aaa, xxx)}, {(uuu, aaa, uuu.nnn)}, name='se2')

SIMPLE_ENTAILMENT = Entailment([se1, se2])

# Literal generalization rule
lg = Rule({(uuu, aaa, lll)}, {(uuu, aaa, lll.nnn)}, name='lg')

SIMPLE_ENTAILMENT_LG = Entailment([lg])

# RDF entailment rules
# http://www.w3.org/TR/rdf-mt/#RDFRules
rdf1 = Rule({(uuu, aaa, yyy)}, {(aaa, RDF.type, RDF.Property)}, name='rdf1')
rdf2 = Rule({(uuu, aaa, llx)},
            {(llx.nnn, RDF.type, RDF.XMLLiteral)}, name='rdf2')

RDF_AXIOMATIC_TRIPLES = {(RDF.type, RDF.type, RDF.Property),
                         (RDF.subject, RDF.type, RDF.Property),
                         (RDF.predicate, RDF.type, RDF.Property),
                         (RDF.object, RDF.type, RDF.Property),
                         (RDF.first, RDF.type, RDF.Property),
                         (RDF.rest, RDF.type, RDF.Property),
                         (RDF.value, RDF.type, RDF.Property),
                         (cmp, RDF.type, RDF.Property),
                         (RDF.nil, RDF.type, RDF.Property)}

RDF_ENTAILMENT = Entailment([rdf1, rdf2], RDF_AXIOMATIC_TRIPLES)

# RDFS entailment rules
# http://www.w3.org/TR/rdf-mt/#RDFSRules
rdfs1 = Rule({(uuu, aaa, llp)},
             {(llp.nnn, RDF.type, RDFS.Literal)}, name='rdfs1')
rdfs2 = Rule({(aaa, RDFS.domain, xxx), (uuu, aaa, yyy)},
             {(uuu, RDF.type, xxx)}, name='rdfs2')
rdfs3 = Rule({(aaa, RDFS.range, xxx), (uuu, aaa, vvv)},
             {(vvv, RDF.type, xxx)}, name='rdfs3')
rdfs4a = Rule({(uuu, aaa, xxx)},
              {(uuu, RDF.type, RDFS.Resource)}, name='rdfs4a')
rdfs4b = Rule({(uuu, aaa, vvv)},
              {(vvv, RDF.type, RDFS.Resource)}, name='rdfs4b')
rdfs5 = Rule({(uuu, RDFS.subPropertyOf, vvv), (vvv, RDFS.subPropertyOf, xxx)},
             {(uuu, RDFS.subPropertyOf, xxx)}, name='rdfs5')
rdfs6 = Rule({(uuu, RDF.type, RDF.Property)},
             {(uuu, RDFS.subPropertyOf, uuu)}, name='rdfs6')
rdfs7 = Rule({(aaa, RDFS.subPropertyOf, bbb), (uuu, aaa, yyy)},
             {(uuu, bbb, yyy)}, name='rdfs7')
rdfs8 = Rule({(uuu, RDF.type, RDFS.Class)},
             {(uuu, RDFS.subClassOf, RDFS.Resource)}, name='rdfs8')
rdfs9 = Rule({(uuu, RDFS.subClassOf, xxx), (vvv, RDF.type, uuu)},
             {(vvv, RDF.type, xxx)}, name='rdfs9')
rdfs10 = Rule({(uuu, RDF.type, RDFS.Class)},
              {(uuu, RDFS.subClassOf, uuu)}, name='rdfs10')
rdfs11 = Rule({(uuu, RDFS.subClassOf, vvv), (vvv, RDFS.subClassOf, xxx)},
              {(uuu, RDFS.subClassOf, xxx)}, name='rdfs11')
rdfs12 = Rule({(uuu, RDF.type, RDFS.ContainerMembershipProperty)},
              {(uuu, RDFS.subPropertyOf, RDFS.member)}, name='rdfs12')
rdfs13 = Rule({(uuu, RDF.type, RDFS.Datatype)},
              {(uuu, RDFS.subClassOf, RDFS.Literal)}, name='rdfs13')

RDFS_ENTAILMENT = Entailment(
    [rdfs1, rdfs2, rdfs3, rdfs4a, rdfs4b, rdfs5, rdfs6, rdfs7, rdfs8, rdfs9,
     rdfs10, rdfs11, rdfs12, rdfs13],
    [(RDF.type, RDFS.domain, RDFS.Resource),
     (RDFS.domain, RDFS.domain, RDF.Property),
     (RDFS.range, RDFS.domain, RDF.Property),
     (RDFS.subPropertyOf, RDFS.domain, RDF.Property),
     (RDFS.subClassOf, RDFS.domain, RDFS.Class),
     (RDF.subject, RDFS.domain, RDF.Statement),
     (RDF.predicate, RDFS.domain, RDF.Statement),
     (RDF.object, RDFS.domain, RDF.Statement),
     (RDFS.member, RDFS.domain, RDFS.Resource),
     (RDF.first, RDFS.domain, RDF.List),
     (RDF.rest, RDFS.domain, RDF.List),
     (RDFS.seeAlso, RDFS.domain, RDFS.Resource),
     (RDFS.isDefinedBy, RDFS.domain, RDFS.Resource),
     (RDFS.comment, RDFS.domain, RDFS.Resource),
     (RDFS.label, RDFS.domain, RDFS.Resource),
     (RDF.value, RDFS.domain, RDFS.Resource),
     (RDF.type, RDFS.range, RDFS.Class),
     (RDFS.domain, RDFS.range, RDFS.Class),
     (RDFS.range, RDFS.range, RDFS.Class),
     (RDFS.subPropertyOf, RDFS.range, RDF.Property),
     (RDFS.subClassOf, RDFS.range, RDFS.Class),
     (RDF.subject, RDFS.range, RDFS.Resource),
     (RDF.predicate, RDFS.range, RDFS.Resource),
     (RDF.object, RDFS.range, RDFS.Resource),
     (RDFS.member, RDFS.range, RDFS.Resource),
     (RDF.first, RDFS.range, RDFS.Resource),
     (RDF.rest, RDFS.range, RDF.List),
     (RDFS.seeAlso, RDFS.range, RDFS.Resource),
     (RDFS.isDefinedBy, RDFS.range, RDFS.Resource),
     (RDFS.comment, RDFS.range, RDFS.Literal),
     (RDFS.label, RDFS.range, RDFS.Literal),
     (RDF.value, RDFS.range, RDFS.Resource),
     (RDF.Alt, RDFS.subClassOf, RDFS.Container),
     (RDF.Bag, RDFS.subClassOf, RDFS.Container),
     (RDF.Seq, RDFS.subClassOf, RDFS.Container),
     (RDFS.ContainerMembershipProperty, RDFS.subClassOf, RDF.Property),
     (RDFS.isDefinedBy, RDFS.subPropertyOf, RDFS.seeAlso),
     (RDF.XMLLiteral, RDF.type, RDFS.Datatype),
     (RDF.XMLLiteral, RDFS.subClassOf, RDFS.Literal),
     (RDFS.Datatype, RDFS.subClassOf, RDFS.Class),
     (cmp, RDF.type, RDFS.ContainerMembershipProperty),
     (cmp, RDFS.domain, RDFS.Resource),
     (cmp, RDFS.range, RDFS.Resource)])

# Extensional entailment rules
# http://www.w3.org/TR/rdf-mt/#RDFSExtRules
ext1 = Rule({(uuu, RDFS.domain, vvv), (vvv, RDFS.subClassOf, zzz)},
            {(uuu, RDFS.domain, zzz)}, name='ext1')
ext2 = Rule({(uuu, RDFS.range, vvv), (vvv, RDFS.subClassOf, zzz)},
            {(uuu, RDFS.range, zzz)}, name='ext2')
ext3 = Rule({(uuu, RDFS.domain, vvv), (www, RDFS.subPropertyOf, uuu)},
            {(www, RDFS.domain, vvv)}, name='ext3')
ext4 = Rule({(uuu, RDFS.range, vvv), (www, RDFS.subPropertyOf, uuu)},
            {(www, RDFS.range, vvv)}, name='ext4')
ext5 = Rule({(RDF.type, RDFS.subPropertyOf, www), (www, RDFS.domain, vvv)},
            {(RDFS.Resource, RDFS.subClassOf, vvv)}, name='ext5')
ext6 = Rule({(RDFS.subClassOf, RDFS.subPropertyOf, www),
             (www, RDFS.domain, vvv)},
            {(RDFS.Class, RDFS.subClassOf, vvv)}, name='ext6')
ext7 = Rule({(RDFS.subPropertyOf, RDFS.subPropertyOf, www),
             (www, RDFS.domain, vvv)},
            {(RDF.Property, RDFS.subClassOf, vvv)}, name='ext7')
ext8 = Rule({(RDFS.subClassOf, RDFS.subPropertyOf, www),
             (www, RDFS.range, vvv)},
            {(RDFS.Class, RDFS.subClassOf, vvv)}, name='ext8')
ext9 = Rule({(RDFS.subPropertyOf, RDFS.subPropertyOf, www),
             (www, RDFS.range, vvv)},
            {(RDF.Property, RDFS.subClassOf, vvv)}, name='ext9')

EXTENSIONAL_ENTAILMENT = Entailment(RDFS_ENTAILMENT.rules +
    [ext1, ext2, ext3, ext4, ext5, ext6, ext7, ext8, ext9],
    RDFS_ENTAILMENT.axioms)

# Datatype entailment rules
# http://www.w3.org/TR/rdf-mt/#DtypeRules
rdfD1 = Rule({(ddd, RDF.type, RDFS.Datatype), (uuu, aaa, llt)},
             {(llt.nnn, RDF.type, llt.ddd)}, name='rdfD1')
#rdfD2 = Rule({(ddd, RDF.type, RDFS.Datatype), (uuu, aaa, llt)},
#             {(uuu, aaa, )}, name='rdfD1')
rdfD3 = Rule({(ddd, RDF.type, RDFS.Datatype), (uuu, aaa, llt)},
             {(llt.nnn, RDF.type, llt.ddd)}, name='rdfD3')

xsd1a = Rule({(uuu, aaa, llp)},
             {(uuu, aaa, llp.sss(XSD.string))}, name='xsd 1a')
xsd1b = Rule({(uuu, aaa, lls)},
             {(uuu, aaa, lls.sss())}, name='xsd 1b')

DATATYPE_ENTAILMENT = Entailment([rdfD1, rdfD3, xsd1a, xsd1b])

