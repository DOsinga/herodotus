import json

from django.http import JsonResponse

from projects.common import Project
from projects.herodotus import database


class Herodotus(Project):
    def fill_dict(self, request, context):
        data = json.dumps(database.index(), ensure_ascii=False)
        context["polity_index"] = data.replace("</", "<\\/")

    def handle_request(self, handler, request):
        if handler == "year":
            return JsonResponse(database.year(int(request.GET["y"])))
        if handler == "polity":
            return JsonResponse(database.polity(request.GET["id"]))
