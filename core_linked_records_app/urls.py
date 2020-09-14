""" Url router for the core linked records app
"""
from django.conf.urls import url, include

urlpatterns = [
    url(r"rest/", include("core_linked_records_app.rest.urls")),
]
