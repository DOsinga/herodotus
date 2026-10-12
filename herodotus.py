import json

from projects.common import Project
from projects.herodotus.database import load_polities


class Herodotus(Project):
    def fill_dict(self, request, context):
        polities = load_polities()
        for polity in polities:
            polity["point"] = {
                "name": polity["point"]["name"],
                "lat": polity["point"]["latitude"],
                "lon": polity["point"]["longitude"],
            }
        data = json.dumps({"polities": polities}, ensure_ascii=False)
        context["polity_data"] = data.replace("</", "<\\/")
