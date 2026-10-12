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
        "Beylik of Germiyan",
        "Beylik of Menteshe",
        "Beylik of Saruhan",
        "Beylik of Teke",
        "Beylik of Aydın",
        "Beylik of Candar",
        "Beylik of Karaman",
        "Burgundian State",
        "Byzantine Empire",
        "Crown of Aragon",
        "Crown of Castile",
        "Emirate of Granada",
        "Empire of Trebizond",
        "Jalayirid Sultanate",
        "Jaunpur Sultanate",
        "Khmer Empire",
        "Kingdom of Bosnia",
        "Kingdom of Chimor",
        "Kingdom of Cusco",
        "Kingdom of Cyprus",
        "Kingdom of Gampola",
        "League of Mayapan",
        "Marinid Sultanate",
        "Novgorod Republic",
        "Principality of Theodoro",
        "Principality of Tver",
        "Qara Qoyunlu",
        "Rasulid Sultanate",
        "Serbian Despotate",
        "Sultanate of Ifat",
        "Tepanec Empire",
        "Tlatelolco",
        "Zeta under the Crnojevići",
        "Hồ dynasty",
        "Hokuzan",
        "Chūzan",
        "League of Lezhë",
        "Nanzan",
        "Principality of Smolensk",
        "Reddi Kingdom",
        "Zeta under the Balšići",
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
