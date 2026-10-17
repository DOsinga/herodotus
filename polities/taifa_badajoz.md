---
id: taifa_badajoz
description: >-
  The Taifa of Badajoz was a Muslim kingdom in western Iberia, governing parts of
  present day Spain and Portugal from 1009 to 1094 and again from 1144 to 1150. Its
  capital was Badajoz, and its lands once included Mérida and Lisbon. Sabur, a
  former official of the Cordoban caliphate, founded it during that state's
  fragmentation. His vizier Abdallah ibn al-Aftas established the Aftasid ruling
  dynasty. The kingdom faced pressure from Seville and the expanding Christian
  kingdoms, paying tribute to León while retaining its own rulers. Its armies joined
  the Almoravids at Sagrajas in 1086, but their allies later conquered it in 1094.
  Local rule briefly returned after Almoravid power weakened. Almohad conquest ended
  the taifa and local rule in 1150.
name: "Taifa of Badajoz"
wikipedia: https://en.wikipedia.org/wiki/Taifa_of_Badajoz
periods:
- start: 1009
  end: 1094
- start: 1144
  end: 1150
point:
  name: "Badajoz"
  latitude: 38.8794
  longitude: -6.9707
colors:
  1009: "#51cd66"
  1119: "#51cd66"
  1144: "#278647"
note: "The second period records the restored local government after Almoravid rule, ending with Almohad conquest. Tribute to León did not end the first period."
transitions:
- year: 1009
  kind: broke_away_from
  from: [caliphate_cordoba]
- year: 1094
  kind: absorbed_into
  into: [almoravid_emirate]
- year: 1144
  kind: broke_away_from
  from: [almoravid_emirate]
- year: 1150
  kind: absorbed_into
  into: [almohad_caliphate]
---
