import re
from pathlib import Path

import yaml


ROOT = Path(__file__).parent
ID = re.compile(r"^[a-z][a-z0-9_]*$")


def load_polities():
    polities = []
    for path in sorted((ROOT / "polities").glob("*.md")):
        text = path.read_text()
        _, frontmatter, _ = text.split("---", 2)
        polity = yaml.safe_load(frontmatter)
        polities.append(polity)
    validate_polities(polities)
    return polities


def validate_polities(polities):
    ids = set()
    names = set()
    for polity in polities:
        assert set(polity) == {"id", "name", "wikipedia", "periods", "point"}, polity["id"]
        assert ID.fullmatch(polity["id"]), polity["id"]
        assert polity["id"] not in ids, polity["id"]
        assert polity["name"] not in names, polity["name"]
        assert polity["wikipedia"].startswith("https://en.wikipedia.org/wiki/"), polity["id"]
        assert polity["periods"], polity["id"]

        previous_end = None
        for period in polity["periods"]:
            assert set(period) == {"start", "end"}, polity["id"]
            assert isinstance(period["start"], int), polity["id"]
            assert isinstance(period["end"], int), polity["id"]
            assert period["start"] <= period["end"], polity["id"]
            assert previous_end is None or period["start"] > previous_end, polity["id"]
            previous_end = period["end"]

        point = polity["point"]
        assert set(point) == {"name", "latitude", "longitude"}, polity["id"]
        assert point["name"], polity["id"]
        assert -90 <= point["latitude"] <= 90, polity["id"]
        assert -180 <= point["longitude"] <= 180, polity["id"]
        assert point["latitude"] != 0 or point["longitude"] != 0, polity["id"]

        ids.add(polity["id"])
        names.add(polity["name"])
