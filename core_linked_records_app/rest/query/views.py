""" REST views for the query API
"""
import json
from urllib.parse import urljoin


from django.urls import reverse
from rest_framework import status
from rest_framework.response import Response

from core_linked_records_app import settings
from core_main_app.components.data import api as data_api
from core_main_app.rest.data.abstract_views import AbstractExecuteLocalQueryView
from core_main_app.utils.requests_utils.requests_utils import send_get_request


class ExecuteLocalPIDQueryView(AbstractExecuteLocalQueryView):
    def build_query(
        self, query, workspaces=None, templates=None, options=None, title=None
    ):
        """Build the query by adding an extra filter to limit to document with
        PID fields.

        Args:
            query:
            workspaces:
            templates:
            options:
            title:

        Returns:
            Query with additional PID filter
        """
        pid_query = {"$and": [{"dict_content.%s" % settings.PID_XPATH: {"$exists": 1}}]}
        query = super().build_query(query, workspaces, templates, options, title)

        if "$and" in query.keys():
            pid_query["$and"] += query["$and"]
        else:
            pid_query["$and"].append(query)

        return pid_query

    def execute_raw_query(self, raw_query, order_by_field):
        """Execute the raw query in database

        Args:

            raw_query: Query to execute
            order_by_field:

        Returns:
            Results of the query
        """
        pipeline = [
            {"$match": raw_query},
            {"$project": {"pid": "$dict_content.%s" % settings.PID_XPATH}},
        ]
        return data_api.aggregate(pipeline, self.request.user)

    def build_response(self, data_list):
        """Build the list of PIDs

        Args:

            data_list: List of data

        Returns:

            Paginated list of data
        """
        # Send list of PID as JSON
        return Response(
            [data["pid"] for data in data_list],
            status=status.HTTP_200_OK,
        )


if (
    "core_oaipmh_harvester_app" in settings.INSTALLED_APPS
    and "core_explore_oaipmh_app" in settings.INSTALLED_APPS
):
    from core_oaipmh_harvester_app.components.oai_record import api as oai_record_api
    from core_oaipmh_harvester_app.components.oai_registry import (
        api as oai_registry_api,
    )
    from core_explore_oaipmh_app.rest.query.views import ExecuteQueryView

    class ExecuteOaiPmhPIDQueryView(ExecuteQueryView):
        pid_xpath = None

        def build_query(self, query, templates, registries):
            """Build the query by adding an extra filter to limit to document with
            PID fields.

            Args:
                query:
                templates:
                registries:

            Returns:
                Query with additional PID filter
            """
            registry_info = oai_registry_api.get_by_id(json.loads(registries)[0])
            pid_xpath_request = send_get_request(
                urljoin(
                    registry_info.url.replace("/oaipmh/server", ""),
                    reverse("core_linked_records_app_settings"),
                )
            )

            if pid_xpath_request.status_code != status.HTTP_200_OK:
                raise Exception("Impossible to retrieve remote PID settings.")

            self.pid_xpath = pid_xpath_request.json()["xpath"]

            pid_query = {"$and": [{"dict_content.%s" % self.pid_xpath: {"$exists": 1}}]}
            query = super().build_query(query, templates, registries)

            if "$and" in query.keys():
                pid_query["$and"] += query["$and"]
            else:
                pid_query["$and"].append(query)

            return pid_query

        def execute_raw_query(self, raw_query, order_by_field):
            """Execute the raw query in database

            Args:

                raw_query: Query to execute
                order_by_field:

            Returns:
                Results of the query
            """
            if self.pid_xpath is None:
                raise Exception("Undefined PID xpath from remote server.")

            pipeline = [
                {"$match": raw_query},
                {"$project": {"pid": "$dict_content.%s" % self.pid_xpath}},
            ]
            return oai_record_api.aggregate(pipeline, self.request.user)

        def build_response(self, data_list):
            """Build the list of PIDs

            Args:

                data_list: List of data

            Returns:

                Paginated list of data
            """
            # Send list of PID as JSON
            return Response(
                [data["pid"] for data in data_list],
                status=status.HTTP_200_OK,
            )
