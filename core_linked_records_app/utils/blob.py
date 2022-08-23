""" Utilities related to blobs with PID
"""
import logging
import re

from django.urls import reverse

from core_linked_records_app.components.blob import api as blob_api
from core_linked_records_app.components.local_id import api as local_id_api

logger = logging.getLogger(__name__)


def get_blob_download_regex(xml_string):
    """Retrieve a list of blob PID from an XML document. Performs a DB lookup
    to ensure the PID belong to blobs.

    Args:
        xml_string (str): Content of the XML file

    Returns:
        list<str>: List of blobs found in the given text
    """
    mock_string = "mock_string"

    # Build django url to download a blob using PID
    blob_pid_url = reverse(
        "core_linked_records_provider_record",
        kwargs={"provider": mock_string, "record": mock_string},
    )
    blob_pid_url = re.sub(f"{mock_string}/?", "", blob_pid_url)

    # Apply the regex
    document_pid_list = re.findall(
        f">(http[s]?:[^<>]+{blob_pid_url}[^/]+/[^/]+/[^/]+/?)<", xml_string
    )

    blob_urls = list()

    for document_pid in document_pid_list:
        try:
            record_name = "/".join(document_pid.split("/")[-2:])
            record_object = local_id_api.get_by_name(record_name)
            blob_api.get_pid_for_blob(record_object.record_object_id)
            blob_urls.append(document_pid)
        except Exception as exc:
            logger.warning("Retrieving blob URL raised an exception: %s", str(exc))
            continue

    return blob_urls
