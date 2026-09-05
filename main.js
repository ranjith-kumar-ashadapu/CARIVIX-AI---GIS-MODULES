// main.js - Map Setup
const map = L.map('map', {
  preferCanvas: true,
  zoomSnap: 0.25,
  minZoom: 4,
  maxZoom: 18
}).setView([20.5937, 78.9629], 5);

// Basemap
L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png', {
  attribution: '&copy; OpenStreetMap, &copy; CARTO'
}).addTo(map);

// Custom DOM Panes for Visual Hierarchy
map.createPane('borderPane');
map.getPane('borderPane').style.zIndex = '450';
map.getPane('borderPane').style.pointerEvents = 'none'; // Pass clicks to lower layers

map.createPane('districtPane');
map.getPane('districtPane').style.zIndex = '410';

// Global Layer Stores
export const layerStore = {
  l0: L.layerGroup().addTo(map),
  l1: L.layerGroup().addTo(map),
  l2: L.layerGroup().addTo(map)
};

// Spatial index for Day 2 search & Day 4 dashboard synchronization
export const spatialFeatureIndex = new Map();


// main.js - Synchronization Pipeline
import { fetchBoundaryLayer } from './spatialService.js';

export async function synchronizeSpatialData() {
  const loader = document.getElementById('map-loader');
  if (loader) loader.classList.remove('hidden');

  try {
    // 1. Fetch boundary tiers concurrently
    const [l0Data, l1Data, l2Data] = await Promise.all([
      fetchBoundaryLayer(0),
      fetchBoundaryLayer(1),
      fetchBoundaryLayer(2)
    ]);

    // 2. Clear stale layers to prevent memory leaks and orphan DOM listeners
    layerStore.l0.clearLayers();
    layerStore.l1.clearLayers();
    layerStore.l2.clearLayers();
    spatialFeatureIndex.clear();

    // 3. National Boundaries (Non-Interactive, Top Stacking Pane)
    L.geoJSON(l0Data, {
      pane: 'borderPane',
      interactive: false,
      style: { color: '#0f172a', weight: 3.0, fill: false }
    }).addTo(layerStore.l0);

    // 4. State Boundaries (Non-Interactive, Top Stacking Pane)
    L.geoJSON(l1Data, {
      pane: 'borderPane',
      interactive: false,
      style: { color: '#334155', weight: 1.8, fill: false }
    }).addTo(layerStore.l1);

    // 5. District Polygons (Interactive Intelligence Pane)
    L.geoJSON(l2Data, {
      pane: 'districtPane',
      style: {
        color: '#64748b',
        weight: 1.0,
        fillColor: '#38bdf8',
        fillOpacity: 0.15
      },
      onEachFeature: (feature, layer) => {
        const props = feature.properties || {};

        // Register feature in memory for O(1) lookups during search and analytics
        const lookupKey = (props.district_id || props.NAME_2 || '').toLowerCase();
        if (lookupKey) {
          spatialFeatureIndex.set(lookupKey, { feature, layer });
        }

        // Popup configuration
        layer.bindPopup(`
          <div class="p-2">
            <h4 class="font-bold text-sm text-slate-900">${props.NAME_2 || 'District'}</h4>
            <p class="text-xs text-slate-600">State: ${props.NAME_1 || 'N/A'}</p>
          </div>
        `);

        layer.on('click', (e) => L.DomEvent.stopPropagation(e));
      }
    }).addTo(layerStore.l2);

    console.info(`[Sync Complete] Registered ${spatialFeatureIndex.size} features in spatial index.`);
  } catch (error) {
    console.error('[GIS Sync Error]:', error);
  } finally {
    if (loader) loader.classList.add('hidden');
  }
}

// Execute on application initialization
window.addEventListener('DOMContentLoaded', synchronizeSpatialData);