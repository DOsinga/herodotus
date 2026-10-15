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
  A gap means no polity we track governed the place, and it casts no
  influence in those years. `end: null` is allowed on the last span when the
  polity still exists.
- Control follows the same who-governed test as the polity records in
  [AGENTS.md](AGENTS.md#who-was-in-control). A town in a vassal state belongs
  to the vassal while the vassal counts as active, not to its overlord.
- When a place changed hands in a year that two polities share, give that
  year to the newcomer and end the previous span the year before.
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
