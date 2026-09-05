// spatialService.js - CARIVIX WebGIS Spatial API Client Module

const API_BASE = '/api/v1/spatial/boundaries';
const spatialCache = new Map();

/**
 * Validates RFC 7946 GeoJSON and standard EPSG:4326 [longitude, latitude] bounds.
 */
export function validateGeoJson(payload, level) {
  if (!payload || payload.type !== 'FeatureCollection' || !Array.isArray(payload.features)) {
    throw new Error(`[GIS Validation] Level ${level} is not a valid FeatureCollection.`);
  }

  if (payload.features.length > 0) {
    const sampleCoord = payload.features[0]?.geometry?.coordinates;
    if (sampleCoord) {
      const [lng, lat] = Array.isArray(sampleCoord[0])
        ? (Array.isArray(sampleCoord[0][0]) ? sampleCoord[0][0][0] : sampleCoord[0][0])
        : sampleCoord;

      if (lng < -180 || lng > 180 || lat < -90 || lat > 90) {
        console.warn(`[GIS Validation] Coordinates out of EPSG:4326 bounds: [${lng}, ${lat}]`);
      }
    }
  }
  return true;
}

/**
 * Fetches boundary data with client-side cache fallback.
 */
export async function fetchBoundaryLayer(level, stateFilter = null) {
  const cacheKey = stateFilter ? `${level}_${stateFilter}` : `${level}`;
  if (spatialCache.has(cacheKey)) {
    return spatialCache.get(cacheKey);
  }

  const url = stateFilter 
    ? `/api/v1/boundaries/${level}?state=${encodeURIComponent(stateFilter)}`
    : `${API_BASE}/${level}`;

  const response = await fetch(url, {
    headers: { 'Accept': 'application/json' }
  });

  if (!response.ok) {
    throw new Error(`HTTP Error ${response.status}: Failed to fetch level ${level} spatial layer.`);
  }

  const data = await response.json();
  validateGeoJson(data, level);
  spatialCache.set(cacheKey, data);
  return data;
}

/**
 * Fetches sample spatial points for heatmap/clustering layers.
 */
export async function fetchSamplePoints() {
  const response = await fetch('/api/v1/points/sample', {
    headers: { 'Accept': 'application/json' }
  });
  if (!response.ok) {
    throw new Error(`HTTP Error ${response.status}: Failed to fetch sample points.`);
  }
  return await response.json();
}

/**
 * Executes a spatial attribute query.
 */
export async function querySpatialFeatures(params = {}) {
  const queryParams = new URLSearchParams();
  if (params.q) queryParams.append('q', params.q);
  if (params.state) queryParams.append('state', params.state);
  if (params.district) queryParams.append('district', params.district);
  if (params.min_density) queryParams.append('min_density', params.min_density);
  if (params.max_density) queryParams.append('max_density', params.max_density);

  const response = await fetch(`/api/v1/spatial/query?${queryParams.toString()}`);
  if (!response.ok) {
    throw new Error(`Spatial query failed with status ${response.status}`);
  }
  return await response.json();
}

/**
 * Fetches spatial analytics telemetry from API.
 */
export async function fetchSpatialAnalytics() {
  const response = await fetch('/api/v1/spatial/analytics');
  if (!response.ok) {
    throw new Error(`Failed to fetch spatial analytics.`);
  }
  return await response.json();
}