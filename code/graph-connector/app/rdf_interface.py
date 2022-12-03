from .model.model import Publication, Keyword, AdditionalAttribute, ValueWithLanguage
from .rdf import queries

from rdflib.term import Node, Variable
from rdflib import Graph, Literal, URIRef, Namespace
from rdflib.plugins.stores import sparqlstore
from rdflib.graph import DATASET_DEFAULT_GRAPH_ID as default_identifier
from rdflib.namespace import RDF, DCTERMS, FOAF, XSD, RDFS

SG_PREFIX = "https://sci-graph.kit.edu/0.1/"
PUBLICATION_PREFIX = SG_PREFIX + "publication/"
KEYWORD_PREFIX = SG_PREFIX + "keyword/"
ATTRIBUTE_PREFIX = SG_PREFIX + "attribute/"

DATACITE = Namespace("https://purl.org/spar/datacite/")
PRISM = Namespace("http://prismstandard.org/namespaces/basic/2.0/")
SGC = Namespace(SG_PREFIX + "classes/")
SGP = Namespace(SG_PREFIX + "properties/")


def getId(value: str) -> str:
    return value.replace(" ", "_").lower()


class RDFConnector:
    graph: Graph

    def __init__(self, hostname: str = None, graph: Graph = None):
        if hostname:
            query_endpoint = hostname + '/query'
            update_endpoint = hostname + '/update'
            store = sparqlstore.SPARQLUpdateStore(query_endpoint=query_endpoint, update_endpoint=update_endpoint,
                                                  context_aware=False, returnFormat='json')
            # store.open((query_endpoint, update_endpoint))
            self.graph = Graph(store, identifier=default_identifier)
        elif graph:
            self.graph = graph

    def add_publication(self, pub: Publication) -> None:
        pub_ref = URIRef(PUBLICATION_PREFIX + pub.publication_id)

        title_literal = Literal(pub.title, datatype=XSD.string)
        author_literal = Literal(pub.author, datatype=XSD.string)
        issued_literal = Literal(pub.issued, datatype=XSD.year)
        doi_literal = Literal(pub.doi, datatype=XSD.string)
        created_literal = Literal(pub.created, datatype=XSD.dateTimeStamp)
        language_literal = Literal(pub.language, datatype=XSD.language)

        self.add_if_new([
            (pub_ref, RDF.type, FOAF.Document),
            (pub_ref, DCTERMS.title, title_literal),
            (pub_ref, DCTERMS.creator, author_literal),
            (pub_ref, DCTERMS.issued, issued_literal),
            (pub_ref, DATACITE.doi, doi_literal),
            (pub_ref, DCTERMS.created, created_literal),
            (pub_ref, DCTERMS.language, language_literal)
        ])

        for keyword in pub.keywords:
            self.add_keyword(keyword, pub_ref, pub.publication_id, pub.language)

        for attribute in pub.additional_attributes:
            self.add_attribute(attribute, pub_ref, pub.publication_id)

    def add_keyword(self, keyword: Keyword, publication_reference: URIRef, publication_id: str,
                    publication_language: str) -> None:
        default_lang_values = [x for x in keyword.values if x.language == publication_language]
        # Check if keyword is provided in the language of the publication, otherwise just take any language
        #  TODO: Assess whether this should result in an exception instead
        if default_lang_values:
            localized_default_value = default_lang_values.pop()
        else:
            localized_default_value = keyword.values.pop()

        # TODO: Get keywordClass reference by querying the kg and checking if the keyword is already in the kg
        #  otherwise adding a new keyword class
        kw_class_ref = URIRef(KEYWORD_PREFIX + getId(localized_default_value.value))
        self.add_if_new([(kw_class_ref, RDFS.subClassOf, SGC.Keyword)])

        for kw_localized_value in keyword.values:
            kw_value_literal = Literal(kw_localized_value.value, lang=kw_localized_value.language)
            self.add_if_new([(kw_class_ref, RDF.value, kw_value_literal)])

        kw_instance_ref = URIRef(
            PUBLICATION_PREFIX + publication_id + "/keyword/" + getId(localized_default_value.value))
        kw_verification_status_literal = Literal(keyword.verification_status, datatype=XSD.integer)

        self.add_if_new([
            (kw_instance_ref, RDF.type, kw_class_ref),
            (kw_instance_ref, SGP.status, kw_verification_status_literal),
            (publication_reference, SGP.keyword, kw_instance_ref)
        ])

    def add_attribute(self, attribute: AdditionalAttribute, publication_reference: URIRef, publication_id: str) -> None:
        attr_flavor_ref = URIRef(ATTRIBUTE_PREFIX + getId(attribute.name))
        name_literal = Literal(attribute.name, datatype=XSD.string)

        attr_ref = URIRef(ATTRIBUTE_PREFIX + getId(attribute.name) + "/" + getId(attribute.value))
        value_literal = Literal(attribute.value, datatype=XSD.string)

        attr_instance_ref = URIRef(SG_PREFIX + "publication/" + publication_id + "/attribute/" + getId(attribute.name))
        verification_status_literal = Literal(attribute.verification_status, datatype=XSD.integer)

        self.add_if_new([
            (attr_flavor_ref, RDF.type, SGC.Attribute),
            (attr_flavor_ref, SGP.name, name_literal),

            (attr_ref, RDFS.subClassOf, attr_flavor_ref),
            (attr_ref, RDF.value, value_literal),

            (attr_instance_ref, RDFS.subClassOf, attr_ref),
            (attr_instance_ref, SGP.status, verification_status_literal),

            (publication_reference, SGP.attribute, attr_instance_ref)
        ])

    def add_if_new(self, triples: list[tuple[Node, Node, Node]]) -> None:
        for triple in triples:
            if triple not in self.graph:
                self.graph.add(triple)

    # TODO: Add language filter to queries
    def get_completed_keywords(self, start_keys: str, filter_attributes: list[AdditionalAttribute] = None,
                               filter_year_range: tuple[int, int] = None, limit: int = None) -> list[dict]:
        keyword_query = queries.get_keyword_begins_with_query(begins_with=start_keys, attributes=filter_attributes,
                                                              years_span=filter_year_range, limit=limit)

        values = []
        query_results = self.graph.query(keyword_query)

        for result in query_results.bindings:
            keyword_value = result[Variable('keyword_value')]
            values.append({
                "value": keyword_value.value,
                "language": keyword_value.language
            })

        return values

    def get_keyword_cross_reference(self, keywords: list[dict], filter_attributes: list[AdditionalAttribute] = None,
                                    filter_year_range: tuple[int, int] = None,
                                    limit: int = None) -> list[dict]:
        cross_reference_query = queries.get_keyword_cross_reference_query(keywords=keywords, limit=limit,
                                                                          attributes=filter_attributes,
                                                                          years_span=filter_year_range)

        values = []
        query_results = self.graph.query(cross_reference_query)

        for result in query_results:
            keyword_value = result[Variable('cross_value')]
            values.append({
                "value": keyword_value.value,
                "language": keyword_value.language
            })

        return values

    def get_results(self, keywords: list[dict], filter_attributes: list[AdditionalAttribute] = None,
                    filter_year_range: tuple[int, int] = None,
                    limit: int = None) -> list[dict]:
        publication_query = queries.get_publications_result(keywords=keywords, limit=limit,
                                                            attributes=filter_attributes, years_span=filter_year_range)
        query_results = self.graph.query(publication_query)

        publications = []
        for result in query_results:
            pub_ref_uri = result[Variable('pub')].toPython()
            keywords = []
            keyword_query = queries.get_keywords_query(pub_ref_uri)
            keyword_result = self.graph.query(keyword_query)

            for keyword in keyword_result:
                keywords.append({
                    'verification_status': keyword[Variable('verification_status')].value,
                    'values': [{
                        'value': keyword[Variable('keyword_value')].value,
                        'language': keyword[Variable('keyword_value')].language
                    }]
                })

            publications.append({
                'publication_id': pub_ref_uri.split("/")[-1],
                'title': result[Variable('title')].value,
                'issued': result[Variable('issued')].value,
                'author': result[Variable('author')].value,
                'doi': result[Variable('doi')].value,
                'language': result[Variable('language')].value,
                'keywords': keywords
            })

        return publications


BASE_CONNECTOR = RDFConnector("http://localhost:3030/ds")
