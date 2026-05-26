"""Local resolver API"""

import logging

from core_linked_records_app.components.oai_record.access_control import (
    can_get_pid_for_data,
)
from core_linked_records_app.utils.exceptions import MultiplePidError
from core_linked_records_app.components.pid_path import api as pid_path_api
from core_linked_records_app.utils.dict import get_value_from_dot_notation
from core_main_app.access_control.decorators import access_control
from core_main_app.commons.exceptions import ApiError
from core_oaipmh_harvester_app.components.oai_record import (
    api as oai_record_data,
)

logger = logging.getLogger(__name__)


@access_control(can_get_pid_for_data)
def get_pid_for_data(oai_record_id, request):
    """Retrieve PID matching the document ID provided.

    Args:
        oai_record_id:
        request: HttpRequest

    Returns:
    """
    try:
        # Retrieve the document passed as input and extra the PID field.
        data = oai_record_data.get_by_id(oai_record_id, request.user)

        # Iterate through all possible paths for the template and enforce exclusivity
        pid_paths = pid_path_api.get_by_template(
            data.harvester_metadata_format.template, request.user
        )

        found_pid = None
        dict_content = data.get_dict_content()

        for pid_path_object in pid_paths:
            pid_path = pid_path_object.path
            pid_value = get_value_from_dot_notation(dict_content, pid_path)

            if pid_value:
                if found_pid is not None:
                    raise MultiplePidError(
                        f"OAI record '{oai_record_id}' contains multiple valid PIDs "
                        f"across defined paths for template {data.harvester_metadata_format.template.pk}"
                    )
                found_pid = pid_value

        return found_pid
    except MultiplePidError:
        raise
    except Exception as exc:
        error_message = (
            "An unexpected error occurred while retrieving PID for OAI data"
        )

        logger.error("%s: %s", error_message, str(exc))
        raise ApiError(f"{error_message}.") from exc
