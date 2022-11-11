from model import Publication

from rdflib import Graph, Literal, URIRef, Namespace
from rdflib.plugins.stores import sparqlstore
from rdflib.graph import DATASET_DEFAULT_GRAPH_ID as default_identifier
from rdflib.namespace import RDF, DCTERMS, FOAF, XSD

DATACITE = Namespace("https://purl.org/spar/datacite/")
PRISM = Namespace("http://prismstandard.org/namespaces/basic/2.0/")


class RDFConnector:
    graph: Graph

    def __init__(self, hostname: str):
        query_endpoint = hostname + '/query'
        update_endpoint = hostname + '/update'
        store = sparqlstore.SPARQLUpdateStore()
        store.open((query_endpoint, update_endpoint))
        self.graph = Graph(store, identifier=default_identifier)

    def add_to_graph(self, pub: Publication):
        # Add publication
        pub_ref = URIRef(pub.pub_id)
        self.graph.add((pub_ref, RDF.type, FOAF.Document))

        # Add title
        title_literal = Literal(pub.title, datatype=XSD.string)
        self.graph.add((pub_ref, DCTERMS.title, title_literal))

        # Add author
        author_literal = Literal(pub.author, datatype=XSD.string)
        self.graph.add((pub_ref, DCTERMS.creator, author_literal))

        # Add year issued
        issued_literal = Literal(pub.issued, datatype=XSD.year)
        self.graph.add((pub_ref, DCTERMS.issued, issued_literal))

        # Add doi
        doi_literal = Literal(pub.doi, datatype=XSD.string)
        self.graph.add((pub_ref, DATACITE.doi, doi_literal))

        # Add keywords
        for keyword in pub.keywords:
            keyword_literal = Literal(keyword, datatype=XSD.string)
            self.graph.add((pub_ref, PRISM.keyword, keyword_literal))
        return
