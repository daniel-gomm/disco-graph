from flask import (
    Blueprint, request, session, jsonify
)

from .auth import login_required
from .model.model import AdditionalAttribute
from .rdf_interface import BASE_CONNECTOR

bp = Blueprint('api', __name__, url_prefix='/api/v1')

rdf_connector = BASE_CONNECTOR


@bp.get("/keyword/load")
def get_keywords_starting_with_keys():
    keys = request.args.get('keys')
    limit = get_numeric_query_parameter('limit')

    if not keys:
        return "Invalid query!", 400

    keywords = rdf_connector.get_completed_keywords(start_keys=keys, filter_attributes=get_attribute_filters(),
                                                    filter_year_range=get_year_filter(), limit=limit)
    return jsonify(keywords), 200


@bp.get("/keyword/cross-reference")
def get_keyword_cross_reference():
    keywords = request.args.get('keywords')
    try:
        keywords = parse_keyboard_query_list(keywords)
    except AttributeError:
        return "Invalid query!", 400

    language = request.args.get('lang')
    if not language:
        language = "en"

    limit = get_numeric_query_parameter('limit')

    cross_reference_keywords = rdf_connector.get_keyword_cross_reference(keywords=keywords,
                                                                         filter_attributes=get_attribute_filters(),
                                                                         filter_year_range=get_year_filter(),
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

    results = rdf_connector.get_results(keywords=keywords, filter_attributes=get_attribute_filters(),
                                        filter_year_range=get_year_filter(), limit=limit)

    return jsonify(results), 200


'''
Expects a requests with a JSON serialization of an attribute (verification_status is not required)
'''


@bp.route("/filter/attribute", methods=('POST', 'PUT', 'DELETE'))
def filter_attribute():
    req_json = request.get_json()
    attribute = AdditionalAttribute(req_json)
    if request.method in ['POST', 'PUT']:
        if not session.get('attributes'):
            session['attributes'] = {}
        session.get('attributes')[attribute.name] = attribute

    if request.method == 'DELETE':
        del session.get('attributes')[attribute.name]


'''
Expects a request containing a json object that looks like this:
{
'lower_limit': int,
'upper_limit': int
}
'''


@bp.route("/filter/year", methods=('POST', 'PUT', 'DELETE'))
def filter_year():
    req_json = request.get_json()
    if request.method in ['POST', 'PUT']:
        session['year_range'] = (req_json['lower_limit'], req_json['upper_limit'])

    elif request.method == 'DELETE':
        session.pop('year_range', None)


def get_attribute_filters() -> list[AdditionalAttribute] | None:
    if session.get('attribute'):
        return list(session.get('attribute').values())
    return None


def get_year_filter() -> tuple[int, int]:
    return session.get('year_range')


def parse_keyboard_query_list(list_query: str) -> list[dict]:
    if list_query:
        result = []
        for arg in list_query.split(','):
            keyword = arg.split("@")
            result.append({"value": keyword[0], "language": keyword[1]})
        return result
    raise AttributeError("Provided parameter is of None value.")


def get_numeric_query_parameter(parameter_name: str, default_value: int = None) -> int:
    parameter = request.args.get(parameter_name)
    if parameter:
        if parameter.isnumeric():
            return int(parameter)
    return default_value


def parse_query(query: str, required_values: list[str] = None) -> dict:
    arguments = {}
    for argument in query.split('&'):
        argument_parts = argument.split('=')
        if len(argument_parts) == 2:
            arg_name = argument_parts[0]
            arg_value = argument_parts[1]
            if arg_value[0] == arg_value[-1] == '"':
                arguments[arg_name] = arg_value[1:-1]
            elif arg_value.isnumeric():
                arguments[arg_name] = int(arg_value)
    if required_values:
        if not all(argument_name in arguments.keys() for argument_name in required_values):
            raise AttributeError('Required argument is missing.')
    return arguments


def get_parameter_or_default(dictionary: dict, value_name: str, default_value: any = None) -> any:
    if value_name in dictionary.keys():
        return dictionary[value_name]
    return default_value
