from flask import request


def get_numeric_query_parameter(parameter_name: str, default_value: int = None) -> int:
    parameter = request.args.get(parameter_name)
    if parameter:
        if parameter.isnumeric():
            return int(parameter)
    return default_value
