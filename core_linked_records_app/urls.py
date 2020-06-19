""" Url router for the core linked records app
"""
from django.conf.urls import url, include
from core_linked_records_app.views.user import ajax

urlpatterns = [
    url(
        r"retrieve-pid",
        ajax.RetrievePID.as_view(),
        name="core_linked_record_retrieve_pid_url",
    ),
    url(r"rest/", include("core_linked_records_app.rest.urls")),
]
