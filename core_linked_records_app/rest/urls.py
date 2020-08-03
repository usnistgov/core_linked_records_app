""" Url router for the core linked records app
"""
from django.conf.urls import url

from core_linked_records_app.rest.providers import views as providers_views
from core_linked_records_app.rest.query import views as query_views

urlpatterns = [
    url(
        r"^query",
        query_views.ExecutePIDQueryView.as_view(),
        name="core_linked_records_app_query",
    ),
    url(
        r"^(?P<provider>[^/]+)/(?P<record>.*)$",
        providers_views.ProviderRecord.as_view(),
        name="core_linked_records_app_rest_provider_record_view",
    ),
]
