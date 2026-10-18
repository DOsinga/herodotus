---
id: duchy_masovia
name: "Duchy of Masovia"
wikipedia: https://en.wikipedia.org/wiki/Duchy_of_Masovia
description: >-
  The Duchy of Masovia emerged in northeastern Poland when Bolesław III's testament divided
  his lands in 1138. Bolesław IV received Masovia and neighboring Kuyavia, governing as a
  Piast duke. Płock was an royal and ecclesiastical center beside the Vistula. Later dukes
  competed for influence within fragmented Poland and defended borders against neighboring
  peoples. Konrad I invited the Teutonic Order to fight the Prussians, a decision with
  lasting regional consequences. Kuyavia separated in 1233. Repeated family partitions
  subsequently produced distinct Masovian duchies, including Płock and Czersk. This record
  follows the united government only, with reunifications in 1294 and 1370 between separate
  periods. Siemowit III's lands were divided again in 1381, after which the shares are
  represented by their own records here.
periods:
- start: 1138
  end: 1275
- start: 1294
  end: 1310
- start: 1370
  end: 1381
point:
  name: "Płock"
  latitude: 52.55
  longitude: 19.7
colors:
  1138: "#cd7a51"
  1345: "#cd7a51"
  1370: "#672786"
note: "Bolesław IV's share of the 1138 testament; Kuyavia split off in 1233. The gaps are the partitions between the Płock, Czersk and Rawa lines in 1275–1294 and from 1310, and from 1381 for good. Siemowit III reunited Masovia in 1370, when Płock came back to him from the Polish crown."
transitions:
- year: 1275
  kind: split_into
  into: [duchy_czersk, duchy_plock]
- year: 1310
  kind: split_into
  into: [duchy_czersk, duchy_plock]
- year: 1381
  kind: split_into
  into: [duchy_czersk, duchy_plock, duchy_rawa]
---
