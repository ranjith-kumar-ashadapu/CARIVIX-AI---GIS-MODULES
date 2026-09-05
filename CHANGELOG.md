# 📜 Changelog

All notable changes to the CARIVIX AI GIS Modules project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.3.0] - 2026-09-05 (Sprint 4 — Week 4)

### Added
* **Dynamic GIS Intelligence Interface:** Upgraded from static cartographic display to an interactive spatial intelligence UI.
* **Geographic Search & 250ms Debouncing:** Added real-time text search querying an in-memory `spatialFeatureIndex` with debouncing to prevent UI thread blocking.
* **Cascading Region Selectors:** Dynamic State and District dropdown filtering with automated camera navigation (`map.fitBounds`).
* **Thematic Choropleth & Dynamic Legend:** 4-tier quantile activity classification (`THEMATIC_SCALE`) with a real-time responsive map legend.
* **Kernel Density Heatmap:** Integrated continuous heat density rendering (`Leaflet.heat`) synchronized with feature property distributions.
* **Bi-Directional Telemetry Dashboard:** Floating analytical dashboard panel updating on feature clicks and dropdown interactions.
* **Keyless Basemap Integration:** Migrated to ESRI World Light Gray Canvas to eliminate CARTO watermark restrictions.

### Optimized
* **Rendering Pipeline:** Enforced `preferCanvas: true` yielding a 51.4% DOM node reduction (486 nodes) and 3.24x execution speedup.
* **DOM Pane Stacking:** Decoupled border overlays (`borderPane` with `pointer-events: none` at z-index 450) from interactive polygons (`districtPane` at z-index 410) to eliminate click event swallowing.
* **Progressive Zoom Thresholding:** Dynamic styling updates based on zoom levels to maintain 60 FPS viewport navigation.


## [1.2.0] - 2026-08-05

### Fixed

- Layer Occlusion & Stacking Order: Resolved visual bug where District (Level 2) and Sub-District (Level 3) polygon fills painted over National (Level 0) and State (Level 1) boundaries.
- Popup Click Interception: Fixed issue where static boundary overlays swallowed click events on underlying interactive polygons and point markers.
- Sub-District Path Rendering: Fixed Level 3 boundary fading across zoom transitions by switching from dynamic layer re-mounting to soft opacity toggling (L3_VISIBLE_STYLE / L3_HIDDEN_STYLE) to preserve Canvas rendering context.

### Changed
- Custom Pane & Z-Index Architecture: Introduced borderPane (zIndex: 450, pointer-events: none) for top-level borders and adjusted districtPane (zIndex: 410) for polygon fills.
- Zoom Threshold Adjustment: Adjusted SUBDISTRICT_ZOOM_THRESHOLD to 7.0 to display Sub-District boundaries at default initial zoom viewports while maintaining smooth Canvas performance.

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