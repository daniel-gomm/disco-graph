from ..model.model import AdditionalAttribute

default_limit = 100

def _get_prefixes() -> str:
    return """
    PREFIX sgc: <https://sci-graph.kit.edu/0.1/classes/>
    PREFIX sgp: <https://sci-graph.kit.edu/0.1/properties/>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX foaf: <http://xmlns.com/foaf/0.1/>
    PREFIX dc: <http://purl.org/dc/terms/>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    """


def get_attribute_filter(attribute: AdditionalAttribute) -> str:
    name = attribute.name
    return f"""
    ?pub sgp:attribute ?{name}_attribute_instance .
    ?{name}_attribute_instance rdf:type ?{name}_attribute .
    ?{name}_attribute rdfs:subClassOf ?{name}_attribute_flavor .
    ?{name}_attribute_flavor sgp:name "{attribute.name}" .
    ?{name}_attribute rdf:value "{attribute.value}" .
    
    """


def get_attributes_filter(attributes: list[AdditionalAttribute] = None) -> str:
    # If not attributes are provided
    if not attributes:
        return ""
    attributes_filter = ""
    for attribute in attributes:
        attributes_filter += get_attribute_filter(attribute)
    return attributes_filter


def get_release_year_filter(span: tuple[int, int] = None) -> str:
    if span is None:
        return ""
    return f"""
    ?pub dc:issued ?year .
    FILTER ({span[0] - 1} < xsd:integer(?year) && xsd:integer(?year) < {span[1] + 1})
    """


def get_keyword_cross_reference_query(keywords: list[str], language: str, limit: int = 10,
                                      attributes: list[AdditionalAttribute] = None,
                                      years_span: tuple[int, int] = None) -> str:
    keyword_list_string = "("
    for keyword in keywords:
        keyword_list_string += f'"{keyword}"@{language},'
    keyword_list_string = keyword_list_string[:-1] + ")"

    return f"""
    {_get_prefixes()}

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
{_get_prefixes()}

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
