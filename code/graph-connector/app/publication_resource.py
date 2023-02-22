from flask import (
    Blueprint, request, jsonify
)

from .auth import login_required, admin_login_required
from .model.model import Publication, Keyword
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
@admin_login_required
def add_publication(identifier):
    req_json = request.get_json()
    pub = Publication(req_json)
    rdf_connector.add_publication(pub)
    return f"Successfully added new publication {pub.publication_id}", 200


@bp.put("/<string:identifier>")
@admin_login_required
def update_publication(identifier):
    # TODO: Implement
    pass


@bp.put("/<string:pub_id>/title")
@admin_login_required
def update_publication_title(pub_id):
    req_json = request.get_json()
    new_title = req_json['title']
    try:
        rdf_connector.update_title(pub_id, new_title)
    except:
        return "Failed to update title", 500
    return f"Successfully updated title of {pub_id}", 200


@bp.put("/<string:pub_id>/doi")
@admin_login_required
def update_publication_doi(pub_id):
    req_json = request.get_json()
    new_doi = req_json['doi']
    try:
        rdf_connector.update_doi(pub_id, new_doi)
    except:
        return "Failed to update doi", 500
    return f"Successfully updated doi of {pub_id}", 200


@bp.put("/<string:pub_id>/issued")
@admin_login_required
def update_publication_issued(pub_id):
    req_json = request.get_json()
    new_issued = req_json['issued']
    try:
        rdf_connector.update_issued(pub_id, new_issued)
    except:
        return "Failed to update publication year", 500
    return f"Successfully updated publication year of {pub_id}", 200


@bp.put("/<string:pub_id>/language")
@admin_login_required
def update_publication_language(pub_id):
    req_json = request.get_json()
    new_language = req_json['language']
    try:
        rdf_connector.update_language(pub_id, new_language)
    except:
        return "Failed to update language", 500
    return f"Successfully updated language of {pub_id}", 200


@bp.post("/<string:pub_id>/author")
@admin_login_required
def add_publication_author(pub_id):
    req_json = request.get_json()
    author_name = req_json['author']
    try:
        rdf_connector.add_author(pub_id, author_name)
    except:
        return "Failed to add author", 500
    return f"Successfully added author to {pub_id}", 200


@bp.post("/<string:pub_id>/keyword")
@login_required
def add_publication_keyword(pub_id):
    req_json = request.get_json()
    try:
        rdf_connector.add_keyword_to_publication(pub_id, req_json)
    except:
        return "Failed to add keyword", 500


@bp.post("/<string:pub_id>/attribute")
@admin_login_required
def add_publication_attribute(pub_id):
    # TODO: Implement
    pass


@bp.delete("/<string:identifier>")
@admin_login_required
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


@bp.put("/<string:pub_identifier>/keyword/<string:keyword_identifier>/verification_status")
@login_required
def update_keyword_verification(pub_identifier, keyword_identifier):
    req_json = request.get_json()
    new_status = req_json['verification_status']
    try:
        rdf_connector.update_keyword_confirmation(pub_identifier, keyword_identifier, int(new_status))
    except:
        return "Failed to update confirmation status", 404
    return f"Successfully updated confirmation status of {keyword_identifier}", 200


@bp.delete("/<string:pub_identifier>/keyword/<string:keyword_identifier>")
@admin_login_required
def delete_keyword(pub_identifier, keyword_identifier):
    # TODO: Implement
    pass


@bp.put("/<string:pub_identifier>/attribute/<string:attribute_flavor>/verification_status")
@login_required
def update_attribute_verification(pub_identifier, attribute_flavor):
    req_json = request.get_json()
    new_status = req_json['verification_status']
    try:
        rdf_connector.update_attribute_confirmation(pub_identifier, attribute_flavor, int(new_status))
    except:
        return "Failed to update confirmation status", 404
    return f"Successfully updated confirmation status of {attribute_flavor}", 200
