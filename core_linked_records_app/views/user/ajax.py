""" Ajax views accessible by users.
"""
import json

from django.http import JsonResponse
from django.views import View

from core_linked_records_app.components.data.api import get_pids_for_data_list


class RetrievePID(View):
    """ Retrieve PIDs for a given list of data IDs.
    """

    def post(self, request):
        data_list = json.loads(request.POST["data_list"])
        return JsonResponse({"pids": get_pids_for_data_list(data_list, request.user)})
