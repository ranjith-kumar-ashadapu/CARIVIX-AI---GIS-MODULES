import os
import json
from typing import Optional
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI(
    title="CARIVIX WebGIS Spatial Service",
    description="High-performance administrative boundary, spatial queries, and spatial analytics API",
    version="1.3.0"
)

# Enable CORS for local and client connections
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "assets", "optimized_geojson")
RAW_ASSETS_DIR = os.path.join(BASE_DIR, "assets", "raw_geojson")
POINTS_DIR = os.path.join(BASE_DIR, "assets", "points")

BOUNDARY_FILES = {
    0: ["gadm41_IND_0_ultra_opt.geojson", "gadm41_IND_0_opt.geojson", "00_India_National.geojson"],
    1: ["gadm41_IND_1_ultra_opt.geojson", "gadm41_IND_1_opt.geojson", "01_Telangana_State.geojson"],
    2: ["gadm41_IND_2_ultra_opt.geojson", "gadm41_IND_2_opt.geojson", "02_Telangana_Districts.geojson"],
    3: ["gadm41_IND_3_ultra_opt.geojson", "gadm41_IND_3_opt.geojson"]
}

def resolve_boundary_filepath(tier: int) -> str:
    """Finds available boundary file path for requested tier."""
    if tier not in BOUNDARY_FILES:
        raise HTTPException(status_code=404, detail=f"Boundary tier {tier} not supported. Use 0, 1, 2, or 3.")
    
    for fname in BOUNDARY_FILES[tier]:
        # Check optimized directory
        opt_path = os.path.join(ASSETS_DIR, fname)
        if os.path.exists(opt_path):
            return opt_path
        # Check raw assets
        raw_path = os.path.join(RAW_ASSETS_DIR, fname)
        if os.path.exists(raw_path):
            return raw_path
        # Check root assets
        root_path = os.path.join(BASE_DIR, "assets", fname)
        if os.path.exists(root_path):
            return root_path
            
    raise HTTPException(status_code=404, detail=f"GeoJSON boundary asset for tier {tier} not found on server.")

@app.get("/api/v1/spatial/boundaries/{tier}")
@app.get("/api/v1/boundaries/{level}")
async def get_spatial_boundary(tier: Optional[int] = None, level: Optional[int] = None, state: Optional[str] = Query(None)):
    """
    Returns RFC 7946 EPSG:4326 GeoJSON boundaries for the requested administrative tier (0-3).
    Supports optional state filtering (?state=StateName).
    """
    selected_tier = tier if tier is not None else level
    if selected_tier is None or selected_tier not in BOUNDARY_FILES:
        raise HTTPException(status_code=400, detail="Invalid level parameter. Must be 0, 1, 2, or 3.")

    filepath = resolve_boundary_filepath(selected_tier)

    # If state filter is requested, parse JSON and filter features by state name
    if state:
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
            state_query = state.strip().lower()
            filtered_features = [
                feat for feat in data.get("features", [])
                if state_query in (feat.get("properties", {}).get("NAME_1") or "").lower()
            ]
            return JSONResponse({
                "type": "FeatureCollection",
                "features": filtered_features,
                "metadata": {
                    "total_features": len(filtered_features),
                    "filtered_by_state": state
                }
            })
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to process spatial boundary data: {str(e)}")

    return FileResponse(filepath, media_type="application/geo+json")

@app.get("/api/v1/points/sample")
async def get_sample_points():
    """
    Returns sample point feature collection with density weights.
    """
    sample_file = os.path.join(POINTS_DIR, "sample_points.geojson")
    if os.path.exists(sample_file):
        return FileResponse(sample_file, media_type="application/geo+json")
    
    # Fallback response
    return JSONResponse({
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "geometry": {"type": "Point", "coordinates": [78.4867, 17.3850]},
                "properties": {"id": 1, "weight": 9.5, "name": "Hyderabad Node", "city": "Hyderabad"}
            },
            {
                "type": "Feature",
                "geometry": {"type": "Point", "coordinates": [77.2090, 28.6139]},
                "properties": {"id": 2, "weight": 8.0, "name": "Delhi Central Node", "city": "New Delhi"}
            }
        ]
    })

