import json

from projects.common import Project
from projects.herodotus.database import load_polities


class Herodotus(Project):
    def fill_dict(self, request, context):
        data = json.dumps({"polities": load_polities()}, ensure_ascii=False)
        context["polity_data"] = data.replace("</", "<\\/")
