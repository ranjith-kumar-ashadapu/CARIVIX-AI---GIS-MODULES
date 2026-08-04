# CARIVIX AI - WebGIS Application Module

An interactive, high-performance WebGIS mapping engine built using **Leaflet.js**, featuring multi-level spatial administrative hierarchies, point clustering, density heatmaps, and dynamic spatial filtering.

---

## 🚀 Key Features

* **Multi-Level Administrative Hierarchy:** Real-time visibility toggling for Nation (L0), State (L1), District (L2), and Sub-District (L3) boundaries.
* **Client-Side Performance Optimizations:**
  * **Canvas Rendering Engine:** Utilizes HTML5 Canvas (`L.canvas()`) to render high-density vector boundaries without heavy DOM overhead.
  * **Progressive Zoom Thresholding:** Lazy loads and dynamically displays high-detail Level 3 boundaries only at zoom levels $\ge 9.0$.
  * **Debounced Event Handling:** Optimizes DOM search interactions to ensure smooth frame rates during real-time queries.
* **Spatial Search & Filtering:** Dynamic State selection filter and smooth `flyToBounds` navigation for district queries.
* **Interactive Marker Clustering & Heatmaps:** Dynamic point feature aggregation (`Leaflet.markercluster`) and spatial density visualization (`Leaflet.heat`).
* **Interactive Compass:** Quick "Reset Map Orientation to North" control with automatic viewport re-centering.

---

## 🛠️ Tech Stack

* **Frontend:** HTML5, CSS3, JavaScript (ES6+)
* **Mapping Library:** Leaflet.js (v1.9.4)
* **Plugins:** `Leaflet.markercluster`, `Leaflet.heat`
* **API Integration:** RESTful GeoJSON endpoint integration (`http://localhost:8000/api/v1`)

---

## 📂 Project Structure

```text
├── index.html              # Main WebGIS application entry point
├── CHANGELOG.md            # Versioning and release history
└── README.md               # Project documentation