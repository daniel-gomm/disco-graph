from .common import SG_PREFIXES, PREFIXES


def get_document_name_list_query(keys: str = '*', limit: int = 10, page: int = 1) -> str:
    return f"""
    {PREFIXES}

SELECT ?pub ?title
WHERE {{
    ?pub rdf:type foaf:Document .
    ?pub dc:title ?title .
    FILTER regex(?title, "^{keys}", "i") .
}}

LIMIT {limit}
OFFSET {((page - 1) * limit)}
"""


def get_document(publication_uri: str) -> str:
    return f"""
{PREFIXES}

SELECT ?title ?issued ?doi ?language ?abstract ?website (concat('["',GROUP_CONCAT(?author;separator='","'),'"]') as ?authors)
(CONCAT('["',GROUP_CONCAT(DISTINCT ?att;separator='","'),'"]') as ?attributes)
WHERE {{
    <{publication_uri}> dc:title ?title;
        dc:issued ?issued ;
        dc:creator ?author ;
        dc:abstract ?abstract ;
        sgp:website ?website;
        datacite:doi ?doi ;
        dc:language ?language .
        OPTIONAL {{
            <{publication_uri}> sgp:attribute ?atri .
            ?atri sgp:status ?atri_s;
            rdfs:subClassOf ?atr .
            ?atr rdf:value ?atr_v ;
                rdfs:subClassOf ?atrf .
            ?atrf sgp:name ?atr_n .
            BIND(CONCAT('{{"name":"',?atr_n,'","value":"',?atr_v,'","status":',STR(?atri_s),'}}') as ?att) .
        }}
}}
GROUP BY ?title ?issued ?doi ?language ?abstract ?website
"""
