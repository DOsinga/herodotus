from database import load_places, load_polities, place_gaps


places = load_places(load_polities())
by_id = {place["id"]: place for place in places}
for place_id, start, end in place_gaps(places):
    point = by_id[place_id]["point"]
    print(f"{place_id} {start} {end} {point['latitude']} {point['longitude']}")
