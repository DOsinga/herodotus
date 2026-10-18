---
id: taifa_almeria
name: "Taifa of Almería"
wikipedia: https://en.wikipedia.org/wiki/Taifa_of_Almer%C3%ADa
description: >-
  Almería was a Muslim kingdom on the southeastern coast of Iberia, formed during the
  collapse of Córdoba's caliphate around 1012. Its emirs governed from a fortified port
  whose silk workshops and Mediterranean maritime trade made it wealthy despite its small
  territory. Early rulers such as Khayran expanded the Alcazaba and mosque, while later
  courts attracted poets and scholars. Rival kingdoms repeatedly challenged its position.
  Valencia imposed a governor in 1038, but local rule returned in 1042 under the Banu
  Sumadih family. The Almoravids conquered the taifa in 1091. A later restoration around
  1140 lasted only until Alfonso VII's forces captured Almería in 1147. These separate
  periods record actual local government, not continuous independence throughout the
  city's prosperous medieval commercial history.
periods:
- start: 1012
  end: 1038
- start: 1042
  end: 1091
- start: 1140
  end: 1147
point:
  name: "Almería"
  latitude: 36.8333
  longitude: -2.45
colors:
  1012: "#a351cd"
  1115: "#a351cd"
  1140: "#cd5166"
note: "The first start is an estimate: independence is variously dated 1010 or around 1012. Valencia ruled through its governor in 1038–1042. The later period follows the conventional 1140 restoration date."
transitions:
- year: 1012
  kind: broke_away_from
  from: [caliphate_cordoba]
- year: 1038
  kind: absorbed_into
  into: [taifa_valencia]
- year: 1042
  kind: broke_away_from
  from: [taifa_valencia]
- year: 1091
  kind: absorbed_into
  into: [almoravid_emirate]
- year: 1140
  kind: broke_away_from
  from: [almoravid_emirate]
- year: 1147
  kind: absorbed_into
  into: [kingdom_castile]
---
