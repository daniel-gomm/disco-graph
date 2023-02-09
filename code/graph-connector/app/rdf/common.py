SG_PREFIXES = """
PREFIX sgc: <https://disco-graph.online/0.1/classes/>
PREFIX sgp: <https://disco-graph.online/0.1/properties/>
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