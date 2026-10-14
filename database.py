import re
from pathlib import Path

import yaml


ROOT = Path(__file__).parent
ID = re.compile(r"^[a-z][a-z0-9_]*$")
TYPES = {"chiefdom", "culture"}
TRANSITION_KINDS = {"absorbed_into", "merged_into", "split_into", "succeeded_by", "broke_away_from"}


def load_polities():
    polities = []
    for path in sorted((ROOT / "polities").glob("*.md")):
        text = path.read_text(encoding="utf-8")
        _, frontmatter, _ = text.split("---", 2)
        polity = yaml.safe_load(frontmatter)
        assert polity["id"] == path.stem, path
        polities.append(polity)
    validate_polities(polities)
    return polities


def is_active(polity, year):
    return any(
        period["start"] <= year and (period["end"] is None or year <= period["end"])
        for period in polity["periods"]
    )


def validate_polities(polities):
    ids = set()
    names = set()
    for polity in polities:
        assert set(polity) - {"transitions", "note", "type"} == {"id", "name", "wikipedia", "description", "periods", "point"}, polity["id"]
        assert isinstance(polity["description"], str) and len(polity["description"].split()) == 120, polity["id"]
        assert "type" not in polity or polity["type"] in TYPES, polity["id"]
        assert "note" not in polity or isinstance(polity["note"], str) and polity["note"], polity["id"]
        assert ID.fullmatch(polity["id"]), polity["id"]
        assert polity["id"] not in ids, polity["id"]
        assert polity["name"] not in names, polity["name"]
        assert polity["wikipedia"].startswith("https://en.wikipedia.org/wiki/"), polity["id"]
        assert polity["periods"], polity["id"]

        previous_end = None
        for index, period in enumerate(polity["periods"]):
            assert set(period) == {"start", "end"}, polity["id"]
            assert isinstance(period["start"], int), polity["id"]
            if period["end"] is None:
                assert index == len(polity["periods"]) - 1, polity["id"]
            else:
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

    by_id = {polity["id"]: polity for polity in polities}
    for polity in polities:
        for transition in polity.get("transitions", []):
            year = transition["year"]
            kind = transition["kind"]
            assert kind in TRANSITION_KINDS, polity["id"]
            if kind == "broke_away_from":
                assert set(transition) == {"year", "kind", "from"}, polity["id"]
                assert any(period["start"] == year for period in polity["periods"]), polity["id"]
                targets = transition["from"]
            else:
                assert set(transition) == {"year", "kind", "into"}, polity["id"]
                assert any(period["end"] == year for period in polity["periods"]), polity["id"]
                targets = transition["into"]
            if kind == "split_into":
                assert len(targets) >= 2, polity["id"]
            else:
                assert len(targets) == 1, polity["id"]
            for target_id in targets:
                assert target_id in by_id, (polity["id"], target_id)
                target = by_id[target_id]
                if kind in ("absorbed_into", "broke_away_from"):
                    assert is_active(target, year), (polity["id"], target_id)
                else:
                    begins = any(period["start"] in (year, year + 1) for period in target["periods"])
                    assert begins, (polity["id"], target_id)

