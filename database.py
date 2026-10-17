import json
import os
import re
import sqlite3
from pathlib import Path

import yaml


ROOT = Path(__file__).parent
ID = re.compile(r"^[a-z][a-z0-9_]*$")
COLOR = re.compile(r"^#[0-9a-f]{6}$")
TYPES = {"chiefdom", "culture"}
TRANSITION_KINDS = {"absorbed_into", "merged_into", "split_into", "succeeded_by", "broke_away_from"}


class UniqueKeyLoader(yaml.CSafeLoader):
    def construct_mapping(self, node, deep=False):
        keys = [self.construct_object(key, deep=deep) for key, _ in node.value]
        assert len(keys) == len(set(keys)), f"duplicate key in {keys}"
        return super().construct_mapping(node, deep)


def load_records(folder):
    records = []
    for path in sorted((ROOT / folder).glob("*.md")):
        text = path.read_text(encoding="utf-8")
        _, frontmatter, _ = text.split("---", 2)
        record = yaml.load(frontmatter, Loader=UniqueKeyLoader)
        assert record["id"] == path.stem, path
        records.append(record)
    return records


def load_polities():
    polities = load_records("polities")
    validate_polities(polities)
    return polities


def load_places(polities):
    places = load_records("places")
    validate_places(places, polities)
    return places


def is_active(polity, year):
    return any(
        period["start"] <= year and (period["end"] is None or year <= period["end"])
        for period in polity["periods"]
    )


def validate_polities(polities):
    ids = set()
    names = set()
    for polity in polities:
        assert set(polity) - {"transitions", "note", "type", "colors"} == {"id", "name", "wikipedia", "description", "periods", "point"}, polity["id"]
        assert "colors" not in polity or polity["colors"] and all(
            isinstance(year, int) and COLOR.fullmatch(color) for year, color in polity["colors"].items()
        ), polity["id"]
        assert isinstance(polity["description"], str) and 105 <= len(polity["description"].split()) <= 130, polity["id"]
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
        validate_point(point, polity["id"])

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



def validate_point(point, record_id):
    assert -90 <= point["latitude"] <= 90, record_id
    assert -180 <= point["longitude"] <= 180, record_id
    assert point["latitude"] != 0 or point["longitude"] != 0, record_id


def validate_places(places, polities):
    by_id = {polity["id"]: polity for polity in polities}
    places_by_id = {place["id"]: place for place in places}
    ids = set()
    names = set()
    links = set()
    for place in places:
        assert set(place) - {"note"} == {"id", "name", "wikipedia", "point", "control"}, place["id"]
        assert ID.fullmatch(place["id"]), place["id"]
        assert place["id"] not in ids, place["id"]
        assert place["name"] not in names, place["name"]
        assert place["wikipedia"] not in links, place["id"]
        assert place["wikipedia"].startswith("https://en.wikipedia.org/wiki/"), place["id"]
        assert "note" not in place or isinstance(place["note"], str) and place["note"], place["id"]
        assert set(place["point"]) == {"latitude", "longitude"}, place["id"]
        validate_point(place["point"], place["id"])
        assert place["control"], place["id"]

        previous_end = None
        for index, span in enumerate(place["control"]):
            assert set(span) - {"polity", "follows"} == {"start", "end", "importance"}, place["id"]
            assert span["importance"] in (1, 2, 3, 4), place["id"]
            assert isinstance(span["start"], int), place["id"]
            assert previous_end is None or span["start"] > previous_end, place["id"]
            if span["end"] is None:
                assert index == len(place["control"]) - 1, place["id"]
            else:
                assert isinstance(span["end"], int) and span["start"] <= span["end"], place["id"]
            previous_end = span["end"]
            if "follows" in span:
                assert "polity" not in span, place["id"]
                leader = places_by_id[span["follows"]]
                assert all("follows" not in other for other in leader["control"]), (place["id"], span["follows"])
                continue
            polity = by_id[span["polity"]]
            assert polity.get("type") != "culture", (place["id"], span["polity"])
            assert any(
                period["start"] <= span["start"]
                and (period["end"] is None or span["end"] is not None and span["end"] <= period["end"])
                for period in polity["periods"]
            ), (place["id"], span["polity"], span["start"])

        ids.add(place["id"])
        names.add(place["name"])
        links.add(place["wikipedia"])

def resolved_control(places):
    by_id = {place["id"]: place for place in places}
    rows = []
    for place in places:
        for span in place["control"]:
            if "polity" in span:
                rows.append((place["id"], span["start"], span["end"], span["polity"], span["importance"]))
                continue
            for lead in by_id[span["follows"]]["control"]:
                start = max(span["start"], lead["start"])
                ends = [end for end in (span["end"], lead["end"]) if end is not None]
                end = min(ends) if ends else None
                if end is None or start <= end:
                    rows.append((place["id"], start, end, lead["polity"], span["importance"]))
    return rows


