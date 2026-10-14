function createTerritory(map, polityRgb) {
  const WIDTH = 1440;
  const NORTH = 84;
  const SOUTH = -60;
  const REACH_KM = [0, 50, 120, 250, 500];
  const THRESHOLD = 0.13;
  const MOVES = [
    [1, 0], [-1, 0], [0, 1], [0, -1], [1, 1], [1, -1], [-1, 1], [-1, -1],
    [2, 1], [2, -1], [-2, 1], [-2, -1], [1, 2], [1, -2], [-1, 2], [-1, -2]
  ];
  const yNorth = mercator(NORTH);
  const ySouth = mercator(SOUTH);
  const HEIGHT = Math.round(WIDTH * (yNorth - ySouth) / (2 * Math.PI));
  const rowLat = new Float32Array(HEIGHT);
  const stepX = new Float32Array(HEIGHT);
  const stepY = new Float32Array(HEIGHT);
  for (let row = 0; row < HEIGHT; row++) rowLat[row] = latitude(yNorth - (row + 0.5) * (yNorth - ySouth) / HEIGHT);
  for (let row = 0; row < HEIGHT; row++) {
    stepX[row] = 111.32 * Math.cos(rowLat[row] * Math.PI / 180) * 360 / WIDTH;
    stepY[row] = row < HEIGHT - 1 ? 111.2 * (rowLat[row] - rowLat[row + 1]) : 0;
  }

  const field = document.createElement("canvas");
  field.width = WIDTH;
  field.height = HEIGHT;
  const pane = map.createPane("territory");
  pane.style.zIndex = 350;
  pane.style.pointerEvents = "none";
  const canvas = document.createElement("canvas");
  pane.appendChild(canvas);
  let land = null;
  let landCells = null;
  const spreads = new Map();
  let year = null;
  let places = [];

  function mercator(lat) {
    return Math.log(Math.tan(Math.PI / 4 + lat * Math.PI / 360));
  }

  function latitude(y) {
    return Math.atan(Math.sinh(y)) * 180 / Math.PI;
  }

  function gridX(lng) {
    return (lng + 180) / 360 * WIDTH;
  }

  function gridY(lat) {
    return (yNorth - mercator(Math.max(-85, Math.min(85, lat)))) / (yNorth - ySouth) * HEIGHT;
  }

  function landPath(context, project) {
    context.beginPath();
    land.features.forEach(function (feature) {
      const geometry = feature.geometry;
      const polygons = geometry.type === "Polygon" ? [geometry.coordinates] : geometry.coordinates;
      polygons.forEach(function (rings) {
        rings.forEach(function (ring) {
          ring.forEach(function (coordinate, index) {
            const point = project(coordinate);
            if (index === 0) context.moveTo(point[0], point[1]);
            else context.lineTo(point[0], point[1]);
          });
          context.closePath();
        });
      });
    });
  }

  function rasterizeLand() {
    const mask = document.createElement("canvas");
    mask.width = WIDTH;
    mask.height = HEIGHT;
    const context = mask.getContext("2d");
    landPath(context, function (c) { return [gridX(c[0]), gridY(c[1])]; });
    context.fill("evenodd");
    const pixels = context.getImageData(0, 0, WIDTH, HEIGHT).data;
    landCells = new Uint8Array(WIDTH * HEIGHT);
    for (let cell = 0; cell < landCells.length; cell++) landCells[cell] = pixels[cell * 4 + 3] > 0 ? 1 : 0;
  }

  function cellAt(x, y) {
    return y < 0 || y >= HEIGHT ? -1 : y * WIDTH + (x + WIDTH) % WIDTH;
  }

  function nearestLand(x, y) {
    for (let radius = 0; radius <= 2; radius++) {
      for (let dy = -radius; dy <= radius; dy++) {
        for (let dx = -radius; dx <= radius; dx++) {
          const cell = cellAt(x + dx, y + dy);
          if (cell !== -1 && landCells[cell]) return cell;
        }
      }
    }
    return -1;
  }

  function spread(place) {
    const limit = REACH_KM[place.importance] * Math.log(1 / THRESHOLD);
    const start = nearestLand(Math.floor(gridX(place.longitude)), Math.floor(gridY(place.latitude)));
    const distances = new Map();
    if (start !== -1) {
      const heap = [[0, start]];
      distances.set(start, 0);
      while (heap.length) {
        const [travelled, cell] = heapPop(heap);
        if (travelled > distances.get(cell)) continue;
        const x = cell % WIDTH;
        const y = Math.floor(cell / WIDTH);
        MOVES.forEach(function ([dx, dy]) {
          const next = cellAt(x + dx, y + dy);
          if (next === -1 || !landCells[next]) return;
          const halfX = Math.trunc(dx / 2);
          const halfY = Math.trunc(dy / 2);
          if (!landCells[cellAt(x + halfX, y + halfY)] || !landCells[cellAt(x + dx - halfX, y + dy - halfY)]) return;
          let vertical = 0;
          for (let row = Math.min(y, y + dy); row < Math.max(y, y + dy); row++) vertical += stepY[row];
          const distance = travelled + Math.hypot(stepX[y] * dx, vertical);
          if (distance > limit || distance >= (distances.get(next) ?? Infinity)) return;
          distances.set(next, distance);
          heapPush(heap, [distance, next]);
        });
      }
    }
    return { cells: Int32Array.from(distances.keys()), distances: Float32Array.from(distances.values()) };
  }

  function heapPush(heap, item) {
    heap.push(item);
    let index = heap.length - 1;
    while (index > 0) {
      const parent = (index - 1) >> 1;
      if (heap[parent][0] <= item[0]) break;
      heap[index] = heap[parent];
      index = parent;
    }
    heap[index] = item;
  }

  function heapPop(heap) {
    const top = heap[0];
    const last = heap.pop();
    if (heap.length) {
      let index = 0;
      while (true) {
        let child = 2 * index + 1;
        if (child >= heap.length) break;
        if (child + 1 < heap.length && heap[child + 1][0] < heap[child][0]) child++;
        if (heap[child][0] >= last[0]) break;
        heap[index] = heap[child];
        index = child;
      }
      heap[index] = last;
    }
    return top;
  }

  function paintField() {
    const scores = new Float32Array(WIDTH * HEIGHT);
    const owners = new Array(WIDTH * HEIGHT);
    places.forEach(function (place) {
      const key = place.id + ":" + place.importance;
      if (!spreads.has(key)) spreads.set(key, spread(place));
      const area = spreads.get(key);
      const reach = REACH_KM[place.importance];
      for (let index = 0; index < area.cells.length; index++) {
        const cell = area.cells[index];
        const score = Math.exp(-area.distances[index] / reach);
        if (score > scores[cell]) {
          scores[cell] = score;
          owners[cell] = place.polity;
        }
      }
    });

    const sharpness = Math.min(1, Math.max(0, (year - 1500) / 300));
    const full = 0.8 - sharpness * (0.78 - THRESHOLD);
    const image = new ImageData(WIDTH, HEIGHT);
    for (let cell = 0; cell < scores.length; cell++) {
      if (scores[cell] <= THRESHOLD) continue;
      const rgb = polityRgb(owners[cell]);
      image.data[cell * 4] = rgb[0];
      image.data[cell * 4 + 1] = rgb[1];
      image.data[cell * 4 + 2] = rgb[2];
      image.data[cell * 4 + 3] = 170 * Math.min(1, (scores[cell] - THRESHOLD) / (full - THRESHOLD));
    }
    field.getContext("2d").putImageData(image, 0, 0);
  }

  function draw() {
    const size = map.getSize();
    canvas.width = size.x;
    canvas.height = size.y;
    canvas.style.display = "";
    L.DomUtil.setPosition(canvas, map.containerPointToLayerPoint([0, 0]));
    if (!landCells || year === null) return;
    const context = canvas.getContext("2d");
    const northWest = map.latLngToContainerPoint([NORTH, -180]);
    const southEast = map.latLngToContainerPoint([SOUTH, 180]);
    context.imageSmoothingEnabled = true;
    context.drawImage(field, northWest.x, northWest.y, southEast.x - northWest.x, southEast.y - northWest.y);
    context.globalCompositeOperation = "destination-in";
    landPath(context, function (c) {
      const point = map.latLngToContainerPoint([c[1], c[0]]);
      return [point.x, point.y];
    });
    context.fill("evenodd");
  }

  map.on("zoomstart", function () { canvas.style.display = "none"; });
  map.on("moveend resize", draw);

  return {
    setLand: function (geojson) {
      land = geojson;
      rasterizeLand();
      if (year !== null) paintField();
      draw();
    },
    show: function (newYear, newPlaces) {
      if (newYear === year) return;
      year = newYear;
      places = newPlaces;
      if (landCells) paintField();
      draw();
    }
  };
}
