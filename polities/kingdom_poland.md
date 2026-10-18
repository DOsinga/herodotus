---
id: kingdom_poland
description: >-
  The Kingdom of Poland began with Bolesław I's coronation in 1025, giving
  royal status to the Piast state in central Europe. Early kings balanced
  territorial expansion with struggles against neighbouring powers and powerful local elites. Bolesław
  III's division of his lands in 1138 produced separately governed duchies rather
  than a united monarchy. Władysław the Elbow-high restored the crown in 1320,
  with Kraków becoming the principal royal centre. Later rulers strengthened towns, law,
  and royal administration, while the nobility gained privileges and influence in parliament.
  The Jagiellonian kings joined Poland to Lithuania through shared rulers, but both
  retained separate government. The Union of Lublin in 1569 created the Polish
  Lithuanian Commonwealth, replacing that arrangement with a common state and joint parliament.
name: Kingdom of Poland
wikipedia: https://en.wikipedia.org/wiki/Kingdom_of_Poland
periods:
- start: 1025
  end: 1138
- start: 1320
  end: 1569
point:
  name: Kraków
  latitude: 50.0614
  longitude: 19.9366
colors:
  1025: "#278657"
  1508: "#278657"
  1533: "#862727"
note: "Starts with Bolesław I's coronation in 1025. Bolesław III's testament divided Poland among his sons in 1138, and the Piast duchies governed separately until Władysław the Elbow-high was crowned in 1320; the main duchies have their own records."
transitions:
- year: 1138
  kind: split_into
  into: [duchy_greater_poland, duchy_krakow, duchy_masovia, duchy_silesia]
- year: 1569
  kind: merged_into
  into: [polish_lithuanian_commonwealth]
---
