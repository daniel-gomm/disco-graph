from ..model.model import AdditionalAttribute

default_limit = 100

from .common import PREFIXES, SG_PREFIXES, get_attributes_filter, get_release_year_filter, get_keyword_list_string


def get_keyword_cross_reference_query(keywords: list[dict], limit: int = default_limit,
                                      attributes: list[AdditionalAttribute] = None,
                                      years_span: tuple[int, int] = None) -> str:
    keyword_list_string = get_keyword_list_string(keywords)
    return f"""
{PREFIXES}

SELECT ?cross_keyword ?cross_value (COUNT(?kwic) AS ?occurrences)
WHERE {{
    ?pub rdf:type foaf:Document .
    ?pub dgp:keyword ?kwi .
    ?kwi rdf:type ?kw .
    ?kw rdf:value ?val 
    FILTER(?val IN {keyword_list_string}) .
    ?pub dgp:keyword ?kwic .
    ?kwic rdf:type ?cross_keyword .
    ?cross_keyword rdf:value ?cross_value 
    FILTER(?cross_value NOT IN {keyword_list_string}) .
    {get_attributes_filter(attributes)}
    {get_release_year_filter(years_span)}
}}
GROUP BY ?cross_keyword ?cross_value

ORDER BY DESC(?occurrences)

LIMIT {limit}
"""


def get_publications_result(keywords: list[dict], limit: int = default_limit,
                            attributes: list[AdditionalAttribute] = None,
                            years_span: tuple[int, int] = None, page: int = 1) -> str:
    return f"""
{PREFIXES}

SELECT ?pub ?title ?issued ?doi ?language (concat('["',GROUP_CONCAT(?author;separator='","'),'"]') as ?authors) 
(COUNT(?kwi) AS ?occurrences)
WHERE {{
    ?pub rdf:type foaf:Document .
    ?pub dgp:keyword ?kwi .
    ?kwi rdf:type ?kw .
    ?kw rdf:value ?val 
    FILTER(?val in {get_keyword_list_string(keywords)}) .
    ?pub dc:title ?title ;
        dc:issued ?issued ;
        dc:creator ?author ;
        datacite:doi ?doi ;
        dc:language ?language .
    {get_attributes_filter(attributes)}
    {get_release_year_filter(years_span)}
}}
GROUP BY ?pub ?title ?issued ?doi ?language

ORDER BY DESC(?occurrences)

LIMIT {limit}
OFFSET {(page - 1 ) * limit}
"""


def get_attributes_names_query() -> str:
    return f"""
{SG_PREFIXES}

SELECT ?attr_name
WHERE {{
    ?attr_flavour rdf:type dgc:Attribute .
    ?attr_flavour dgp:name ?attr_name .
}}
"""

def get_attribute_values_query(attribute_name:str) -> str:
    return f"""
{SG_PREFIXES}

SELECT ?attr_value
WHERE {{
    ?attr_flavour rdf:type dgc:Attribute .
    ?attr_flavour dgp:name "{attribute_name}" .
    ?attr rdfs:subClassOf ?attr_flavour .
    ?attr rdf:value ?attr_value .
}}
"""
