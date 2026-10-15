# Herodotus

Herodotus is a small browser for historical polities. Move the year slider to
see polities appear and disappear; select a point to see its dates,
description and Wikipedia page.

The canonical data is one Markdown file per polity in `polities/`. Each file
contains a stable internal ID, name, Wikipedia link, a 105–130-word description,
active periods, and one representative point. There is no Wikidata import or
generated candidate list.

A second set of files in `places/` records which polity controlled a town in
which years. The map spreads colour outward from those towns to suggest
territory; [BORDERS.md](BORDERS.md) explains how.

Run the data checks with:

```bash
python validate.py
```

The project is rendered inside douwe.com, but the data and browser code are
self-contained in this directory.
