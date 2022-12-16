from flask import (
    Blueprint, request, jsonify
)

from .auth import login_required
from .model.model import Publication
from .rdf_interface import BASE_CONNECTOR
from .request_utils import get_numeric_query_parameter

bp = Blueprint('publication', __name__, url_prefix='/publication')

rdf_connector = BASE_CONNECTOR


@bp.get('/list')
def get_publications():
    search_input = request.args.get('keys')
    if not search_input:
        search_input = '*'
    limit = get_numeric_query_parameter('limit', 10)
    page = get_numeric_query_parameter('page', 1)

    documents = rdf_connector.get_publication_names(search_input, limit, page)

    return documents, 200


@bp.get("/<string:identifier>")
def get_publication(identifier):
    # Return full publication with all info
    try:
        publication = rdf_connector.get_publication(identifier)
        return jsonify(publication), 200
    except AttributeError:
        return {}, 404


@bp.post("/<string:identifier>")
@login_required
def add_publication(identifier):
    req_json = request.get_json()
    pub = Publication(req_json)
    rdf_connector.add_publication(pub)
    return f"Successfully added new publication {pub.publication_id}", 200


@bp.put("/<string:identifier>")
@login_required
def update_publication(identifier):
    # TODO: Implement
    pass


@bp.delete("/<string:identifier>")
@login_required
def delete_publication(identifier):
    # TODO: Implement
    pass


# Keyword
@bp.get("/<string:pub_identifier>/keyword/<string:keyword_identifier>")
def get_keyword(pub_identifier, keyword_identifier):
    # TODO: implement
    pass


@bp.post("/<string:pub_identifier>/keyword/<string:keyword_identifier>")
@login_required
def add_keyword(pub_identifier, keyword_identifier):
    # TODO: implement
    pass


@bp.put("/<string:pub_identifier>/keyword/<string:keyword_identifier>")
@login_required
def update_keyword(pub_identifier, keyword_identifier):
    # TODO: Implement
    pass


@bp.delete("/<string:pub_identifier>/keyword/<string:keyword_identifier>")
@login_required
def delete_keyword(pub_identifier, keyword_identifier):
    # TODO: Implement
    pass
