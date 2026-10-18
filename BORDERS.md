# Borders

The polity files give a continuous history of who governed, with one point per
polity. This document describes how we get from there to territory on the
map. There are three phases. Phase one is being built; the other two are
plans.

## Phase one: places and influence

A second set of records, one file per place in `places/`, says which polity
controlled a town in which years:

```markdown
---
id: milan
name: Milan
wikipedia: https://en.wikipedia.org/wiki/Milan
point:
  latitude: 45.4642
  longitude: 9.19
control:
- start: 1250
  end: 1395
  polity: commune_milan
  importance: 3
- start: 1395
  end: 1447
  polity: duchy_milan
  importance: 4
---
```

- `name` is the place's Wikipedia title and `wikipedia` its English article.
  Both are unique.
- `control` spans are inclusive, in order and do not overlap. The polity must
  be active for the whole span, and it cannot be an archaeological culture.
  `end: null` is allowed on the last span when the polity still exists.
- Someone almost always governed a town. A gap between spans of more than 25
  years fails the validator, so a town gets a span for every polity that
  held it, and a governor without a record gets one: a commune, a count or a
  chief who held the town for decades matters enough to add. Shorter gaps
  are allowed for a sack, a civil war or a changeover nobody can date. Where
  nobody governed the town for longer, because it lay abandoned or in a
  long anarchy, say so with an ungoverned span, which casts no influence:

  ```yaml
  - start: 1150
    end: 1590
    ungoverned: Abandoned after the Seljuk sack until Shah Abbas refounded it.
  ```

  `python gaps.py` lists the gaps that are too long.
