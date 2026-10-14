const assert = require("node:assert/strict");
const fs = require("node:fs");
const vm = require("node:vm");

const polity = {
  id: "sample_kingdom",
  name: "Sample kingdom",
  wikipedia: "https://en.wikipedia.org/wiki/Sample",
  periods: [{ start: 1400, end: 1600 }],
  point: { name: "Sample capital", latitude: 10, longitude: 20 },
  description: 'A description with <script>alert("unsafe")</script> & details.',
  note: "A separate note."
};
const nodes = new Map();
function getNode(id) {
  if (!nodes.has(id)) {
    nodes.set(id, {
      value: "",
      textContent: "",
      events: {},
      addEventListener(name, callback) { this.events[name] = callback; },
      replaceChildren() {}
    });
  }
  return nodes.get(id);
}
getNode("polity-data").textContent = JSON.stringify({ polities: [
  polity,
  { ...polity, id: "older_kingdom", name: "Older kingdom", periods: [{ start: 1000, end: 1100 }] }
] });
const mapEvents = {};
const markerEvents = [];
const map = {
  setView() { return this; },
  createPane() {},
  getPane() { return { style: {} }; },
  attributionControl: { addAttribution() {} },
  on(name, callback) { mapEvents[name] = callback; },
  getZoom() { return 2; },
  flyTo() {}
};
const layer = { addTo() { return this; }, clearLayers() {} };
vm.runInNewContext(fs.readFileSync(__dirname + "/static/atlas.js", "utf8"), {
  document: { getElementById: getNode, createElement() { return {}; } },
  fetch: async function () { return { json: async function () { return {}; } }; },
  L: {
    map() { return map; },
    control: { zoom() { return { addTo() {} }; } },
    layerGroup() { return layer; },
    geoJSON() { return { addTo() { return this; }, addData() {} }; },
    circleMarker() {
      return {
        addTo() { return this; },
        bindTooltip() {},
        on(name, callback) { markerEvents.push(callback); },
        bringToFront() {}
      };
    },
    DomEvent: { stopPropagation() {} }
  }
});

markerEvents[0]({});
const card = getNode("atlas-card");
assert.ok(card.innerHTML.includes("A description with &lt;script&gt;"));
assert.ok(card.innerHTML.includes("&amp; details."));
assert.ok(!card.innerHTML.includes("<script>"));
assert.ok(card.innerHTML.indexOf("A description") < card.innerHTML.indexOf("A separate note"));
assert.ok(card.innerHTML.includes("1400–1600"));
assert.ok(card.innerHTML.includes('rel="noopener"'));

getNode("atlas-year").value = "0";
getNode("atlas-year").events.input();
assert.ok(card.innerHTML.includes("A description"));
assert.ok(card.innerHTML.includes("Not active in"));

mapEvents.click();
assert.ok(!card.innerHTML.includes("A description"));
getNode("atlas-search").value = "sample_kingdom";
getNode("atlas-search").events.change();
assert.ok(card.innerHTML.includes("A description"));
assert.ok(!card.innerHTML.includes("Not active in"));
console.log("Atlas description selection, escaping and timeline checks passed");
