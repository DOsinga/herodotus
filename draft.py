import json
from pathlib import Path

from database import ROOT, load_polities

PRESENT = 2026
POLITIES = {polity["id"]: polity for polity in load_polities()}

FRANKISH_BURGUNDY = ["merovingian_burgundy", "merovingian_francia_late", "neustria"]
ALEMANNIC = ["holy_roman_empire", "duchy_swabia", "east_francia", "carolingian_francia", "alamannic_duchy", "austrasia",
             "merovingian_francia_late"]
FRANCE = ["kingdom_france", "french_first_republic", "first_french_empire", "french_second_republic", "second_french_empire",
          "french_third_republic", "vichy_france", "provisional_government_france", "french_fourth_republic", "france"]
GERMANY = ["german_empire", "weimar_republic", "nazi_germany", "west_germany"]
AUSTRIA = ["austria", "austrian_empire", "austria_hungary", "nazi_germany"]
ITALY = ["kingdom_italy", "italy"]
ENGLAND = ["kingdom_england", "commonwealth_england", "kingdom_great_britain", "united_kingdom_gbi", "united_kingdom"]
SCOTLAND = ["kingdom_scotland", "commonwealth_england", "kingdom_great_britain", "united_kingdom_gbi", "united_kingdom"]
IRELAND = ["kingdom_england", "commonwealth_england", "kingdom_great_britain", "united_kingdom_gbi", "ireland"]


def period_of(polity_id, year):
    for period in POLITIES[polity_id]["periods"]:
        if period["start"] <= year and (period["end"] is None or year <= period["end"]):
            return period["start"], period["end"]


def spans(segments):
    result = []
    for start, end, candidates, importance in segments:
        for year in range(start, (PRESENT if end is None else end) + 1):
            active = [c for c in candidates if period_of(c, year)]
            continuing = [c for c in active if period_of(c, year)[1] != year]
            holder = (continuing or active or [None])[0]
            last = result[-1] if result else None
            if (holder and last and last["polity"] == holder and last["end"] == year - 1
                    and last["importance"] == importance and period_of(holder, year) == period_of(holder, year - 1)):
                last["end"] = year
            elif holder:
                result.append({"start": year, "end": year, "polity": holder, "importance": importance})
    for span in result:
        if span["end"] == PRESENT and period_of(span["polity"], PRESENT)[1] is None:
            span["end"] = None
    return result


def follows(place_id, start, end, importance):
    return [{"start": start, "end": end, "follows": place_id, "importance": importance}]


def roman(start, end, importance):
    segments = [(start, -28, ["roman_republic"], importance), (max(start, -27), min(end, 394), ["roman_empire"], importance),
                (395, end, ["western_roman_empire"], importance)]
    return [segment for segment in segments if segment[0] <= segment[1]]


def roman_britain(start, importance):
    return [(start, 394, ["carausian_empire", "gallic_empire", "roman_empire"], importance),
            (395, 409, ["western_roman_empire"], importance)]


def burgundy(importance, start=443):
    segments = [(443, 533, ["burgundian_kingdom"], importance), (534, 750, FRANKISH_BURGUNDY, importance),
                (751, 842, ["carolingian_francia"], importance), (843, 854, ["middle_francia"], importance),
                (855, 869, ["lotharingia"], importance), (888, 932, ["upper_burgundy"], importance),
                (933, 1031, ["kingdom_burgundy"], importance), (1032, 1249, ["holy_roman_empire"], importance)]
    return [segment for segment in segments if segment[1] >= start]


def italian(importance, start=476, end=1099):
    segments = [(476, 492, ["kingdom_odoacer"], importance), (493, 553, ["ostrogothic_kingdom"], importance),
                (554, 567, ["byzantine_empire"], importance), (568, 773, ["lombard_kingdom"], importance),
                (774, 842, ["carolingian_francia"], importance), (843, 854, ["middle_francia"], importance),
                (855, 961, ["carolingian_italy"], importance), (962, end, ["holy_roman_empire"], importance)]
    return [segment for segment in segments if segment[1] >= start]


def write(place_id, name, title, latitude, longitude, control, note=None):
    lines = ["---", f"id: {place_id}", f"name: {json.dumps(name, ensure_ascii=False) if ':' in name else name}",
             "wikipedia: https://en.wikipedia.org/wiki/" + title.replace(" ", "_"), "point:",
             f"  latitude: {latitude}", f"  longitude: {longitude}"]
    if note:
        lines.append("note: " + json.dumps(note, ensure_ascii=False))
    lines.append("control:")
    for span in control:
        key = "follows" if "follows" in span else "polity"
        end = "null" if span["end"] is None else span["end"]
        lines += [f"- start: {span['start']}", f"  end: {end}", f"  {key}: {span[key]}", f"  importance: {span['importance']}"]
    Path(ROOT, "places", f"{place_id}.md").write_text("\n".join(lines) + "\n---\n")
