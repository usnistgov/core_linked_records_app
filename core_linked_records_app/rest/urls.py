""" Url router for the core linked records app
"""
from django.conf.urls import url

from core_linked_records_app.rest.blob import views as blob_views
from core_linked_records_app.rest.pid import views as pid_views
from core_linked_records_app.rest.query import views as query_views
from core_linked_records_app.rest.pid_settings import views as settings_views
from core_linked_records_app.rest.pid_xpath import views as xpath_views
from core_linked_records_app.rest.providers import views as providers_views

urlpatterns = [
    url(
        r"^query$",
        query_views.RetrieveQueryPidListView.as_view(),
        name="core_linked_records_app_query_pid",
    ),
]

urlpatterns += [
    url(
        r"^settings/$",
        settings_views.PidSettingsView.as_view(),
        name="core_linked_records_app_settings",
    ),
    url(
        r"^settings/xpath/$",
        xpath_views.PidXpathListView.as_view(),
        name="core_linked_records_app_settings_xpath_list",
    ),
    url(
        r"^settings/xpath/(?P<pk>[0-9]+)/$",
        xpath_views.PidXpathDetailView.as_view(),
        name="core_linked_records_app_settings_xpath_detail",
    ),
    url(
        r"^retrieve-list-pid",
        pid_views.RetrieveListPIDView.as_view(),
        name="core_linked_records_retrieve_list_pid",
    ),
    url(
        r"^retrieve-data-pid",
        pid_views.RetrieveDataPIDView.as_view(),
        name="core_linked_records_retrieve_data_pid",
    ),
    url(
        r"^retrieve-blob-pid",
        pid_views.RetrieveBlobPIDView.as_view(),
        name="core_linked_records_retrieve_blob_pid",
    ),
    url(
        r"^upload-blob-pid",
        blob_views.BlobUploadWithPIDView.as_view(),
        name="core_linked_records_upload_blob_pid",
    ),
    url(
        r"^(?P<provider>[^/]+)/(?P<record>.*)$",
        providers_views.ProviderRecordView.as_view(),
        name="core_linked_records_provider_record",
    ),
]
