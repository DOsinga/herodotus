from database import load_polities


polities = load_polities()
names = {polity["name"] for polity in polities}


def active_names(year):
    return {
        polity["name"]
        for polity in polities
        if any(period["start"] <= year <= period["end"] for period in polity["periods"])
    }


active_1500 = active_names(1500)
assert "Kingdom of Portugal" in active_1500
assert "Old Swiss Confederacy" in active_1500
assert "Habsburg Netherlands" in active_1500
assert {"Wattasid Sultanate", "Zayyanid Kingdom of Tlemcen", "Hafsid Sultanate"} <= active_1500
assert {"Lordship of Ireland", "Kingdom of Tyrone", "Tyrconnell", "Kingdom of Thomond"} <= active_1500
assert "Kingdom of Sicily" not in active_1500
assert "Maghrebi sultanates" not in names
assert "Hausa city-states" not in names
assert "Maya states" not in names

vanished_before_1500 = {
    "Bahmani Sultanate",
    "Beylik of Aydın",
    "Beylik of Candar",
    "Beylik of Germiyan",
    "Beylik of Karaman",
    "Beylik of Menteshe",
    "Beylik of Saruhan",
    "Beylik of Teke",
    "Burgundian State",
    "Byzantine Empire",
    "Chūzan",
    "Crown of Aragon",
    "Crown of Castile",
    "Emirate of Granada",
    "Empire of Trebizond",
    "Hokuzan",
    "Hồ dynasty",
    "Jalayirid Sultanate",
    "Jaunpur Sultanate",
    "Khmer Empire",
    "Kingdom of Bosnia",
    "Kingdom of Chimor",
    "Kingdom of Cusco",
    "Kingdom of Cyprus",
    "Kingdom of Gampola",
    "League of Lezhë",
    "League of Mayapan",
    "Marinid Sultanate",
    "Nanzan",
    "Novgorod Republic",
    "Principality of Smolensk",
    "Principality of Theodoro",
    "Principality of Tver",
    "Qara Qoyunlu",
    "Rasulid Sultanate",
    "Reddi Kingdom",
    "Serbian Despotate",
    "Sultanate of Ifat",
    "Tepanec Empire",
    "Tlatelolco",
    "Zeta under the Balšići",
    "Zeta under the Crnojevići",
}
assert vanished_before_1500.isdisjoint(active_1500)
assert all(
    any(name in active_names(year) for year in range(1400, 1500))
    for name in vanished_before_1500
)

assert {"Crown of Aragon", "Crown of Castile"} <= active_names(1478)
assert {"Crown of Aragon", "Crown of Castile"}.isdisjoint(active_names(1479))
assert "Spanish Monarchy" in active_names(1479)
assert "Burgundian State" in active_names(1481)
assert "Burgundian State" not in active_names(1482)
assert "Habsburg Netherlands" in active_names(1482)
assert "Kingdom of Cusco" in active_names(1437)
assert "Kingdom of Cusco" not in active_names(1438)
assert "Inca Empire" in active_names(1438)
assert "Khmer Empire" in active_names(1430)
assert "Khmer Empire" not in active_names(1431)
assert "Kingdom of Cambodia" in active_names(1431)

print(f"valid: {len(polities)} polities, {len(active_1500)} active in 1500")
