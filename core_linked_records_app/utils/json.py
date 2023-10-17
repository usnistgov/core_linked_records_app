""" JSON utilities functions.
"""
import logging

from core_main_app.utils.json_utils import validate_json_data

logger = logging.getLogger(__name__)


def set_value_at_dict_path(dictionary, dot_notation, value):
    """Create a value at a given dot notation path

    Params:
        dictionary:
        dot_notation:
        value:

    Returns:
    """
    # Split dot_notation except if it is None or ''
    key_list = dot_notation.split(".") if dot_notation else []

    # If the key list contains only one key, assign the value to that key and return the
    # updated dictionary.
    if len(key_list) == 1:
        dictionary[key_list.pop(0)] = value
        return dictionary

    if len(key_list) < 1:
        raise KeyError(f"Cannot set value at path {dot_notation}")

    key = key_list.pop(0)
    dictionary[key] = set_value_at_dict_path(
        dictionary[key] if key in dictionary.keys() else {},
        ".".join(key_list),
        value,
    )
    return dictionary


def can_create_value_at_dict_path(json_dict, template_dict, dict_path, value):
    """Evaluate if a value can be set in an JSON dict at a given dot notation path

    Params:
        json_dict:
        template_dict:
        dict_path:
        value:

    Returns:
        bool - True if the value can be created, False otherwise.
    """
    try:
        # Replace the current by the modified tree (containing mock PID) and
        # force document PID to be regenerated.
        set_value_at_dict_path(json_dict, dict_path, value)

        validation_error = validate_json_data(json_dict, template_dict)
        if validation_error is not None:
            raise Exception(f"Error while validating JSON: {validation_error}")

        return True
    except Exception as exc:  # pylint: disable=broad-except
        logger.info(
            "Function 'can_create_value_at_dict_path' raised %s", str(exc)
        )
        return False
