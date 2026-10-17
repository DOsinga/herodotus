---
id: byzantine_empire
description: >-
  The Byzantine Empire was the eastern continuation of Rome, governed from
  Constantinople by Christian emperors and a civil administration. This record begins
  with the imperial division of 395, rather than the capital's earlier foundation. Its
  inhabitants called themselves Romans, although Greek gradually became the principal
  language of government. Justinian recovered parts of the western Mediterranean, but
  later wars and Arab conquests greatly reduced imperial territory. The state survived
  through changing military systems, diplomacy, and periods of renewed expansion.
  Constantinople remained a major centre of commerce and Orthodox Christianity.
  Crusaders captured it in 1204, breaking the empire into rival successor states. The
  Nicaean emperors recovered the capital in 1261. A weakened restored empire endured
  until Ottoman conquest of Constantinople in 1453.
name: Byzantine Empire
wikipedia: https://en.wikipedia.org/wiki/Byzantine_Empire
periods:
- start: 395
  end: 1204
- start: 1261
  end: 1453
point:
  name: Constantinople
  latitude: 41.0125
  longitude: 28.98
colors:
  395: "#cd7a51"
  1093: "#cd7a51"
  1118: "#3488b2"
  1236: "#3488b2"
  1261: "#b8cd51"
  1338: "#b8cd51"
  1363: "#a351cd"
note: "Starts with the 395 division of the Roman Empire; Constantinople was founded as the capital in 330, when the Roman Empire record still covers it."
transitions:
- year: 1204
  kind: split_into
  into: [latin_empire, empire_nicaea, empire_trebizond]
- year: 1453
  kind: absorbed_into
  into: [ottoman_empire]
---
