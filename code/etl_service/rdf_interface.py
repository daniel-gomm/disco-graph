from model import publication

from rdflib import Graph, Literal, URIRef, Namespace
from rdflib.plugins.stores import sparqlstore
from rdflib.graph import DATASET_DEFAULT_GRAPH_ID as default_identifier
from rdflib.namespace import RDF, DCTERMS, FOAF, XSD

DATACITE = Namespace("https://purl.org/spar/datacite/")
PRISM = Namespace("http://prismstandard.org/namespaces/basic/2.0/")


graph = None

def init() -> None:
    # for local debugging only
    query_endpoint = 'http://localhost:3030/ds/query'
    update_endpoint = 'http://localhost:3030/ds/update'

    store = sparqlstore.SPARQLStore()
    store.open((query_endpoint, update_endpoint))
    graph = Graph(store, identifier=default_identifier)

def add_publication(pub:publication):
    if not graph:
        init()
    #Add publication
    pub_ref = URIRef(pub.pub_id)
    graph.add((pub_ref, RDF.type, FOAF.Document))

    #Add title
    title_literal = Literal(pub.title, datatype=XSD.string)
    graph.add((pub_ref, DCTERMS.title, title_literal))

    #Add author
    author_literal = Literal(pub.author, datatype=XSD.string)
    graph.add((pub_ref, DCTERMS.creator, author_literal))

    #Add year issued
    issued_literal = Literal(pub.issued, datatype=XSD.year)
    graph.add((pub_ref, DCTERMS.issued, issued_literal))

    #Add doi
    doi_literal = Literal(pub.doi, datatype=XSD.string)
    graph.add((pub_ref, DATACITE.doi, doi_literal))

    #Add keywords
    for keyword in pub.keywords:
        keyword_literal = Literal(keyword, XSD.string)
        graph.add((pub_ref, PRISM.keyword, keyword_literal))