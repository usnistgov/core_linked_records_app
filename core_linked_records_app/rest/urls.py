""" Url router for the core linked records app
"""

from django.urls import re_path

from core_linked_records_app.rest.blob import views as blob_views
from core_linked_records_app.rest.pid import views as pid_views
from core_linked_records_app.rest.pid_settings import views as settings_views
from core_linked_records_app.rest.pid_path import views as pid_path_views
from core_linked_records_app.rest.providers import views as providers_views
from core_linked_records_app.rest.query import views as query_views

urlpatterns = [
    re_path(
        r"^query$",
        query_views.RetrieveQueryPidListView.as_view(),
        name="core_linked_records_app_query_pid",
    ),
]

urlpatterns += [
    re_path(
        r"^settings/$",
        settings_views.PidSettingsView.as_view(),
        name="core_linked_records_app_settings",
    ),
    re_path(
        r"^settings/path/$",
        pid_path_views.PidPathListView.as_view(),
        name="core_linked_records_app_settings_path_list",
    ),
    re_path(
        r"^settings/path/(?P<pk>[0-9]+)/$",
        pid_path_views.PidPathDetailView.as_view(),
        name="core_linked_records_app_settings_path_detail",
    ),
    re_path(
        r"^retrieve-list-pid",
        pid_views.RetrieveListPIDView.as_view(),
        name="core_linked_records_retrieve_list_pid",
    ),
    re_path(
        r"^retrieve-data-pid",
        pid_views.RetrieveDataPIDView.as_view(),
        name="core_linked_records_retrieve_data_pid",
    ),
    re_path(
        r"^retrieve-blob-pid",
        pid_views.RetrieveBlobPIDView.as_view(),
        name="core_linked_records_retrieve_blob_pid",
    ),
    re_path(
        r"^upload-blob-pid",
        blob_views.BlobUploadWithPIDView.as_view(),
        name="core_linked_records_upload_blob_pid",
    ),
    re_path(
        r"^(?P<provider>[^/]+)/(?P<record>.*)$",
        providers_views.ProviderRecordView.as_view(),
        name="core_linked_records_provider_record",
    ),
]
