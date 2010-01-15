class Resource:
    def __new__(cls, uri=None):
        from rdf.uri import URI
        from rdf.blanknode import BlankNode
        
        if cls is Resource:
            if uri is not None:
                cls = URI
            else:
                cls = BlankNode
        args = (uri,) if issubclass(cls, URI) else ()
        return super().__new__(cls, *args)

