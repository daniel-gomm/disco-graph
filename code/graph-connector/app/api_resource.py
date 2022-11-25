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
    limit = request.args.get('limit')
    if limit:
        if limit.isnumeric():
            limit = int(limit)
        else:
            limit = None

    if not keys:
        return "Invalid query!", 400

    keywords = rdf_connector.get_completed_keywords(start_keys=keys, filter_attributes=get_attribute_filters(),
                                                    filter_year_range=get_year_filter(), limit=limit)
    return jsonify(keywords), 200


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
