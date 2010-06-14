from rdf.namespace import RDF
from rdf.semantics.type import cmp


RDF_AXIOMATIC_TRIPLES = {(RDF.type, RDF.type, RDF.Property),
                         (RDF.subject, RDF.type, RDF.Property),
                         (RDF.predicate, RDF.type, RDF.Property),
                         (RDF.object, RDF.type, RDF.Property),
                         (RDF.first, RDF.type, RDF.Property),
                         (RDF.rest, RDF.type, RDF.Property),
                         (RDF.value, RDF.type, RDF.Property),
                         (cmp, RDF.type, RDF.Property),
                         (RDF.nil, RDF.type, RDF.List)}
