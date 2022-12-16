from .common import SG_PREFIXES


def get_document_name_list_query(keys: str = '*', limit: int = 10, page: int = 1)-> str:
    return f"""
{SG_PREFIXES}

SELECT ?pub ?title
WHERE {{
    ?pub rdf:type foaf:Document .
    ?pub dc:title ?title .
    FILTER regex(?keyword_value, "^{keys}", "i") .
}}

LIMIT {limit}
OFFSET {(page - 1) * limit}
"""

def get_document(publication_uri: str)-> str:
    return f"""
{SG_PREFIXES}

SELECT ?title ?issued ?doi ?language (concat('[',GROUP_CONCAT(?author;separator=","),']') as ?authors)
(CONCAT('[',GROUP_CONCAT(DISTINCT ?kw_c;separator=","),']') as ?keywords)
(CONCAT('[',GROUP_CONCAT(DISTINCT ?att;separator=","),']') as ?attributes)
WHERE {{
    <{publication_uri}> dc:title ?title;
        dc:issued ?issued ;
        dc:creator ?author ;
        datacite:doi ?doi ;
        dc:language ?language ;
        sgp:keyword ?kwi ;
        sgp:attribute ?atri .
        ?atri sgp:status ?atri_s;
        rdfs:subClassOf ?atr .
    ?atr rdf:value ?atr_v ;
        rdfs:subClassOf ?atrf .
    ?atrf sgp:name ?atr_n .
    BIND(CONCAT('{"name":"',?atr_n,'","value":"',?atr_v,'","status":',STR(?atri_s),'}') as ?att) .
    
    ?kwi rdf:type ?kw ;
        sgp:status ?kwi_s .
    ?kw rdf:value ?kw_val 
    FILTER (lang(?kw_val) = ?language)
    BIND(CONCAT('{"value":"',?kw_val,'","status":',STR(?kwi_s),'}') as ?kw_c) .
}}
GROUP BY ?title ?issued ?doi ?language
"""
