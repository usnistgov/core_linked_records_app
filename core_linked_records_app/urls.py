""" Url router for the core linked records app
"""
from django.conf.urls import include
from django.urls import re_path

urlpatterns = [
    re_path(r"rest/", include("core_linked_records_app.rest.urls")),
]
