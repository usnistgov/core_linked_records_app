"""
"""


def get_dict_value_from_key_list(dictionary, key_list):
    """Browse dictionary content given an ordered list of keys.

    Params:
        dictionary:
        key_list:

    Returns:
    """
    while len(key_list) > 0:
        key = key_list.pop(0)

        if key in dictionary.keys():
            return get_dict_value_from_key_list(dictionary[key], key_list)
        else:
            return None

    return dictionary
