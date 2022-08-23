""" REST views for the query API
"""
from rest_framework import status
from rest_framework.response import Response

from core_main_app.components.data import api as data_api
from core_main_app.rest.data.abstract_views import AbstractExecuteLocalQueryView
from core_linked_records_app import settings
from core_linked_records_app.components.pid_xpath import api as pid_xpath_api
from core_linked_records_app.utils.dict import get_value_from_dot_notation
from core_linked_records_app.utils.pid import is_valid_pid_value


class ExecuteLocalPIDQueryView(AbstractExecuteLocalQueryView):
    """Execute Local PID Query View"""

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
        pid_xpath_list = [
            pid_xpath_object.xpath
            for pid_xpath_object in pid_xpath_api.get_all(self.request)
        ] + [settings.PID_XPATH]
        pid_query = {
            "$and": [
                {
                    "$or": [
                        {f"dict_content.{pid_xpath}": {"$exists": 1}}
                        for pid_xpath in pid_xpath_list
                    ]
                }
            ]
        }
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
        pid_list = list()
        data_list = data_api.execute_json_query(raw_query, self.request.user)

        for data in data_list:
            pid_xpath_object = pid_xpath_api.get_by_template(
                data.template, self.request
            )
            pid_xpath = pid_xpath_object.xpath

            data_pid = get_value_from_dot_notation(
                data.get_dict_content(),
                pid_xpath,
            )

            if not is_valid_pid_value(
                data_pid, settings.ID_PROVIDER_SYSTEM_NAME, settings.PID_FORMAT
            ):
                continue

            pid_list.append({"pid": data_pid})

        return pid_list

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
    from core_explore_oaipmh_app.rest.query.views import ExecuteQueryView

    class ExecuteOaiPmhPIDQueryView(ExecuteQueryView):
        """ " Execute Oai Pmh PID Query View"""

        pid_xpath_list = None

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
            self.pid_xpath_list = [
                pid_xpath_object.xpath
                for pid_xpath_object in pid_xpath_api.get_all(self.request)
            ] + [settings.PID_XPATH]
            pid_query = {
                "$and": [
                    {
                        "$or": [
                            {f"dict_content.{pid_xpath}": {"$exists": 1}}
                            for pid_xpath in self.pid_xpath_list
                        ]
                    }
                ]
            }
            query = super().build_query(query, templates, registries)

            if "$and" in query.keys():
                pid_query["$and"] += query["$and"]
            else:
                pid_query["$and"].append(query)

            return pid_query

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
