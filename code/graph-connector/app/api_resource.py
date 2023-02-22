from flask import (
    Blueprint, request, session, jsonify
)

from .rdf_interface import BASE_CONNECTOR
from .request_utils import get_numeric_query_parameter

bp = Blueprint('api', __name__, url_prefix='/api/v1')

rdf_connector = BASE_CONNECTOR


@bp.get("/keyword/load")
def get_keywords_starting_with_keys():
    keys = request.args.get('keys')
    limit = get_numeric_query_parameter('limit')

    if not keys:
        return "Invalid query!", 400

    keywords = rdf_connector.get_completed_keywords(start_keys=keys,
                                                    filter_attributes=get_attribute_filters(session.get('attributes')),
                                                    filter_year_range=session.get('year_range'), limit=limit)
    return jsonify(keywords), 200


@bp.get("/keyword/cross-reference")
def get_keyword_cross_reference():
    keywords = request.args.get('keywords')
    try:
        keywords = parse_keyboard_query_list(keywords)
    except AttributeError:
        return "Invalid query!", 400

    limit = get_numeric_query_parameter('limit')

    cross_reference_keywords = rdf_connector.get_keyword_cross_reference(keywords=keywords,
                                                                         filter_attributes=get_attribute_filters(
                                                                             session.get('attributes')),
                                                                         filter_year_range=session.get('year_range'),
                                                                         limit=limit)
    return jsonify(cross_reference_keywords), 200


'''
Get publications as results.
'''


@bp.get("publication/results")
def get_results():
    keywords = request.args.get('keywords')
    try:
        keywords = parse_keyboard_query_list(keywords)
    except AttributeError:
        return "Invalid query!", 400

    limit = get_numeric_query_parameter('limit')

    results = rdf_connector.get_results(keywords=keywords, filter_attributes=get_attribute_filters(session
                                                                                                   .get('attributes')),
                                        filter_year_range=session.get('year_range'), limit=limit)

    return jsonify(results), 200


'''
Expects a requests with a JSON serialization of an attribute (verification_status is not required)
'''


@bp.route("/filter/attribute", methods=('POST', 'PUT', 'GET'))
def filter_attribute():
    if request.method in ['POST', 'PUT']:
        req_json = request.get_json()
        if not session.get('attributes'):
            session['attributes'] = {}
        session['attributes'][req_json['name']] = req_json['value']

    elif request.method == 'GET':
        attributes = rdf_connector.get_attributes()
        return jsonify(attributes), 200

    return {}, 200


@bp.route('/filter/attribute/<string:name>', methods=['DELETE'])
def delete_attribute_filter(name: str):
    dictionary: dict = session.get('attributes')
    dictionary.pop(name)
    session.pop('attributes', None)
    session['attributes'] = dictionary
    return {}, 200


'''
Expects a request containing a json object that looks like this:
{
'lower_limit': int,
'upper_limit': int
}
'''


@bp.route("/filter/year", methods=('POST', 'PUT', 'DELETE'))
def filter_year():
    if request.method in ['POST', 'PUT']:
        req_json = request.get_json()
        session['year_range'] = (req_json['lower_limit'], req_json['upper_limit'])

    elif request.method == 'DELETE':
        session.pop('year_range', None)

    return {}, 200


def get_attribute_filters(attributes: dict) -> list[tuple[str:str]] | None:
    if attributes:
        return [(k, v) for k, v in attributes.items()]
    return None


def parse_keyboard_query_list(list_query: str) -> list[dict]:
    if list_query:
        result = []
        for arg in list_query.split(','):
            keyword = arg.split("@")
            result.append({"value": keyword[0], "language": keyword[1]})
        return result
    raise AttributeError("Provided parameter is of None value.")
