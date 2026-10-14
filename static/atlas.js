(function () {
  const database = JSON.parse(document.getElementById("polity-data").textContent);
  const yearInput = document.getElementById("atlas-year");
  const yearValue = document.getElementById("atlas-year-value");
  const yearMin = document.getElementById("atlas-year-min");
  const yearMid = document.getElementById("atlas-year-mid");
  const yearMax = document.getElementById("atlas-year-max");
  const searchInput = document.getElementById("atlas-search");
  const polityList = document.getElementById("atlas-polities");
  const card = document.getElementById("atlas-card");
  const SLIDER_STEPS = 2000;
  const FILL_OPACITY = { polity: 1, chiefdom: 0.45, culture: 0 };
  const count = document.getElementById("atlas-count");
  const note = document.getElementById("atlas-note");
  const markers = new Map();
  let selectedPolity = null;
  let currentYear = 1500;

  const map = L.map("atlas-map", {
    minZoom: 1,
    maxZoom: 7,
    zoomControl: false,
    worldCopyJump: true
  }).setView([23, 10], 2);
  L.control.zoom({ position: "topright" }).addTo(map);
  map.createPane("land");
  map.getPane("land").style.zIndex = 300;
  const layer = L.layerGroup().addTo(map);
  const territory = createTerritory(map, database.places, polityRgb);
  const landLayer = L.geoJSON(null, {
    pane: "land",
    interactive: false,
    style: { color: "#aca99f", fillColor: "#eeeade", fillOpacity: 1, weight: 0.5 }
  }).addTo(map);
  fetch("/static/projects/herodotus/land-50m.geojson")
    .then(function (response) { return response.json(); })
    .then(function (geojson) {
      landLayer.addData(geojson);
      territory.setLand(geojson);
    });
  map.attributionControl.addAttribution('<a href="https://www.naturalearthdata.com/">Natural Earth</a>');

  function formatYear(year) {
    return year < 0 ? Math.abs(year) + " BCE" : String(year);
  }

  function activePeriod(polity, year) {
    return polity.periods.find(function (period) {
      return period.start <= year && (period.end === null || year <= period.end);
    });
  }

  function polityHue(id) {
    let hash = 0;
    for (let index = 0; index < id.length; index++) {
      hash = ((hash << 5) - hash + id.charCodeAt(index)) | 0;
    }
    return Math.abs(hash) % 360;
  }

  function polityColor(id) {
    return "hsl(" + polityHue(id) + " 55% 43%)";
  }

  function polityRgb(id) {
    const hue = polityHue(id);
    const chroma = 0.55 * 0.43;
    return [0, 8, 4].map(function (offset) {
      const k = (offset + hue / 30) % 12;
      return Math.round(255 * (0.43 - chroma * Math.max(-1, Math.min(k - 3, 9 - k, 1))));
    });
  }

  function escapeHtml(value) {
    return String(value).replace(/[&<>'"]/g, function (character) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", "'": "&#39;", '"': "&quot;" }[character];
    });
  }

  function showCard(polity, year) {
    const isActive = !!activePeriod(polity, year);
    const periods = polity.periods.map(function (period) {
      return formatYear(period.start) + "–" + (period.end === null ? "present" : formatYear(period.end));
    }).join(" · ");
    card.className = "atlas-card" + (isActive ? "" : " is-inactive");
    const status = isActive
      ? ""
      : '<span class="atlas-status">Not active in ' + escapeHtml(formatYear(year)) + "</span>";
    card.innerHTML = "<strong>" + escapeHtml(polity.name) + "</strong>" +
      '<span class="atlas-id">' + escapeHtml(polity.id + (polity.type ? " · " + polity.type : "")) + "</span>" +
      "<span>" + escapeHtml(periods) + "</span>" +
      status +
      "<span>representative point: " + escapeHtml(polity.point.name) + "</span>" +
      "<p>" + escapeHtml(polity.description) + "</p>" +
      (polity.note ? "<p>" + escapeHtml(polity.note) + "</p>" : "") +
      '<p><a href="' + escapeHtml(polity.wikipedia) + '" target="_blank" rel="noopener">Wikipedia</a></p>';
  }

  function resetCard(year) {
    card.className = "atlas-card";
    card.innerHTML = "<strong>Polities in " + formatYear(year) +
      "</strong><span>Click a representative point to inspect the polity and its dates.</span>";
  }

  function selectPolity(polity) {
    selectedPolity = polity;
    showYear(currentYear);
  }

  function showYear(year) {
    currentYear = year;
    territory.show(year);
    layer.clearLayers();
    markers.clear();
    const active = database.polities.filter(function (polity) {
      return activePeriod(polity, year);
    });

    let selectedMarker = null;
    active.forEach(function (polity) {
      const isSelected = selectedPolity && selectedPolity.id === polity.id;
      const color = polityColor(polity.id);
      const marker = L.circleMarker([polity.point.latitude, polity.point.longitude], {
        radius: isSelected ? 9 : 6,
        color: isSelected ? "#20272b" : polity.type ? color : "#fff",
        weight: isSelected ? 3 : polity.type ? 2.5 : 1.5,
        fillColor: color,
        fillOpacity: FILL_OPACITY[polity.type || "polity"]
      }).addTo(layer);
      marker.bindTooltip(polity.name, {
        className: "atlas-tooltip",
        direction: "top",
        offset: [0, isSelected ? -7 : -4]
      });
      marker.on("click", function (event) {
        L.DomEvent.stopPropagation(event);
        selectPolity(polity);
      });
      markers.set(polity.id, marker);
      if (isSelected) {
        selectedMarker = marker;
      }
    });

    if (selectedMarker) {
      selectedMarker.bringToFront();
    }

    yearValue.textContent = formatYear(year);
    if (selectedPolity) {
      showCard(selectedPolity, year);
    } else {
      resetCard(year);
    }
    count.textContent = active.length + " polities";
    note.textContent = "Each dot is one polity's representative point. Half-filled rings are chiefdoms and hollow rings are archaeological cultures. The shading spreads from the towns each polity controlled; it is not a surveyed border.";
  }

  function normalizeSearch(text) {
    return text
      .toLowerCase()
      .normalize("NFD")
      .replace(/[\u0300-\u036f]/g, "")
      .replace(/[\u02bb\u02bc\u2018\u2019\u0060']/g, "");
  }

  function findPolity() {
    const rawQuery = searchInput.value.trim();
    if (!rawQuery) return;
    const query = normalizeSearch(rawQuery.replace(/_/g, " "));
    const polity = database.polities.find(function (candidate) {
      const name = normalizeSearch(candidate.name);
      const id = normalizeSearch(candidate.id.replace(/_/g, " "));
      return id === query || name === query;
    }) || database.polities.find(function (candidate) {
      const name = normalizeSearch(candidate.name);
      const id = normalizeSearch(candidate.id.replace(/_/g, " "));
      return name.startsWith(query) || id.startsWith(query);
    }) || database.polities.find(function (candidate) {
      const name = normalizeSearch(candidate.name);
      const id = normalizeSearch(candidate.id.replace(/_/g, " "));
      return name.includes(query) || id.includes(query);
    });
    if (!polity) {
      selectedPolity = null;
      showYear(currentYear);
      card.className = "atlas-card";
      card.innerHTML = "<strong>No polity found</strong><span>Try another name.</span>";
      return;
    }

    selectedPolity = polity;
    if (!activePeriod(polity, currentYear)) {
      currentYear = polity.periods[0].start;
      yearInput.value = sliderPosition(currentYear);
    }
    showYear(currentYear);
    searchInput.value = polity.name;
    map.flyTo([polity.point.latitude, polity.point.longitude], Math.max(map.getZoom(), 4));
  }

  const bounds = database.polities.reduce(function (accumulator, polity) {
    polity.periods.forEach(function (period) {
      if (period.start < accumulator.min) accumulator.min = period.start;
      const end = period.end === null ? new Date().getFullYear() : period.end;
      if (end > accumulator.max) accumulator.max = end;
    });
    return accumulator;
  }, { min: Infinity, max: -Infinity });

  // The slider is linear in the log of years before a point 500 years after the
  // last year, so deep time is compressed and recent centuries get more room.
  const reference = bounds.max + 500;
  const oldest = Math.log(reference - bounds.min);
  const newest = Math.log(reference - bounds.max);

  function sliderYear(position) {
    return Math.round(reference - Math.exp(oldest + (newest - oldest) * position / SLIDER_STEPS));
  }

  function sliderPosition(year) {
    return Math.round(SLIDER_STEPS * (Math.log(reference - year) - oldest) / (newest - oldest));
  }

  yearInput.min = 0;
  yearInput.max = SLIDER_STEPS;
  yearInput.step = 1;
  yearInput.value = sliderPosition(currentYear);
  yearMin.textContent = formatYear(bounds.min);
  yearMid.textContent = formatYear(sliderYear(SLIDER_STEPS / 2));
  yearMax.textContent = formatYear(bounds.max);

  polityList.replaceChildren.apply(polityList, database.polities.map(function (polity) {
    const option = document.createElement("option");
    option.value = polity.name;
    return option;
  }));

  map.on("click", function () {
    if (selectedPolity) {
      selectedPolity = null;
      showYear(currentYear);
    }
  });

  yearInput.addEventListener("input", function () { showYear(sliderYear(Number(yearInput.value))); });
  searchInput.addEventListener("change", findPolity);
  searchInput.addEventListener("keydown", function (event) {
    if (event.key === "Enter") findPolity();
  });
  showYear(1500);
})();
