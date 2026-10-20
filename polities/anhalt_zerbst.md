---
id: anhalt_zerbst
name: "Anhalt-Zerbst"
wikipedia: https://en.wikipedia.org/wiki/Principality_of_Anhalt-Zerbst
description: >-
  Anhalt-Zerbst was a principality in Germany, with medieval Zerbst lines from 1252 to 1396 and
  from 1544 to 1570, and the principality of 1603 until its ruling line ended in 1793. Ascanian
  princes governed from Zerbst within the Holy Roman Empire, sharing a dynastic background with
  neighboring Anhalt states. The principality adopted Reformed religion before returning to
  Lutheranism in 1644. Later inheritance brought the distant lordship of Jever, while further
  family partitions created smaller branches. Its best-known family member was Sophie Auguste
  Fredericka, who married the Russian heir and became Catherine the Great. Prussian occupation
  during the Seven Years' War drove the prince's household into exile. After Frederick Augustus
  died without an heir, the core lands were divided among Anhalt-Dessau, Anhalt-Bernburg, and
  Anhalt-Köthen, with Dessau receiving the largest share.
periods:
- start: 1252
  end: 1396
- start: 1544
  end: 1570
- start: 1603
  end: 1793
point:
  name: "Zerbst"
  latitude: 51.966
  longitude: 12.084
colors:
  1252: "#cd5166"
  1371: "#cd5166"
  1396: "#b234b2"
  1519: "#b234b2"
  1544: "#8834b2"
  1619: "#8834b2"
  1644: "#b8cd51"
note: "Three periods: the medieval line from the 1252 division, whose lands its princes divided in 1396 into Köthen and Dessau; the principality of 1544–1570, whose prince Joachim Ernest reunited Anhalt; and the principality of the 1603 division. The home of Catherine the Great's family. When its line died out in 1793 it was divided among Dessau, Bernburg and Köthen; linked to Dessau, which took the largest share."
transitions:
- year: 1396
  kind: split_into
  into: [anhalt_kothen, anhalt_dessau]
- year: 1544
  kind: broke_away_from
  from: [anhalt_dessau]
- year: 1570
  kind: merged_into
  into: [anhalt]
- year: 1793
  kind: absorbed_into
  into: [anhalt_dessau]
---
