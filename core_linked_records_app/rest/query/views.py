""" REST views for the query API
"""
from rest_framework import status
from rest_framework.response import Response

from core_linked_records_app import settings
from core_main_app.components.data import api as data_api
from core_main_app.rest.data.abstract_views import AbstractExecuteLocalQueryView


class ExecutePIDQueryView(AbstractExecuteLocalQueryView):
    def build_query(
        self, query, workspaces=None, templates=None, options=None, title=None
    ):
        """ Build the query by adding an extra filter to limit to document with
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
        """ Execute the raw query in database

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
        """ Build the list of PIDs

        Args:

            data_list: List of data

        Returns:

            Paginated list of data
        """
        # Send list of PID as JSON
        return Response([data["pid"] for data in data_list], status=status.HTTP_200_OK,)
