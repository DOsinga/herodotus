import colorsys
import math
import re
import sys
from collections import defaultdict

from database import ROOT, is_active, load_places, load_polities, resolved_control

STEP = 25
REACH_KM = (0, 50, 120, 250, 500)  # must match REACH_KM in static/territory.js
TOUCHING = 0.8
CELL = 4
PRESENT = 2025
LIGHTNESS = (0.34, 0.45, 0.56)
COLORS = [(hue, light) for hue in range(0, 360, 10) for light in LIGHTNESS]
SETTLE_YEARS = 100


def separation(a, b):
    hue_gap = min(abs(a[0] - b[0]), 360 - abs(a[0] - b[0]))
    return math.hypot(hue_gap / 40, (a[1] - b[1]) / 0.1)


def hex_color(color):
    r, g, b = colorsys.hls_to_rgb(color[0] / 360, color[1], 0.55)
    return "#" + "".join(f"{round(channel * 255):02x}" for channel in (r, g, b))


def hashed_color(polity_id):
    value = sum(ord(character) * 31 ** index for index, character in enumerate(polity_id))
    return COLORS[value % len(COLORS)]


def distance(a, b):
    la1, lo1, la2, lo2 = map(math.radians, (a[0], a[1], b[0], b[1]))
    h = math.sin((la2 - la1) / 2) ** 2 + math.cos(la1) * math.cos(la2) * math.sin((lo2 - lo1) / 2) ** 2
    return 12742 * math.asin(math.sqrt(h))


def positions_at(year, active, by_id, rows, points):
    positions = defaultdict(list)
    for place, start, end, polity_id, importance in rows:
        if polity_id in active and start <= year and (end is None or year <= end):
            positions[polity_id].append(points[place] + (REACH_KM[importance],))
    for polity_id in active:
        if not positions[polity_id]:
            point = by_id[polity_id]["point"]
            positions[polity_id].append((point["latitude"], point["longitude"], REACH_KM[2]))
    return positions


def neighbours(positions):
    cells = defaultdict(list)
    for polity_id, points in positions.items():
        for point in points:
            cells[(int(point[0] // CELL), int(point[1] // CELL))].append((polity_id, point))
    result = defaultdict(set)
    span = range(-2, 3)
    for (x, y), entries in cells.items():
        nearby = [entry for dx in span for dy in span for entry in cells.get((x + dx, y + dy), [])]
        for a, pa in entries:
            for b, pb in nearby:
                if a != b and b not in result[a] and distance(pa, pb) < TOUCHING * (pa[2] + pb[2]):
                    result[a].add(b)
                    result[b].add(a)
    return result


def clearance(color, others):
    return min((separation(color, other) for other in others), default=9)


def best_color(others, preferred):
    return max(COLORS, key=lambda color: (min(clearance(color, others), 2), -separation(color, preferred)))


def assign():
    polities = load_polities()
    by_id = {p["id"]: p for p in polities}
    places = load_places(polities)
    rows = resolved_control(places)
    points = {place["id"]: (place["point"]["latitude"], place["point"]["longitude"]) for place in places}
    predecessor = {}
    for polity in polities:
        for transition in polity.get("transitions", []):
            if transition["kind"] in ("succeeded_by", "merged_into", "split_into"):
                for target in transition["into"]:
                    predecessor.setdefault(target, polity["id"])
    first = min(period["start"] for p in polities for period in p["periods"])
    starts = {period["start"] for p in polities for period in p["periods"]}
    years = sorted(set(range(first - first % STEP, PRESENT + 1, STEP)) | starts)
    color = {}
    keys = defaultdict(dict)
    last_move = {}
    for year in years:
        active = [p["id"] for p in polities if is_active(p, year)]
        positions = positions_at(year, set(active), by_id, rows, points)
        touching = neighbours(positions)
        for pid in active:
            if pid in color:
                continue
            others = [color[other] for other in touching[pid] if other in color]
            parent = predecessor.get(pid)
            if parent in color and clearance(color[parent], others) >= 1:
                color[pid] = color[parent]
            else:
                color[pid] = best_color(others, hashed_color(pid))
            keys[pid][year] = color[pid]
            last_move[pid] = year
        for pid in sorted(active, key=lambda pid: -by_id[pid]["periods"][0]["start"]):
            others = [color[other] for other in touching[pid]]
            if clearance(color[pid], others) >= 0.6 or year - last_move[pid] < SETTLE_YEARS:
                continue
            new = best_color(others, color[pid])
            if clearance(new, others) > clearance(color[pid], others) + 0.3:
                hold = max(year - STEP, max(keys[pid]))
                if hold < year:
                    keys[pid][hold] = color[pid]
                color[pid] = new
                keys[pid][year] = new
                last_move[pid] = year
    clashes = 0
    for year in range(first - first % STEP, PRESENT + 1, STEP):
        active = [p["id"] for p in polities if is_active(p, year)]
        positions = positions_at(year, set(active), by_id, rows, points)
        for pid, others in neighbours(positions).items():
            clashes += sum(1 for other in others if pid < other and separation(color_at(keys[pid], year), color_at(keys[other], year)) < 0.6)
    return keys, clashes


def color_at(keys, year):
    before = [k for k in sorted(keys) if k <= year]
    return keys[before[-1]] if before else keys[min(keys)]


def write(keys):
    for polity_id, colors in keys.items():
        path = ROOT / "polities" / f"{polity_id}.md"
        text = re.sub(r"^colors:\n(  .*\n)*", "", path.read_text(), flags=re.M)
        block = "colors:\n" + "".join(f'  {year}: "{hex_color(c)}"\n' for year, c in sorted(colors.items()))
        text = re.sub(r"(^point:\n(  .*\n)+)", lambda m: m.group(1) + block, text, count=1, flags=re.M)
        path.write_text(text)


if __name__ == "__main__":
    keys, clashes = assign()
    changes = sum(len(colors) - 1 for colors in keys.values())
    print(f"{len(keys)} polities, {changes} colour keys beyond the first, {clashes} neighbour clashes left across sample years")
    if "--write" in sys.argv:
        write(keys)
