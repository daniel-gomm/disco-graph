from flask import (
    Blueprint, request, jsonify
)
from .rdf_interface import BASE_CONNECTOR

bp = Blueprint('keyword', __name__, url_prefix='/keyword')

rdf_connector = BASE_CONNECTOR


@bp.get('/languages')
def get_languages():
    languages = rdf_connector.get_keyword_languages()
    try:
        return languages, 200
    except:
        return 'Failed to retrieve languages.', 500
