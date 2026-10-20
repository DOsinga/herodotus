---
id: gwent_kingdom
name: "Kingdom of Gwent"
description: >-
  Gwent was a Welsh kingdom between the rivers Wye and Usk, emerging after Roman rule ended
  in Britain. Its beginning around 450 is estimated, and its name derives from Venta
  Silurum, the Roman town now called Caerwent. Native kings governed communities with strong
  continuity from the earlier Silures, supported by local courts and Christian churches.
  Gwent's relationship with neighboring Glywysing shifted through dynastic unions and
  divisions. Morgan united them within Morgannwg in 942; separate Gwent returned after his
  death in 974. Gruffudd ap Llywelyn took control in 1055, interrupting its government until
  1063. Norman expansion then dismantled the kingdom, conventionally ending around 1075.
  Smaller Welsh lordships survived longer, but they did not preserve the earlier kingdom as
  one independent government.
wikipedia: https://en.wikipedia.org/wiki/Kingdom_of_Gwent
periods:
- start: 450
  end: 942
- start: 974
  end: 1055
- start: 1063
  end: 1075
point:
  name: "Caerwent"
  latitude: 51.611
  longitude: -2.766
colors:
  450: "#5e34b2"
note: "450 estimates its post-Roman royal government's emergence. Morgan's 942 union placed it within Morgannwg; separate Gwent reappeared after his death in 974. Gruffudd ap Llywelyn's government interrupted it in 1055–1063. The final end around 1075 estimates the Norman conquests, not the survival of smaller Caerleon and Gwynllŵg lordships."
transitions:
- year: 942
  kind: absorbed_into
  into: [glywysing_morgannwg]
- year: 1055
  kind: absorbed_into
  into: [gwynedd]
---
