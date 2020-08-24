""" Url router for the core linked records app
"""
from django.conf.urls import url, include
from core_linked_records_app.views.user import ajax

urlpatterns = [
    url(
        r"retrieve-list-pid",
        ajax.RetrieveListPID.as_view(),
        name="core_linked_record_retrieve_list_pid_url",
    ),
    url(
        r"retrieve-data-pid",
        ajax.RetrieveDataPID.as_view(),
        name="core_linked_record_retrieve_data_pid_url",
    ),
    url(r"rest/", include("core_linked_records_app.rest.urls")),
]
