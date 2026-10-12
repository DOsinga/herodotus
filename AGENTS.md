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
---
```

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

## Overlords and successors

The model has no relations yet. Nothing records that Milan belonged to the
Holy Roman Empire, that Crimea was an Ottoman vassal or that Castile and
Aragon became the Spanish Monarchy.

Existing files resolve vassalage inconsistently because of this. Wallachia and
Moldavia end when they started paying Ottoman tribute, while the Crimean
Khanate and Ragusa continue as vassals. Sicily and Naples end under Aragonese
and Spanish rule, while the Holy Roman Empire appears next to its own members.
Do not "fix" these period endings one at a time; they will be revisited once
relations exist.

## Checks

```bash
python validate.py
```

It loads every file, applies the rules above plus a few assertions about the
1500 view, and prints the number of polities active in 1500. Run it before
committing any change to `polities/`.
