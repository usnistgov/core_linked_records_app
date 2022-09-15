""" Dict
"""


def get_value_from_dot_notation(dictionary, dot_notation):
    """Retrieve dictionary content given a dot notation path.

    Params:
        dictionary:
        key_list:

    Returns:
    """
    # Split dot_notation except if it is None or ''
    key_list = dot_notation.split(".") if dot_notation else []

    while len(key_list) > 0:
        key = key_list.pop(0)

        if key in dictionary.keys():
            return get_value_from_dot_notation(dictionary[key], ".".join(key_list))
        return None

    return dictionary


def is_dot_notation_in_dictionary(dictionary, dot_notation):
    """Given a dot notation path, find if it is present in a dictionary.

    Params:
        dictionary:
        dot_notation:

    Returns:
    """
    # Split dot_notation except if it is None or ''
    key_list = dot_notation.split(".") if dot_notation else []

    while len(key_list) > 0:
        key = key_list.pop(0)

        if key in dictionary.keys():
            return is_dot_notation_in_dictionary(dictionary[key], ".".join(key_list))
        return False

    return True
