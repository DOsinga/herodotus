# Herodotus

Herodotus is a small browser for historical polities. Move the year slider to
see polities appear and disappear; select a point to see its dates,
description and Wikipedia page.

The canonical data is one Markdown file per polity in `polities/`. Each file
contains a stable internal ID, name, Wikipedia link, a 120-word description,
active periods, and one representative point. There is no Wikidata import or
generated candidate list.

Run the data checks with:

```bash
python validate.py
```

Check description coverage and the map's inspection card with:

```bash
python -m unittest test_database
node test_atlas.js
```

The project is rendered inside douwe.com, but the data and browser code are
self-contained in this directory.
