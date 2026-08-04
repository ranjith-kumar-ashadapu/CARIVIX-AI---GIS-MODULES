# 📜 Changelog

All notable changes to the CARIVIX AI GIS Modules project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.1.0] - 2026-08

### Performance Optimizations & Enhancements
* **Added Canvas Rendering Engine:** Switched Leaflet vector renderer from SVG to HTML5 Canvas (`L.canvas()`) to eliminate browser DOM bloat when handling large vector datasets.
* **Added Progressive Zoom Thresholding:** Configured `SUBDISTRICT_ZOOM_THRESHOLD` ($9.0$). High-density Level 3 (Sub-District) boundary layers are now lazy-loaded and only added to the viewport when zoomed in.
* **Added Search Input Debouncing:** Wrapped the real-time search event handler in a 250ms debounce function to reduce layout re-renders during text input.
* **Optimized Marker Clustering:** Configured `chunkedLoading: true` on `L.markerClusterGroup` to prevent UI thread blocking while rendering cluster nodes.

---

## [1.0.0] - 2026-07

### Initial Feature Release
* **Layer Toggling:** Implemented interactive checkbox controls for Nation (L0), State (L1), District (L2), Sub-District (L3), Marker Clusters, and Heatmaps.
* **Spatial Hierarchy Popups:** Formatted popup cards displaying metadata across Sub-District, District, State, and Nation hierarchies.
* **Search & State Filters:** Implemented dynamic dropdown filtering by state and search-based map navigation using `flyToBounds`.
* **Interactive North Arrow:** Added quick map re-centering compass control.