""" Url router for the core linked records app
"""
from django.conf.urls import url

from core_linked_records_app.rest.handle import views as handle_rest_views

urlpatterns = [
    url(r'^(?P<system>[^/]+)/(?P<handle>.+)$',
        handle_rest_views.HandleRecord.as_view(),
        name='core_linked_records_app_rest_handle_record_view')
]
