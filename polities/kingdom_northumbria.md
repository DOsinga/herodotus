---
id: kingdom_northumbria
name: "Kingdom of Northumbria"
wikipedia: https://en.wikipedia.org/wiki/Northumbria
description: >-
  Northumbria was an Anglo-Saxon monarchy joining Bernicia and Deira across northern England
  and parts of southern Scotland. Its first union followed Aethelfrith's conquest around
  604, but separate royal courts returned during seventh century struggles. This record
  follows those interruptions and the reunification conventionally dated 654. Kings such as
  Edwin, Oswald, and Oswiu extended Northumbrian influence while Christianity reshaped royal
  patronage and religious life. Monasteries including Lindisfarne and Wearmouth-Jarrow
  became centres of scholarship, manuscript production, and art. Bamburgh anchored power in
  the north, while York was important in the south. Defeat against the Picts checked
  expansion, and later succession conflicts undermined stability. Viking conquest of York in
  867 divided the kingdom between Scandinavian Jórvík and a surviving northern government at
  Bamburgh.
periods:
- start: 604
  end: 633
- start: 634
  end: 644
- start: 654
  end: 867
point:
  name: "Bamburgh"
  latitude: 55.608
  longitude: -1.709
colors:
  604: "#862737"
  680: "#862737"
  705: "#278627"
note: "The first union of Bernicia and Deira followed Aethelfrith's conquest around 604. Separate courts returned after Edwin's death in 633. Oswald reunited them in 634; this record retains Oswiu's initial inherited union after Oswald's death in 642 until Oswine's separate Deiran court in 644. 654 conventionally marks the lasting reunification. In 867 York passed to Jórvík while a separate northern government survived at Bamburgh."
transitions:
- year: 633
  kind: split_into
  into: [bernicia, deira]
- year: 644
  kind: split_into
  into: [bernicia, deira]
- year: 867
  kind: split_into
  into: [kingdom_jorvik, bamburgh_lordship]
---
