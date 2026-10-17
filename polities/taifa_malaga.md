---
id: taifa_malaga
description: >-
  The Taifa of Malaga was a Muslim kingdom on the southern coast of Iberia, centred on the
  Mediterranean port of Malaga. Its first period began in 1026 when the Hammudid ruler Yahya
  withdrew from Cordoba and established a separate royal government. His successors retained
  caliphal claims while competing with Seville and neighbouring Granada. Granada absorbed the
  kingdom in 1057, but Malaga recovered separate rule in 1073. The Almoravids conquered it in
  1090. Their later decline allowed another restoration in 1145, which ended under the
  Almohads in 1153. A final independent period began in 1229 during the breakdown of Almohad
  power. Nasrid Granada incorporated Malaga around 1238, or 1239 in some accounts, making the
  coastal city part of its emerging emirate.
name: "Taifa of Málaga"
wikipedia: https://en.wikipedia.org/wiki/Taifa_of_M%C3%A1laga
periods:
- start: 1026
  end: 1057
- start: 1073
  end: 1090
- start: 1145
  end: 1153
- start: 1229
  end: 1238
point:
  name: "Málaga"
  latitude: 36.7213
  longitude: -4.4214
colors:
  1026: "#b234b2"
note: "Granada governed Málaga between the first two periods. The later restorations ended under the Almohads and Nasrid Granada. The final annexation is dated 1238 here; some accounts use 1239."
transitions:
- year: 1057
  kind: absorbed_into
  into: [taifa_granada]
- year: 1073
  kind: broke_away_from
  from: [taifa_granada]
- year: 1090
  kind: absorbed_into
  into: [almoravid_emirate]
- year: 1145
  kind: broke_away_from
  from: [almoravid_emirate]
- year: 1153
  kind: absorbed_into
  into: [almohad_caliphate]
- year: 1229
  kind: broke_away_from
  from: [almohad_caliphate]
- year: 1238
  kind: absorbed_into
  into: [emirate_granada]
---