PATH = ROOT / "herodotus.sqlite"
SCHEMA = """
CREATE TABLE polities (
    id TEXT PRIMARY KEY, name TEXT, type TEXT, wikipedia TEXT, description TEXT, note TEXT,
    point_name TEXT, latitude REAL, longitude REAL, transitions TEXT, colors TEXT
);
CREATE TABLE periods (polity TEXT, start INTEGER, end INTEGER);
CREATE TABLE places (id TEXT PRIMARY KEY, name TEXT, wikipedia TEXT, latitude REAL, longitude REAL);
CREATE TABLE control (place TEXT, start INTEGER, end INTEGER, polity TEXT, importance INTEGER);
CREATE INDEX periods_years ON periods (start, end);
CREATE INDEX control_years ON control (start, end);
"""
ACTIVE = "start <= :year AND (end IS NULL OR :year <= end)"


def build():
    polities = load_polities()
    places = load_places(polities)
    partial = PATH.with_suffix(".partial")
    partial.unlink(missing_ok=True)
    db = sqlite3.connect(partial)
    db.executescript(SCHEMA)
    db.executemany("INSERT INTO polities VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", [
        (p["id"], p["name"], p.get("type"), p["wikipedia"], p["description"], p.get("note"),
         p["point"]["name"], p["point"]["latitude"], p["point"]["longitude"],
         json.dumps(p.get("transitions", []), ensure_ascii=False), json.dumps(sorted(p.get("colors", {}).items())))
        for p in polities
    ])
    db.executemany("INSERT INTO periods VALUES (?, ?, ?)", [
        (p["id"], q["start"], q["end"]) for p in polities for q in p["periods"]
    ])
    db.executemany("INSERT INTO places VALUES (?, ?, ?, ?, ?)", [
        (p["id"], p["name"], p["wikipedia"], p["point"]["latitude"], p["point"]["longitude"]) for p in places
    ])
    db.executemany("INSERT INTO control VALUES (?, ?, ?, ?, ?)", resolved_control(places))
    db.commit()
    db.close()
    os.replace(partial, PATH)


def is_stale():
    if not PATH.exists():
        return True
    sources = [Path(__file__), *ROOT.glob("polities/*.md"), *ROOT.glob("places/*.md")]
    built = PATH.stat().st_mtime
    return any(path.stat().st_mtime > built for path in sources)


def connect():
    if is_stale():
        build()
    db = sqlite3.connect(PATH)
    db.row_factory = sqlite3.Row
    return db


def color_at(colors, year):
    if not colors:
        return None
    before = [(y, c) for y, c in colors if y <= year]
    after = [(y, c) for y, c in colors if y > year]
    if not before or not after:
        return (before or after)[-1 if before else 0][1]
    (y0, c0), (y1, c1) = before[-1], after[0]
    t = (year - y0) / (y1 - y0)
    channels = [round(int(c0[i:i + 2], 16) * (1 - t) + int(c1[i:i + 2], 16) * t) for i in (1, 3, 5)]
    return "#" + "".join(f"{channel:02x}" for channel in channels)


def year(value):
    db = connect()
    polities = [
        {**{key: row[key] for key in ("id", "name", "type", "latitude", "longitude")},
         "color": color_at(json.loads(row["colors"]), value)}
        for row in db.execute(
            f"SELECT id, name, type, latitude, longitude, colors FROM polities"
            f" WHERE id IN (SELECT polity FROM periods WHERE {ACTIVE}) ORDER BY id",
            {"year": value},
        )
    ]
    places = db.execute(
        f"SELECT places.id, name, latitude, longitude, polity, importance FROM control"
        f" JOIN places ON places.id = control.place WHERE {ACTIVE} ORDER BY places.id",
        {"year": value},
    ).fetchall()
    gaps = db.execute(
        f"SELECT id, name, latitude, longitude FROM places WHERE id IN ("
        f" SELECT place FROM control GROUP BY place"
        f" HAVING MIN(start) <= :year AND (MAX(end IS NULL) OR :year <= MAX(end)))"
        f" AND id NOT IN (SELECT place FROM control WHERE {ACTIVE}) ORDER BY id",
        {"year": value},
    ).fetchall()
    return {
        "year": value,
        "polities": polities,
        "places": [dict(row) for row in places],
        "gaps": [dict(row) for row in gaps],
    }


def polity(polity_id):
    db = connect()
    row = db.execute("SELECT * FROM polities WHERE id = ?", (polity_id,)).fetchone()
    record = dict(row)
    record["transitions"] = json.loads(record["transitions"])
    record["colors"] = json.loads(record["colors"])
    record["periods"] = [
        dict(period) for period in db.execute("SELECT start, end FROM periods WHERE polity = ? ORDER BY start", (polity_id,))
    ]
    return record


def index():
    db = connect()
    names = db.execute("SELECT id, name FROM polities ORDER BY name").fetchall()
    first, last, open_ended = db.execute(
        "SELECT MIN(start), MAX(COALESCE(end, start)), MAX(end IS NULL) FROM periods"
    ).fetchone()
    return {"names": [[row["id"], row["name"]] for row in names], "first": first, "last": last, "open_ended": bool(open_ended)}