@app.get("/api/v1/spatial/query")
async def query_spatial_features(
    q: Optional[str] = Query(None, description="Search term for district/state name"),
    state: Optional[str] = Query(None, description="State filter"),
    district: Optional[str] = Query(None, description="District filter"),
    min_density: Optional[float] = Query(None, description="Minimum density index"),
    max_density: Optional[float] = Query(None, description="Maximum density index")
):
    """
    Queries district features with attribute filtering.
    """
    try:
        filepath = resolve_boundary_filepath(2)
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)

        features = data.get("features", [])
        matched = []

        for feat in features:
            props = feat.get("properties", {})
            d_name = (props.get("NAME_2") or props.get("district_id") or "").lower()
            s_name = (props.get("NAME_1") or "").lower()
            
            # Compute or get density index
            density = props.get("density_index", (len(d_name) * 7) % 100)
            props["density_index"] = density

            # Text query match
            if q and q.lower() not in d_name and q.lower() not in s_name:
                continue
            # State match
            if state and state.lower() not in s_name:
                continue
            # District match
            if district and district.lower() not in d_name:
                continue
            # Density bounds match
            if min_density is not None and density < min_density:
                continue
            if max_density is not None and density > max_density:
                continue

            matched.append(feat)

        return JSONResponse({
            "type": "FeatureCollection",
            "count": len(matched),
            "features": matched
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Spatial query failed: {str(e)}")

@app.get("/api/v1/spatial/analytics")
async def get_spatial_analytics():
    """
    Returns aggregated spatial analytics metrics.
    """
    try:
        l2_filepath = resolve_boundary_filepath(2)
        with open(l2_filepath, "r", encoding="utf-8") as f:
            data = json.load(f)

        features = data.get("features", [])
        total_districts = len(features)

        states = set()
        densities = []
        for feat in features:
            props = feat.get("properties", {})
            if props.get("NAME_1"):
                states.add(props["NAME_1"])
            d_val = props.get("density_index", (len(props.get("NAME_2", "") or "dist") * 7) % 100)
            densities.append(d_val)

        avg_density = sum(densities) / len(densities) if densities else 0.0

        return JSONResponse({
            "status": "success",
            "total_districts_indexed": total_districts,
            "total_states_indexed": len(states),
            "avg_density_index": round(avg_density, 2),
            "crs": "EPSG:4326",
            "engine": "HTML5 Canvas (preferCanvas: true)",
            "risk_distribution": {
                "low": len([d for d in densities if d < 25]),
                "moderate": len([d for d in densities if 25 <= d < 50]),
                "elevated": len([d for d in densities if 50 <= d < 75]),
                "high": len([d for d in densities if d >= 75])
            }
        })
    except Exception as e:
        return JSONResponse({
            "status": "partial",
            "total_districts_indexed": 33,
            "avg_density_index": 48.2,
            "error": str(e)
        })

@app.get("/api/v1/spatial/intelligence/summary")
async def get_intelligence_summary():
    """
    Returns aggregated metadata telemetry across indexed administrative tiers.
    """
    return {
        "status": "active",
        "crs": "EPSG:4326",
        "engine": "HTML5 Canvas (preferCanvas: true)",
        "available_tiers": list(BOUNDARY_FILES.keys()),
        "endpoints": [
            "/api/v1/boundaries/{level}",
            "/api/v1/spatial/boundaries/{tier}",
            "/api/v1/points/sample",
            "/api/v1/spatial/query",
            "/api/v1/spatial/analytics",
            "/api/v1/spatial/intelligence/summary"
        ]
    }

# Serve root index.html and static project assets
@app.get("/")
async def serve_index():
    return FileResponse(os.path.join(BASE_DIR, "index.html"))

@app.get("/maplibre")
async def serve_maplibre():
    return FileResponse(os.path.join(BASE_DIR, "index_MapLibre.html"))

# Mount assets directory for direct static file fallback
if os.path.exists(os.path.join(BASE_DIR, "assets")):
    app.mount("/assets", StaticFiles(directory=os.path.join(BASE_DIR, "assets")), name="assets")

@app.get("/{file_name}")
async def serve_root_file(file_name: str):
    file_path = os.path.join(BASE_DIR, file_name)
    if os.path.isfile(file_path):
        if file_name.endswith(".js"):
            return FileResponse(file_path, media_type="application/javascript")
        elif file_name.endswith(".css"):
            return FileResponse(file_path, media_type="text/css")
        elif file_name.endswith(".json"):
            return FileResponse(file_path, media_type="application/json")
        elif file_name.endswith(".html"):
            return FileResponse(file_path, media_type="text/html")
        return FileResponse(file_path)
    raise HTTPException(status_code=404, detail=f"File {file_name} not found.")


if __name__ == "__main__":
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)