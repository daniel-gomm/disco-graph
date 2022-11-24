from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from auth import login_required
from model.model import Publication
from rdf_interface import RDFConnector

bp = Blueprint('publication', __name__)

rdf_connector = RDFConnector("http://localhost:3030/ds")

@bp.get("/publication/<string:identifier>")
def get_publication(identifier):
    # TODO: implement
    pass

@bp.post("/publication/<string:identifier>")
@login_required
def add_publication(identifier):
    req_json = request.get_json()
    pub = Publication(req_json)
    rdf_connector.add_publication(pub)
    return f"Successfully added new publication {pub.pub_id}", 200

@bp.put("/publication/<string:identifier>")
@login_required
def update_publication(identifier):
    # TODO: Implement
    pass

@bp.delete("/publication/<string:identifier>")
@login_required
def delete_publication(identifier):
    # TODO: Implement
    pass


# Keyword
@bp.get("/publication/<string:pub_identifier>/keyword/<string:keyword_identifier>")
def get_keyword(pub_identifier, keyword_identifier):
    # TODO: implement
    pass

@bp.post("/publication/<string:pub_identifier>/keyword/<string:keyword_identifier>")
@login_required
def add_keyword(pub_identifier, keyword_identifier):
    # TODO: implement
    pass

@bp.put("/publication/<string:pub_identifier>/keyword/<string:keyword_identifier>")
@login_required
def update_keyword(pub_identifier, keyword_identifier):
    # TODO: Implement
    pass

@bp.delete("/publication/<string:pub_identifier>/keyword/<string:keyword_identifier>")
@login_required
def delete_keyword(pub_identifier, keyword_identifier):
    # TODO: Implement
    pass