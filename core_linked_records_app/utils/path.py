""" Utilities to retrieve path information.
"""


def get_api_path_from_object(instance):
    """Retrieve API path from a given object instance.

    Code adapted from https://stackoverflow.com/questions/2020014.

    Args:
        instance:

    Returns:
        str: A dot delimited path to the API of the given object
    """
    instance_class = instance.__class__
    module = instance_class.__module__

    if module == "__builtin__":
        # avoid outputs like '__builtin__.str'
        model_path = instance_class.__name__
    else:
        model_path = module + "." + instance_class.__name__

    return f"{'.'.join(model_path.split('.')[:-2])}.api"
