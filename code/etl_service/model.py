from flask import request
from extraction import parse_publication_pdf

class publication:
    pub_id: str
    author: str
    title: str
    doi: str
    issued: int
    keywords: list(str)
    full_text: str
    pdf: any

    def __init__(self, request:request=None) -> None:
        if not request:
            raise Exception("Unable to instantiate new publication. No request provided!")
        self.pub_id = request.form["pub_id"]
        self.author = request.form["author"]
        self.title = request.form["title"]
        self.doi = request.form["doi"]
        self.issued = request.form["issued"]
        self.keywords = []
        if "keywords" in request.form:
            for keyword in request.form["keywords"]:
                self.keywords.append(keyword)
        self.pdf = request.files["publication_pdf"]
        self.full_text = parse_publication_pdf(self.pdf)
