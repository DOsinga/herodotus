---
id: palmyrene_empire
name: "Palmyrene Empire"
description: >-
  The Palmyrene Empire was a short-lived regional monarchy that separated from Rome
  during the third century crisis, ruling much of the eastern Mediterranean between 270
  and 273. Its centre was Palmyra, a wealthy caravan city in present day Syria. Queen
  Zenobia governed for her young son Vaballathus after the death of Odaenathus, who had
  defended the Roman East as an imperial ally. Her armies occupied Egypt and extended
  Palmyrene control into Asia Minor while initially retaining signs of loyalty to Rome.
  The adoption of imperial titles made the rivalry explicit. Emperor Aurelian defeated
  Palmyrene armies and captured Zenobia in 272. A renewed uprising at Palmyra in 273
  brought further Roman intervention and destruction, closing the city's brief bid for
  empire.
wikipedia: https://en.wikipedia.org/wiki/Palmyrene_Empire
periods:
- start: 270
  end: 273
point:
  name: "Palmyra"
  latitude: 34.5514
  longitude: 38.2681
colors:
  270: "#572786"
note: "Odaenathus already governed the Roman East from Palmyra in the 260s as Rome's ally; the record starts with Zenobia's break with Rome and conquest of Egypt in 270."
transitions:
- year: 270
  kind: broke_away_from
  from: [roman_empire]
- year: 273
  kind: absorbed_into
  into: [roman_empire]
---
