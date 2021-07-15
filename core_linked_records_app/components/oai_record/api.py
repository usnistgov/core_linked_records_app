""" Local resolver API
"""
from core_linked_records_app.components.pid_xpath import api as pid_xpath_api
from core_linked_records_app.utils.dict import get_dict_value_from_key_list
from core_oaipmh_harvester_app.components.oai_record import api as oai_record_data


def get_pid_for_data(oai_record_id, request):
    """Retrieve PID matching the document ID provided.

    Args:
        oai_record_id:
        request: HttpRequest

    Returns:
    """
    # Retrieve the document passed as input and extra the PID field.
    data = oai_record_data.get_by_id(oai_record_id, request.user)

    pid_xpath_object = pid_xpath_api.get_by_template_id(
        data.harvester_metadata_format.template.pk, request
    )
    pid_xpath = pid_xpath_object.xpath

    # Return PID value from the document and the PID_XPATH
    return get_dict_value_from_key_list(data["dict_content"], pid_xpath.split("."))
