# Herodotus

A browser for historical polities: pick a year and see which polities existed,
each shown as one dot. The project is rendered inside douwe.com as
`projects/herodotus`, but the data and browser code live in this repository.

## Layout

```
polities/<id>.md     one file per polity; the canonical data
database.py          loads and validates the polity files
validate.py          runs the checks; use it after every data change
herodotus.py         douwe.com Project subclass; embeds the data in the page
herodotus.html       info block + page template
static/atlas.js      Leaflet map, year slider, search
static/land-50m.geojson  Natural Earth 1:50m land
```

There is no database, import step or generated file. The page loads every
polity file on each request, so a data edit shows up on reload.

## Polity files

A polity file is YAML frontmatter with nothing after it:

```markdown
---
id: republic_genoa
name: Republic of Genoa
wikipedia: https://en.wikipedia.org/wiki/Republic_of_Genoa
periods:
- start: 1339
  end: 1396
- start: 1409
  end: 1421
point:
  name: Genoa
  latitude: 44.4056
  longitude: 8.9463
transitions:
- year: 1396
  kind: absorbed_into
  into: [kingdom_france]
- year: 1421
  kind: absorbed_into
  into: [duchy_milan]
---
```

`transitions` is optional and described [below](#transitions).

`database.py` enforces these rules:

- `id` is lowercase snake case, matches the filename and never changes once
  other data refers to it.
- `name` is the conventional English name and is unique.
- `wikipedia` is an English Wikipedia URL for the polity itself. Avoid
  articles about a dynasty or an institution when a page about the state
  exists.
- `periods` is a list of integer years, inclusive at both ends, with negative
  years for BCE. Periods are in order and must not overlap. A polity is active
  in year Y when `start <= Y <= end` for one of its periods.
- `end` is required, so a polity that still exists cannot be represented yet.
- `point` is a representative place, normally the capital or seat of
  government, with its name. It is a marker for the polity, not a claim about
  its territory.

## What counts as a polity

One file describes one political entity that historians treat as acting in its
own right, such as a kingdom, sultanate, republic, city-state or confederacy.

- Do not create group records such as "Maya states" or "Hausa city-states".
  Add the individual polities instead.
- A dynasty is not a polity. Use the state's name unless the dynasty name is
  the conventional name for the state (Ming dynasty, Joseon).
- When a polity changes character enough that historians treat it as a new
  state, it gets a new file rather than another period.
- A gap between periods means the polity did not exist as its own entity in
  those years, for example Genoa under French or Milanese rule.

Coverage is built outward from 1500, by hand. Do not bulk-import from
Wikidata or another list: that approach was tried and produced thousands of
duplicates, placeholder dates and anachronistic identities.

## Who was in control

A polity is active while it was actually in power and in control of its own
affairs. Legal titles, nominal overlords, claims and tribute do not decide
this; who governed does.

The most useful question is who chose the ruler and who did the ruling:

- A local ruler who came to power through local succession or election and
  made their own decisions keeps the polity active, even if it paid tribute,
  owed troops or acknowledged an emperor. Crimea under the Ottomans, Ragusa,
  and Milan or Savoy inside the Holy Roman Empire stay on the map.
- Once the outside power ruled directly, or through a governor, viceroy or
  other appointee, the polity has been absorbed and its period ends. Naples
  and Sicily under the Spanish crown and Frisia after Maximilian appointed
  Albert of Saxony in 1498 end there, even though they kept their own laws
  and estates.
- An occupation that took control away for some years is a gap between
  periods, as with Genoa under French or Milanese rule.

This stays a judgement call. When the evidence points both ways, choose one,
and do not invent an intermediate category.

Overlordship itself is not recorded. A loose umbrella such as the Holy Roman
Empire is therefore not a polity on the map; its members are.

Several existing files predate this rule. Wallachia and Moldavia end when they
began paying Ottoman tribute, although they kept their own voivodes until the
Ottomans appointed Phanariot princes in the 1710s. The Holy Roman Empire still
has its own file.

## Transitions

Polities are connected by what happened when one ended. A transition is
stored once, on the polity that ends; the other direction ("formed from",
"absorbed") is derived from it and never written down:

```yaml
transitions:
- year: 1479
  kind: merged_into
  into: [spanish_monarchy]
```

`kind` is one of:

- `absorbed_into`: another polity took control, as described above.
- `merged_into`: several polities became one new polity; each of them points
  to it.
- `split_into`: the polity broke up into several new ones.
- `succeeded_by`: the same state continued under a new identity, such as a
  change of regime that warrants a new file.

`database.py` checks that:

- `year` is the end of one of the polity's periods. That includes a period
  followed by a gap, as with Genoa above: the transition says who took over
  during the gap.
- `into` lists at least two polities for `split_into` and exactly one for the
  other kinds, and each of them exists.
- An `absorbed_into` target is active in that year. Any other target begins a
  period in that year or the next.

Transitions are optional. A polity that simply disappeared has none, and most
files have not been given theirs yet.

## Checks

```bash
python validate.py
```

It loads every file, applies the rules above plus a few assertions about the
1500 view, and prints the number of polities active in 1500. Run it before
committing any change to `polities/`.
