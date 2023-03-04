from . import configuration

from .model.model import Publication, Keyword, AdditionalAttribute
from .rdf import queries, document_queries, keyword_queries

from rdflib.term import Node, Variable
from rdflib import Graph, Literal, URIRef, Namespace
from rdflib.plugins.stores import sparqlstore
from rdflib.graph import DATASET_DEFAULT_GRAPH_ID as default_identifier
from rdflib.namespace import RDF, DCTERMS, FOAF, XSD, RDFS

import ast

DG_PREFIX = "https://disco-graph.online/0.1/"
PUBLICATION_PREFIX = DG_PREFIX + "publication/"
KEYWORD_PREFIX = DG_PREFIX + "keyword/"
ATTRIBUTE_PREFIX = DG_PREFIX + "attribute/"

DATACITE = Namespace("https://purl.org/spar/datacite/")
PRISM = Namespace("http://prismstandard.org/namespaces/basic/2.0/")
DGC = Namespace(DG_PREFIX + "classes/")
DGP = Namespace(DG_PREFIX + "properties/")


def get_id(value: str) -> str:
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
        abstract_literal = Literal(pub.abstract, datatype=XSD.string)
        website_literal = Literal(pub.website, datatype=XSD.string)
        issued_literal = Literal(pub.issued, datatype=XSD.year)
        doi_literal = Literal(pub.doi, datatype=XSD.string)
        created_literal = Literal(pub.created, datatype=XSD.dateTimeStamp)
        language_literal = Literal(pub.language, datatype=XSD.language)

        self.add_if_new([
            (pub_ref, RDF.type, FOAF.Document),
            (pub_ref, DCTERMS.title, title_literal),
            (pub_ref, DCTERMS.abstract, abstract_literal),
            (pub_ref, DGP.website, website_literal),
            (pub_ref, DCTERMS.issued, issued_literal),
            (pub_ref, DATACITE.doi, doi_literal),
            (pub_ref, DCTERMS.created, created_literal),
            (pub_ref, DCTERMS.language, language_literal)
        ])

        for author in pub.authors:
            self.add_if_new([
                (pub_ref, DCTERMS.creator, Literal(author, datatype=XSD.string))
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
        kw_class_ref = URIRef(KEYWORD_PREFIX + get_id(localized_default_value.value))
        self.add_if_new([(kw_class_ref, RDFS.subClassOf, DGC.Keyword)])

        for kw_localized_value in keyword.values:
            kw_value_literal = Literal(kw_localized_value.value, lang=kw_localized_value.language)
            self.add_if_new([(kw_class_ref, RDF.value, kw_value_literal)])

        kw_instance_ref = URIRef(
            PUBLICATION_PREFIX + publication_id + "/keyword/" + get_id(localized_default_value.value))
        kw_verification_status_literal = Literal(keyword.verification_status, datatype=XSD.integer)

        self.add_if_new([
            (kw_instance_ref, RDF.type, kw_class_ref),
            (kw_instance_ref, DGP.status, kw_verification_status_literal),
            (publication_reference, DGP.keyword, kw_instance_ref)
        ])

    def add_attribute(self, attribute: AdditionalAttribute, publication_reference: URIRef, publication_id: str) -> None:
        attr_flavor_ref = URIRef(ATTRIBUTE_PREFIX + get_id(attribute.name))
        name_literal = Literal(attribute.name, datatype=XSD.string)

        attr_ref = URIRef(ATTRIBUTE_PREFIX + get_id(attribute.name) + "/" + get_id(attribute.value))
        value_literal = Literal(attribute.value, datatype=XSD.string)

        attr_instance_ref = URIRef(DG_PREFIX + "publication/" + publication_id + "/attribute/" + get_id(attribute.name))
        verification_status_literal = Literal(attribute.verification_status, datatype=XSD.integer)

        self.add_if_new([
            (attr_flavor_ref, RDF.type, DGC.Attribute),
            (attr_flavor_ref, DGP.name, name_literal),

            (attr_ref, RDFS.subClassOf, attr_flavor_ref),
            (attr_ref, RDF.value, value_literal),

            (attr_instance_ref, RDFS.subClassOf, attr_ref),
            (attr_instance_ref, DGP.status, verification_status_literal),

            (publication_reference, DGP.attribute, attr_instance_ref)
        ])

    def add_if_new(self, triples: list[tuple[Node, Node, Node]]) -> None:
        for triple in triples:
            if triple not in self.graph:
                self.graph.add(triple)

    def update_title(self, pub_id: str, new_title: str) -> None:
        self._update_publication_attribute(pub_id, new_title, DCTERMS.title, datatype=XSD.string)

    def update_doi(self, pub_id: str, new_doi: str) -> None:
        self._update_publication_attribute(pub_id, new_doi, DATACITE.doi, XSD.string)

    def update_language(self, pub_id: str, new_language: str) -> None:
        self._update_publication_attribute(pub_id, new_language, DCTERMS.language, XSD.language)

    def update_issued(self, pub_id: str, new_issued: str) -> None:
        self._update_publication_attribute(pub_id, new_issued, DCTERMS.issued, XSD.year)

    def update_keyword_confirmation(self, pub_id: str, keyword_id: str, updated_status: int) -> None:
        kwi_ref = URIRef(PUBLICATION_PREFIX + pub_id + "/keyword/" + get_id(keyword_id))
        updated_status_literal = Literal(int(updated_status), datatype=XSD.integer)
        self._update_triple(kwi_ref, DGP.status, updated_status_literal)

    def update_attribute_confirmation(self, pub_id: str, attribute_flavor: str,
                                      updated_status: int) -> None:
        attr_instance_ref = URIRef(DG_PREFIX + "publication/" + pub_id + "/attribute/" + get_id(attribute_flavor))
        updated_status_literal = Literal(int(updated_status), datatype=XSD.integer)
        self._update_triple(attr_instance_ref, DGP.status, updated_status_literal)

    def add_author(self, pub_id: str, author_name: str):
        pub_ref = URIRef(PUBLICATION_PREFIX + pub_id)
        author_name_literal = Literal(author_name, datatype=XSD.string)
        self.add_if_new([
            (pub_ref, DCTERMS.creator, author_name_literal)
        ])

    def add_keyword_to_publication(self, pub_id: str, keyword: dict) -> None:
        pub_ref = URIRef(PUBLICATION_PREFIX + pub_id)
        publication = self.get_publication(pub_id)
        self.add_keyword(Keyword(keyword), pub_ref, pub_id, publication['language'])

    def delete_author(self, pub_id: str, author_name: str):
        pub_ref = URIRef(PUBLICATION_PREFIX + pub_id)
        author_name_literal = Literal(author_name, datatype=XSD.string)
        self._delete_if_exists([
            (pub_ref, DCTERMS.creator, author_name_literal)
        ])

    def _delete_if_exists(self, triples: list[tuple[Node, Node, Node]]) -> None:
        for triple in triples:
            if triple in self.graph:
                self.graph.remove(triple)

    def _update_publication_attribute(self, pub_id: str, new_value: any, predicate: Node, datatype: str) -> None:
        pub_ref = URIRef(PUBLICATION_PREFIX + pub_id)
        new_value_literal = Literal(new_value, datatype=datatype)
        self._update_triple(pub_ref, predicate, new_value_literal)

    def _update_triple(self, subject: Node, predicate: Node, new_object: Node):
        prev_value = self.graph.value(subject, predicate)
        if prev_value:
            self._delete_if_exists([
                (subject, predicate, prev_value)
            ])
        self.add_if_new([
            (subject, predicate, new_object)
        ])

    # TODO: Add language filter to queries
    def get_completed_keywords(self, start_keys: str, filter_attributes: list[tuple[str, str]] = None,
                               filter_year_range: tuple[int, int] = None, limit: int = None) -> list[dict]:
        keyword_query = keyword_queries.get_keyword_begins_with_query(begins_with=start_keys,
                                                                      attributes=filter_attributes,
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

    def get_keyword_cross_reference(self, keywords: list[dict], filter_attributes: list[tuple[str, str]] = None,
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

    def get_results(self, keywords: list[dict], filter_attributes: list[tuple[str, str]] = None,
                    filter_year_range: tuple[int, int] = None,
                    limit: int = None) -> list[dict]:
        publication_query = queries.get_publications_result(keywords=keywords, limit=limit,
                                                            attributes=filter_attributes, years_span=filter_year_range)
        query_results = self.graph.query(publication_query)

        publications = []
        for result in query_results:
            pub_ref_uri = result[Variable('pub')].toPython()
            keywords = self.get_keywords(pub_ref_uri)
            publications.append({
                'publication_id': pub_ref_uri.split("/")[-1],
                'title': result[Variable('title')].value,
                'issued': result[Variable('issued')],
                'authors': ast.literal_eval(result[Variable('authors')].value),
                'doi': result[Variable('doi')].value,
                'language': result[Variable('language')].value,
                'keywords': list(keywords.values())
            })

        return publications

    def get_attributes(self) -> list[dict]:
        attribute_name_query = queries.get_attributes_names_query()

        query_results = self.graph.query(attribute_name_query)

        results = []

        for result in query_results:
            name = result[Variable('attr_name')].value
            values = []
            attribute_values_query = queries.get_attribute_values_query(name)

            attribute_values_query_results = self.graph.query(attribute_values_query)
            for attribute_value in attribute_values_query_results:
                values.append(attribute_value[Variable('attr_value')].value)

            results.append({
                'attribute_name': name,
                'values': values
            })

        return results

    def get_publication_names(self, keys: str, limit: int, page: int) -> list[dict]:
        publication_names_query = document_queries.get_document_name_list_query(keys, limit, page)

        query_results = self.graph.query(publication_names_query)

        results = []

        for result in query_results:
            results.append({
                'title': result[Variable('title')],
                'publication_id': result[Variable('pub')].toPython().split("/")[-1]
            })

        return results

    def get_publication(self, publication_id: str) -> dict:
        pub_ref_uri = PUBLICATION_PREFIX + publication_id
        doc_query = document_queries.get_document(pub_ref_uri)

        query_result = self.graph.query(doc_query)

        if len(query_result) != 1:
            raise AttributeError(f'No publication with id {publication_id} exists.')

        pub_result = query_result.bindings[0]
        keywords = self.get_keywords(pub_ref_uri)
        publication = {
            'publication_id': publication_id,
            'title': pub_result[Variable('title')],
            'language': pub_result[Variable('language')],
            'issued': pub_result[Variable('issued')],
            'doi': pub_result[Variable('doi')],
            'abstract': pub_result[Variable('abstract')],
            'website': pub_result[Variable('website')],
            'authors': ast.literal_eval(pub_result[Variable('authors')]),
            'keywords': list(keywords.values())
        }
        try:
            attributes = pub_result[Variable('attributes')]
            publication['attributes'] = attributes
        finally:
            return publication

    def get_keywords(self, pub_ref_uri: str) -> dict:
        keyword_query = keyword_queries.get_keywords_query(pub_ref_uri)
        keyword_result = self.graph.query(keyword_query)

        keywords = {}

        for keyword in keyword_result:
            keyword_uri = keyword[Variable('kw')].toPython()
            if keyword_uri not in keywords:
                keywords[keyword_uri] = {
                    'verification_status': keyword[Variable('verification_status')].value,
                    'values': []
                }

            keywords[keyword_uri]['values'].append({
                'value': keyword[Variable('keyword_value')].value,
                'language': keyword[Variable('keyword_value')].language
            })
        return keywords

    def get_keyword_languages(self) -> list[str]:
        languages_query = keyword_queries.get_keyword_languages_query()
        languages_result = self.graph.query(languages_query)
        return [value[Variable('lang')].value for value in languages_result]


BASE_CONNECTOR = RDFConnector(configuration.KG_HOSTNAME)
