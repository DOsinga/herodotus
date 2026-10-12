from database import load_polities


polities = load_polities()
active_1500 = [
    polity
    for polity in polities
    if any(period["start"] <= 1500 <= period["end"] for period in polity["periods"])
]
print(f"valid: {len(polities)} polities, {len(active_1500)} active in 1500")
