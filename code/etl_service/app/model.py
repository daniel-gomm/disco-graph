from flask import request
from extraction import parse_publication_pdf


def get_field_or_exception(field_to_get: str, json: dict):
    if field_to_get not in json.keys():
        raise Exception(f"Field {field_to_get} not provided.")
    return json[field_to_get]


class Publication:
    pub_id: str
    author: str
    title: str
    doi: str
    issued: int
    keywords: list
    full_text: str

    def __init__(self, req_json: dict = None) -> None:
        if not req_json:
            raise Exception("Unable to instantiate new publication. No request body provided!")
        self.pub_id = get_field_or_exception("pub_id", req_json)
        self.author = get_field_or_exception("author", req_json)
        self.title = get_field_or_exception("title", req_json)
        self.doi = get_field_or_exception("doi", req_json)
        self.issued = get_field_or_exception("issued", req_json)
        self.keywords = get_field_or_exception("keywords", req_json)

    def extract_text(self, pdf):
        if not pdf:
            pdf = request.files["publication_pdf"]
        self.full_text = parse_publication_pdf(pdf)
