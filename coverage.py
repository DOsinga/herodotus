import sys

from database import is_active, load_places, load_polities, resolved_control


polities = load_polities()
rows = resolved_control(load_places(polities))
for year in map(int, sys.argv[1:]):
    placed = {polity for _, start, end, polity, _ in rows if start <= year and (end is None or year <= end)}
    missing = [p for p in polities if p.get("type") != "culture" and is_active(p, year) and p["id"] not in placed]
    print(f"{year}: {len(missing)} active polities without a place")
    for polity in missing:
        print(f"  {polity['id']} ({polity['point']['name']})")
