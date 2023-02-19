from .common import SG_PREFIXES, PREFIXES, get_attributes_filter, get_release_year_filter

from ..model.model import AdditionalAttribute

default_limit = 100


def get_keyword_begins_with_query(begins_with: str, limit: int = default_limit,
                                  attributes: list[AdditionalAttribute] = None,
                                  years_span: tuple[int, int] = None) -> str:
    if limit is None:
        limit = default_limit
    return f"""
{PREFIXES}

SELECT DISTINCT ?keyword_value
WHERE {{
    ?pub rdf:type foaf:Document .
    ?pub dgp:keyword ?kwi .
    ?kwi rdf:type ?keyword .
    ?keyword rdf:value ?keyword_value
    FILTER regex(?keyword_value, "^{begins_with}", "i") .
    {get_attributes_filter(attributes)}
    {get_release_year_filter(years_span)}
}}
LIMIT {limit}
"""


def get_keywords_query(publication_uri: str, limit: int = default_limit, page: int = 1) -> str:
    return f"""
{SG_PREFIXES}

SELECT ?keyword_value ?verification_status ?kw
WHERE {{
    <{publication_uri}> dgp:keyword ?kwi .
    ?kwi rdf:type ?kw ;
        dgp:status ?verification_status .
    ?kw rdf:value ?keyword_value .
}}

LIMIT {limit}
OFFSET {(page - 1) * limit}
"""
