---
id: saxe_eisenach
name: "Saxe-Eisenach"
wikipedia: https://en.wikipedia.org/wiki/Saxe-Eisenach
description: >-
  Saxe-Eisenach was an Ernestine duchy in western Thuringia, centred on Eisenach below the
  Wartburg castle. It existed three times. First, John Ernest received Eisenach in the division of
  1596 and inherited Coburg in 1633, ruling both until his death in 1638. In 1640 a new division
  of the Weimar lands created a duchy at Eisenach for Albert, which returned to Weimar on his
  death in 1644. A third Saxe-Eisenach began in 1662 for Adolf William and his brothers, and
  lasted under its own dukes until the last of them, William Henry, died in 1741. Its lands then
  passed to Saxe-Weimar, which governed them from Weimar and formally merged the two in 1809.
periods:
- start: 1596
  end: 1638
- start: 1640
  end: 1644
- start: 1662
  end: 1741
point:
  name: "Eisenach"
  latitude: 50.9744
  longitude: 10.3197
colors:
  1596: "#572786"
note: "Three periods, each a separate grant to a branch of the Weimar Ernestines. On John Ernest's death in 1638 his lands were divided between Saxe-Weimar and Saxe-Altenburg."
transitions:
- year: 1596
  kind: broke_away_from
  from: [saxe_coburg_eisenach]
- year: 1638
  kind: absorbed_into
  into: [saxe_altenburg]
- year: 1640
  kind: broke_away_from
  from: [saxe_weimar]
- year: 1644
  kind: absorbed_into
  into: [saxe_weimar]
- year: 1662
  kind: broke_away_from
  from: [saxe_weimar]
- year: 1741
  kind: absorbed_into
  into: [saxe_weimar]
---
