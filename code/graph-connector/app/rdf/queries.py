from ..model.model import AdditionalAttribute

default_limit = 100

SG_PREFIXES = """
PREFIX sgc: <https://sci-graph.kit.edu/0.1/classes/>
PREFIX sgp: <https://sci-graph.kit.edu/0.1/properties/>
"""

PREFIXES = SG_PREFIXES + """
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX dc: <http://purl.org/dc/terms/>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX datacite: <https://purl.org/spar/datacite/>
"""


def get_attribute_filter(name: str, value: str) -> str:
    return f"""
?pub sgp:attribute ?{name}_attribute_instance .
?{name}_attribute_instance rdfs:subClassOf ?{name}_attribute .
?{name}_attribute rdfs:subClassOf ?{name}_attribute_flavor .
?{name}_attribute_flavor sgp:name "{name}" .
?{name}_attribute rdf:value "{value}" .
"""


def get_attributes_filter(attributes: list[tuple[str, str]] = None) -> str:
    # If not attributes are provided
    if not attributes:
        return ""
    attributes_filter = ""
    for attribute in attributes:
        attributes_filter += get_attribute_filter(attribute[0], attribute[1])
    return attributes_filter


def get_release_year_filter(span: tuple[int, int] = None) -> str:
    if span is None:
        return ""
    return f"""
?pub dc:issued ?year .
FILTER ({span[0] - 1} < xsd:integer(?year) && xsd:integer(?year) < {span[1] + 1})
"""


def get_keyword_list_string(keywords: list[dict]) -> str:
    keyword_list_string = "("
    for keyword in keywords:
        keyword_list_string += f'"{keyword["value"]}"@{keyword["language"]},'
    return keyword_list_string[:-1] + ")"


def get_keyword_cross_reference_query(keywords: list[dict], limit: int = default_limit,
                                      attributes: list[AdditionalAttribute] = None,
                                      years_span: tuple[int, int] = None) -> str:
    keyword_list_string = get_keyword_list_string(keywords)
    return f"""
{PREFIXES}

SELECT ?cross_keyword ?cross_value (COUNT(?kwic) AS ?occurrences)
WHERE {{
    ?pub rdf:type foaf:Document .
    ?pub sgp:keyword ?kwi .
    ?kwi rdf:type ?kw .
    ?kw rdf:value ?val 
    FILTER(?val IN {keyword_list_string}) .
    ?pub sgp:keyword ?kwic .
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
    ?pub sgp:keyword ?kwi .
    ?kwi rdf:type ?keyword .
    ?keyword rdf:value ?keyword_value
    FILTER regex(?keyword_value, "^{begins_with}", "i") .
    {get_attributes_filter(attributes)}
    {get_release_year_filter(years_span)}
}}
LIMIT {limit}
"""


def get_publications_result(keywords: list[dict], limit: int = default_limit,
                            attributes: list[AdditionalAttribute] = None,
                            years_span: tuple[int, int] = None) -> str:
    return f"""
{PREFIXES}

SELECT ?pub ?title ?issued ?author ?doi ?language (COUNT(?kwi) AS ?occurrences)
WHERE {{
    ?pub rdf:type foaf:Document .
    ?pub sgp:keyword ?kwi .
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
GROUP BY ?pub ?title ?issued ?author ?doi ?language

ORDER BY DESC(?occurrences)

LIMIT {limit}
"""


# TODO: add support for language query in order to not get multiple values for the same keyword
def get_keywords_query(publication_uri: str, limit: int = default_limit) -> str:
    return f"""
{SG_PREFIXES}

SELECT ?keyword_value ?verification_status
WHERE {{
    <{publication_uri}> sgp:keyword ?kwi .
    ?kwi rdf:type ?kw .
    ?kwi sgp:status ?verification_status .
    ?kw rdf:value ?keyword_value .
}}

LIMIT {limit}
"""


def get_attributes_names_query() -> str:
    return f"""
{SG_PREFIXES}

SELECT ?attr_name
WHERE {{
    ?attr_flavour rdf:type sgc:Attribute .
    ?attr_flavour sgp:name ?attr_name .
}}
"""

def get_attribute_values_query(attribute_name:str) -> str:
    return f"""
{SG_PREFIXES}

SELECT ?attr_value
WHERE {{
    ?attr_flavour rdf:type sgc:Attribute .
    ?attr_flavour sgp:name "{attribute_name}" .
    ?attr rdfs:subClassOf ?attr_flavour .
    ?attr rdf:value ?attr_value .
}}
"""