- Control follows the same who-governed test as the polity records in
  [AGENTS.md](AGENTS.md#who-was-in-control). A town in a vassal state belongs
  to the vassal while the vassal counts as active, not to its overlord.
- When a place changed hands in a year that two polities share, give that
  year to the newcomer and end the previous span the year before.
- An occupation that held a town for a while without ending the polity
  that lost it is still a span of the occupier: Philadelphia is British in
  1777, Puebla American in 1847, Bornholm Soviet in 1945, even though the
  United States, Mexico and Denmark stay active. The same changeover rule
  applies, so the occupier gets the year it took the town and the original
  holder the year it got it back. A state set up by the occupier counts as
  the occupier, as with Joseph Bonaparte's Spain or Axis-held Tunisia.
- Control means governing the town, not holding a title over it. A national
  ruler without real authority there does not get the town: Delhi goes to
  the Marathas from 1771, not to the Mughal emperor they protected, and
  Japanese towns between the Ōnin War and their submission to Hideyoshi go
  to the daimyo who held them rather than to Ashikaga or Oda–Toyotomi.
- Changing a polity's periods can invalidate the places that refer to it.
  The validator reports them; fix them in the same change.
- `importance` sets how far the place's influence reaches, from 1 to 4:
  1. a border fort or small town, placed to pin a border;
  2. a town;
  3. a city or regional seat;
  4. the capital of a large state or one of its great cities.

  Importance belongs to the span, not the place: Nijmegen as a legionary
  base matters more than Nijmegen as a Frankish town, and a capital that the
  court left drops a level.
- A span can follow another place instead of naming a polity:

  ```yaml
  - start: 1384
    end: 1798
    follows: bern
    importance: 1
  ```

  Thun then belongs to whoever holds Bern in each of those years. Use it for towns that went wherever their regional centre
  went. The followed place's own spans must name polities.

The map turns the places into territory with a flood fill over a land grid.
Each place active in the year spreads over land from its point, and its
influence falls off exponentially with the distance travelled; higher
importance falls off more slowly. Each cell goes to the place with the
strongest influence there, and takes that place's polity's colour. The fill
never crosses the sea.

The strongest single place wins, rather than the sum of a polity's places. A
sum would let the polity with more towns push its border outward, so Rome
would reach deep into Batavian land. With the strongest place winning, every
place holds the ground around itself, and a row of small forts holds a line
against a big city behind it. Where a border comes out wrong, the fix is to
add the towns that held it.

Inside a sparse empire the strongest single town can leave holes between
towns of the same polity. So each cell also adds up the influence of the
winning polity's towns and subtracts that of everyone else, and keeps that
support when it beats the strongest town. Where only one polity reaches,
its towns' faint overlaps add up and close the hole; where a rival reaches
too, the subtraction keeps the strongest-town rule in charge, so border
towns still decide borders. Towns therefore spread a little further than
the visible edge, down to an influence of 0.04, so faint overlaps exist to
be added.

Old polities fade towards their edges, since their reach thinned out with
distance. From about 1500 to 1800 the fade sharpens, and modern polities are
coloured right up to where a neighbour takes over.

Islands follow from the no-sea rule. An island with one place gets that
place's control history; an island with several is divided between them like
any other land. A small island needs its own place to be coloured at all.

The grid is 0.25° of longitude, about 18 km wide in northern Europe. A cell
counts as land when at least half of it is, and a step may only pass through
land cells, so the Channel and the Strait of Gibraltar separate. Straits
narrower than a cell, such as the Bosporus, the Øresund and the Strait of
Messina, do not. Each place starts from its true position rather than the
centre of its cell, so neighbouring towns like Kinshasa and Brazzaville
divide their surroundings instead of one taking both.

### Seeding

The first places come from the polity points. A polity's point is its seat,
so the point's town is controlled by that polity during its periods.
Polities whose points lie within 3 km of each other share a place, named
after the town's Wikipedia article. Points that name a region rather than a
town, such as steppe khaganates, have no place yet.

Where two polities claim the same seat in the same years, the one in its
shorter period wins, which picks the local ruler over a wider state: the
Emirate of Tbilisi over the Kingdom of Georgia until 1122, the State of
Buenos Aires over Argentina. A polity that took the seat by a transition
from another polity at the same place only holds it from that year, so Rome
is papal until Italy's capture of 1870. In a changeover year the polity that
continues wins. A few cases were set by hand: Hanoi under the Mạc, the
Toucouleur conquest of Ségou, and Cairo from the Fatimid conquest of 969.
Vatican City has no place; its dot sits inside Rome.

These seed spans have importance 3, or 2 for a chiefdom, and need review:
the capital of an empire deserves 4, and a polity point is not always the
seat for all of the polity's periods. Further spans and towns are
researched, starting with Europe from 1000 to 1500.

Transitions hint at the next holder of a town, but are not used to fill in
spans automatically: chaining them goes wrong within a hop or two, as when a
city absorbed by Spain would stay Spanish after Spain lost it.

### Researching places

Places are researched in batches of about ten neighbouring polities, one
batch after another, so that each batch builds on the places that exist.
Batches only run side by side in regions far enough apart that they cannot
touch the same towns.

For each polity in the batch, collect:

- its capital and major cities, at importance 3 or 4;
- enough towns that no part of its core lies more than about 100 km from a
  place, at importance 2;
- towns where it met a neighbour, at importance 1, so the border falls in
  the right place. A border town is also the place to record a frontier that
  moved: the town changes hands, and the border moves with it.

Before adding a town, look for an existing place: same Wikipedia article, or
a point within a few kilometres. The validator rejects a second file with
the same link. When the place exists, check its history and extend it; do
not start a new one.

A new place gets its whole history, not just the span under the polity being
researched. Walk through the polity records that governed the area, from the
earliest to the present, and give the town to each one for the years it
actually governed it, using the who-governed test, and start the first span
no earlier than the town's founding. Use `follows` for a town that simply went
with its regional centre. When the town's real governor has no polity record,
such as a free city or a local dynasty, add the polity, with the usual
description and transitions, in the same batch.

A batch is done when every polity in it has places for all of its active
years and the map on staging looks plausible for the region. List the
polities that still have no place in a given year with:

```bash
python coverage.py 1250 1500
```

### Drafting histories

`draft.py` turns a list of segments into control spans. Each segment is a
range of years, the candidate polities in order of preference and an
importance; for every year the first candidate that is active wins, so a
segment can run straight through a series of partitions:

```python
import draft
from draft import spans, follows, roman, burgundy, FRANCE

draft.write("dole", "Dole", "Dole, Jura", 47.0925, 5.4897, spans([
    (1384, 1476, ["burgundian_state"], 2),
    (1556, 1673, ["spanish_monarchy"], 2),
    (1674, None, FRANCE, 2),
]), note="The county of Burgundy before Valois rule in 1384 has no record.")
```

It also holds shared sequences, such as the Frankish kingdoms of Burgundy,
the kingdoms of Italy before 1100 and the French and German regimes since
1789. Add to them when a region has a sequence many towns share. The script
only drafts: check its output against the history, commit the place files,
and edit those files directly afterwards rather than regenerating them.

### Coverage plan

Coverage is built in two passes over the whole world.

1. Breadth. Every polity gets places for all of its active years, so
   `coverage.py` reports none missing, and large states get their regional
   centres at importance 3, so that empires come out the right size. Steppe
   powers get their real seats, such as Sarai or Karakorum.
2. Depth. Border towns, satellite towns using `follows`, and enough density
   for borders to fall in the right place, region by region.

Each region below is claimed by one agent at a time. Put your branch next to
a region before starting and clear it when the work is merged. Regions next
to each other share border towns; agree on them in the later batch rather
than editing a place another open branch has touched.

| Region | Pass 1 | Pass 2 |
|---|---|---|
| Switzerland and the western Alps | done (#33) | done (#33) |
| British Isles | done (#34) | |
| Scandinavia and the Baltic | done (#35) | |
| The Americas | done (#36) | |
| Iberia and the Maghreb | done (#37) | |
| South Asia | done (#38) | |
| East Asia | done (#39) | |
| France and the Low Countries | dmo/places-france | |
| Germany and Central Europe | dmo/places-germany | |
| Italy and the Balkans | dmo/places-italy-balkans | |
| Russia and the steppe | dmo/places-russia | |
| Anatolia, the Levant, Egypt and Arabia | dmo/places-levant | |
| Iran, Mesopotamia, the Caucasus and Central Asia | dmo/places-iran | |
| Southeast Asia | dmo/places-southeast-asia | |
| Sub-Saharan Africa | dmo/places-africa | |
| Oceania | dmo/places-oceania | |

### Colours

A polity file can give its colour at one or more years:

```yaml
colors:
  1636: "#cd51b8"
  1735: "#cd51b8"
  1760: "#5151cd"
```

The year endpoint interpolates between them, so a colour can drift slowly
over a polity's life; before the first year and after the last the nearest
colour holds. A polity without `colors` falls back to a colour hashed from
its id. No single colour per polity can contrast with every neighbour
across all of history, which is why the drift is allowed.

`colors.py` proposes the colours. It walks through history in 25-year steps
and at every period start, treats two polities as neighbours when any of
their places or points lie within 400 km, and picks from 36 hues at three
lightness levels. A successor (`succeeded_by`, `merged_into`, `split_into`)
keeps its predecessor's colour when that still contrasts with its
neighbours; any other new polity takes the colour that stands furthest from
its neighbours'. When two neighbours clash, the younger one moves, at most
once a century, and the change is written as a drift over 25 years.
Compared with hashed colours it cuts clashes between neighbours from about
11,000 to about 350 across the sample years.

```bash
python colors.py          # report only
python colors.py --write  # write colors into every polity file
```

Rerun it with `--write` after adding polities or places. The output is data:
commit it, and adjust a colour by hand where the script chose badly.

## Phase two: barriers

Borders can be added as barriers in the same flood fill. The sea is already a
barrier the fill cannot cross.

A hard border is a line with the years it applies, in its own file:

```yaml
---
id: france_germany_1871
name: Frankfurt treaty line
periods:
- {start: 1871, end: 1918}
- {start: 1940, end: 1944}
line: [[6.13, 49.46], [6.73, 49.16], [7.06, 48.52], [7.17, 47.49]]
---
```

The line does not say which polity is on which side. The places decide who
owns what and the line decides where it stops, so the two cannot contradict
each other. A line that does not close a loop lets influence flow around its
ends, so a partial border still improves the map locally: the Rhine can go in
without the whole Franco-German border. A border that moved gets a segment
per course, each with its own periods.

Rivers and mountains are softer barriers. Crossing one adds to the distance
travelled instead of blocking it. A barrier pulls in any border within half
its cost: two equal towns either side of a river that costs 60 km to cross
will meet on the river if the midpoint between them lies within 30 km of it.

- Rivers cost according to their size, from Natural Earth's river ranks. The
  cost applies to crossing a river, not to following it, so valleys like
  the Nile stay whole.
- Mountains cost according to the slope from an elevation grid. Passes then
  come for free, and Tyrol can straddle the Brenner while the main Alpine
  ridge still divides.

Everything becomes one cost per step between cells: sea and active hard
borders are impassable, rivers and slopes add a cost, and the rest is plain
distance. Only the hard borders change with the year.

Costs set too high would make every border follow a river, including where
history did not. Places override geography: a Frankish town on the right bank
of the Rhine holds its own ground whatever the river costs.

The fill also gives a consistency check. Every place should end up inside the
territory of the polity that controls it; one that does not points at a
missing town or barrier.

## Phase three: precise modern borders

Precise borders only exist for modern times. Natural Earth's boundary lines
cover the present, and CShapes 2.0 has dated country borders from 1886 to
2019 (its licence is non-commercial share-alike, which needs checking).
Treaty lines before that are researched by hand.

With hard borders as barriers, the fill can be turned into polygons whose
edges are exactly the border lines where they exist, and the grid only
decides what lies behind them.
