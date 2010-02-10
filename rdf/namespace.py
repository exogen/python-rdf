from rdf.uri import URI


class Namespace(URI):
    def __getitem__(self, local_name):
        if isinstance(local_name, str):
            return URI(self + local_name)
        else:
            return super().__getitem__(local_name)

    def __getattr__(self, local_name):
        return URI(self + local_name)

    def __repr__(self):
        return "Namespace({!r})".format(str(self))


RDF = Namespace('http://www.w3.org/1999/02/22-rdf-syntax-ns#')
RDFS = Namespace('http://www.w3.org/2000/01/rdf-schema#')
TEST = Namespace('http://www.w3.org/2000/10/rdf-tests/rdfcore/testSchema#')
XML = Namespace('http://www.w3.org/XML/1998/namespace')
XSD = Namespace('http://www.w3.org/2001/XMLSchema#')
