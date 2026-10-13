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
  exists. When no article covers the polity, link the closest one, such as
  the country's history or the period, and say so in the note.
- `periods` is a list of integer years, inclusive at both ends, with negative
  years for BCE. Periods within one polity are in order and must not overlap.
  A polity is active in year Y when `start <= Y` and its period has no end or
  `Y <= end`.
  Different polities can share a changeover year.
- The last period's `end` is `null` for a polity that still exists.
- `point` is a representative place, normally the capital or seat of
  government, with its name. It is a marker for the polity, not a claim about
  its territory. The dots exist for debugging, so two polities sharing a
  point, such as Ming and Qing at Beijing from 1636 to 1644, is fine.
- `note` is optional text shown on the polity's card. Use it whenever a date
  or the point is an estimate, and say what the estimate rests on so it can be
  revisited. An estimated polity with a note is better than an empty region.

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

The test is who actually governed: whether the state's own ruler and
government ran its affairs and made its decisions, or the outside power did.
Succession is evidence but does not settle it either way. A ruler who
inherits a title but has no say is not in control, and a ruler whom an
overlord confirmed or chose can still govern.

- A state that kept governing itself stays active, even if it paid tribute,
  sent troops to its overlord's wars, or had its ruler confirmed or picked by
  the overlord from the local dynasty. Crimea, whose khans the Ottoman sultan
  appointed from 1524 but who fought their own wars, Ragusa, Mewar after its
  1615 treaty with the Mughals, and Milan or Savoy inside the Holy Roman
  Empire stay on the map.
- A protected or princely state is absorbed from the treaty that handed its
  war and foreign relations to the protecting power, whether a
  protectorate, paramountcy or subsidiary alliance, even though its ruler
  kept governing at home. Unlike Crimea, it could not fight or negotiate on
  its own account. The Indian princely states, the Gulf states before
  independence, Zanzibar, Buganda, Tonga from 1900 to 1970 and the Javanese
  courts under the Dutch fall here.
- Once the outside power ruled directly, or through a governor, viceroy or
  other official of its own, the polity has been absorbed and its period
  ends. Naples and Sicily under the Spanish crown and Frisia after Maximilian
  appointed Albert of Saxony in 1498 end there, even though they kept their
  own laws and estates.
- An occupation that took control away for some years is a gap between
  periods, as with Genoa under French or Milanese rule.

Sharing a monarch does not by itself combine polities. A personal union can
leave each polity governing its own affairs; the monarch's nationality or
residence does not decide this. Keep them separate while they governed
separately. If one state took control and governed the other through its
appointed governors or viceroys, the latter's independent period ends.
Separate titles, laws or estates alone do not show separate government.
Apply this rule consistently to personal unions, not just to selected cases.

This stays a judgement call. When the evidence points both ways, choose one,
and do not invent an intermediate category.

Overlordship itself is not recorded. A loose umbrella such as the Holy Roman
Empire is therefore not a polity on the map; its members are. The Empire is a
polity only from 962 to 1250, while the emperors still appointed and removed
the German dukes. From Frederick II's death the princes, bishops and free
cities governed their own lands, and each has its own record until it was
absorbed, mediatised or became one of the nineteenth-century German states.

## Transitions

Polities are connected by what happened when one ended. A transition is
stored once, on the polity that ends; the other direction ("formed from",
"absorbed") is derived from it and never written down. The exception is a
breakaway, where nothing ends: it is stored on the polity that began.

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
- `broke_away_from`: stored on the new polity, which left a polity that
  carried on. It uses `from` instead of `into`:

  ```yaml
  transitions:
  - year: 1581
    kind: broke_away_from
    from: [spanish_monarchy]
  ```

Keep the historical years inclusive. If one polity ended and its replacement
began in the same year, use that year for both; do not subtract a year from
the outgoing polity's end just to avoid an overlap. The one exception is a
change at midnight on 31 December: the outgoing polity ends in that year
and its successor starts in the next, as Czechoslovakia did in 1992–1993.

When building a map for a year, the builder must use the transition and
historical evidence to choose one polity for each place in a shared changeover
year. A shared boundary year does not mean both ruled that place at the same
time. Make the map's choice explicit without changing the historical dates
in the polity records.

`database.py` checks that:

- `year` is the end of one of the polity's periods, or the start of one for
  `broke_away_from`. That includes a period followed by a gap, as with Genoa
  above: the transition says who took over during the gap.
- `into` lists at least two polities for `split_into`, and `into` or `from`
  lists exactly one for the other kinds. Each of them exists.
- An `absorbed_into` or `broke_away_from` target is active in that year. Any
  other target begins a period in that same year, following the inclusive
  changeover rule above, or in the next year for a change that took effect
  at midnight on 31 December, such as the split of Czechoslovakia.

Transitions are optional. A polity that simply disappeared has none, and most
files have not been given theirs yet.

## Checks

```bash
python validate.py
```

It loads every file, applies the rules above plus a few assertions about the
1500 view, and prints the number of polities active in 1500. Run it before
committing any change to `polities/`.
