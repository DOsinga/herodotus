from database import is_active, load_polities


polities = load_polities()
names = {polity["name"] for polity in polities}
active_1500 = {polity["name"] for polity in polities if is_active(polity, 1500)}
assert "Kingdom of Portugal" in active_1500
assert "Old Swiss Confederacy" in active_1500
assert "Habsburg Netherlands" in active_1500
assert {"Wattasid Sultanate", "Zayyanid Kingdom of Tlemcen", "Hafsid Sultanate"} <= active_1500
assert {"Lordship of Ireland", "Kingdom of Tyrone", "Tyrconnell", "Kingdom of Thomond"} <= active_1500
assert {"Tuʻi Tonga Empire", "Kazakh Khanate", "Khanate of Kazan", "Khanate of Sibir", "Astrakhan Khanate", "Kanem–Bornu Empire"} <= active_1500
assert "Kingdom of Sicily" not in active_1500
assert "Tuʻi Haʻatakalaua" not in active_1500
assert "Tuʻi Kanokupolu" not in active_1500
assert {"Tuʻi Haʻatakalaua", "Tuʻi Kanokupolu"} <= names
assert "Maghrebi sultanates" not in names
assert "Hausa city-states" not in names
assert "Maya states" not in names
print(f"valid: {len(polities)} polities, {len(active_1500)} active in 1500")
