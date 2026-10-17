---
id: hammadid_emirate
name: "Hammadid Emirate"
description: >-
  The Hammadid Emirate ruled much of present northern Algeria from 1014 to 1152. Hammad ibn Buluggin,
  a member of the Berber Zirid family, established his own hereditary government and secured Zirid
  recognition in 1017. His fortified capital, Qalat Beni Hammad, became a urban centre with palaces
  and a large mosque. The dynasty changed allegiance between Abbasid and Fatimid caliphs while
  retaining local political control. Pressure from migrating Arab tribes encouraged a shift towards
  the coast, and Bejaia replaced the inland capital around 1090. Its port supported Mediterranean
  trade and an active cultural life. Hammadid rulers competed with Zirid neighbours and other western
  powers, but could not withstand Almohad expansion. The Almohads conquered the emirate in 1152,
  ending the dynasty's government.
wikipedia: https://en.wikipedia.org/wiki/Hammadid_dynasty
periods:
- start: 1014
  end: 1152
point:
  name: "Bejaia"
  latitude: 36.7514
  longitude: 5.0557
colors:
  1014: "#cd5166"
  1090: "#cd5166"
  1115: "#b851cd"
note: "Hammad established his own government in 1014; Zirid recognition followed in 1017. Changing caliphal allegiance did not end local rule. Bejaia became the capital around 1090, replacing Qalat Beni Hammad."
transitions:
- year: 1014
  kind: broke_away_from
  from: [zirid_emirate]
- year: 1152
  kind: absorbed_into
  into: [almohad_caliphate]
---
