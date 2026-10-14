import json

from projects.common import Project
from projects.herodotus.database import load_places, load_polities


class Herodotus(Project):
    def fill_dict(self, request, context):
        polities = load_polities()
        data = json.dumps({"polities": polities, "places": load_places(polities)}, ensure_ascii=False)
        context["polity_data"] = data.replace("</", "<\\/")
