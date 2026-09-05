# CARIVIX AI — WebGIS Intelligence Engine

An interactive, enterprise-grade WebGIS spatial intelligence platform built using **FastAPI** and **Leaflet.js**, featuring multi-level administrative boundary hierarchies (L0–L3), HTML5 Canvas-accelerated vector rendering, kernel heat density visualization, marker clustering, attribute query filters, and real-time telemetry dashboards.

---

## 🌟 Key Features

* **Multi-Level Administrative Hierarchy:** Real-time boundary rendering for National (L0), State (L1), District (L2), and Sub-District (L3) GADM datasets.
* **FastAPI Spatial REST Backend:** High-performance RESTful API endpoints serving GeoJSON boundaries, state-filtered feature payloads, sample point weights, spatial attribute queries, and telemetry metrics.
* **Client-Side Performance Optimizations:**
  * **HTML5 Canvas Vector Renderer:** Utilizes `preferCanvas: true` to yield a **51.4% DOM node reduction** (capped at 486 nodes) and **3.24x main thread execution speedup**.
  * **Custom Stacking Panes Architecture:** Decouples top-level borders (`borderPane` with `pointer-events: none` at z-index 450) from interactive district fills (`districtPane` at z-index 410) to eliminate click event swallowing.
  * **Progressive Zoom Thresholding:** Lazy loads high-density sub-district boundaries dynamically at zoom thresholds $\ge 7.0$.
  * **250ms Input Debouncing:** Debounces text search inputs to eliminate DOM layout recalculation overhead during typing.
* **Geographic Search & Cascading Selectors:** Dynamic State and District dropdown filtering with smooth camera navigation (`map.fitBounds` / `map.flyToBounds`).
* **Thematic Choropleth & Heatmap Layers:** 4-tier quantile activity classification with real-time responsive map legends and kernel density heatmaps (`Leaflet.heat`).
* **Bi-Directional Telemetry Dashboard:** Floating analytical telemetry cards updating dynamically on polygon selection and spatial queries.

---

## 🛠️ Tech Stack

* **Backend & API:** Python 3, FastAPI, Uvicorn, CORS Middleware
* **Frontend UI:** HTML5, CSS3 (Vanilla CSS Custom Properties), JavaScript (ES6+ Modules)
* **WebGIS Engine:** Leaflet.js (v1.9.4) with HTML5 Canvas Renderer (`preferCanvas: true`)
* **Plugins:** `Leaflet.markercluster` (Marker Clustering), `Leaflet.heat` (Kernel Heat Density)
* **Basemaps:** ESRI World Light Gray Canvas, CARTO Dark Matter, OpenStreetMap

---

## 🚀 Quick Start Guide

### 1. Prerequisites
- Python 3.9+
- FastAPI & Uvicorn (`pip install fastapi uvicorn`)

### 2. Launch the WebGIS Backend Server
Run the FastAPI application from the project root:

```bash
python -m uvicorn server:app --host 127.0.0.1 --port 8000 --reload
```

Open your browser and navigate to:
👉 **`http://127.0.0.1:8000/`**

### 3. Run Automated API Verification Suite
To execute the automated API benchmark and endpoint verification suite:

```bash
python test_spatial_api.py
```

---

## 📁 Project Structure

```text
├── server.py               # FastAPI WebGIS REST backend & static file server
├── spatialService.js       # ES6 module client-side API adapter & GeoJSON validator
├── index.html              # Main WebGIS interactive visualizer dashboard
├── main.js                 # Layer synchronization & map setup module
├── test_spatial_api.py     # Automated API benchmark & test runner suite
├── API_DOCUMENTATION.md    # Complete REST API specification
├── CHANGELOG.md            # Version release notes and optimization logs
├── README.md               # Project documentation
└── assets/                 # GeoJSON datasets & point spatial assets
    ├── optimized_geojson/  # Quantized & ultra-optimized vector boundary files
    ├── raw_geojson/        # Standard GADM administrative datasets
    └── points/             # Sample spatial point coordinate payloads
```

---

## 📖 API Documentation

For full REST API specifications, query parameters, request/response headers, and GeoJSON schemas, refer to [API_DOCUMENTATION.md](file:///f:/CARIVIX/CARIVIX-AI/CARIVIX%20-%20AI/API_DOCUMENTATION.md).