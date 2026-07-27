from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
import os
import json

app = FastAPI(
    title="India Administrative Boundary & Point GIS API",
    description="High-performance WebGIS spatial data delivery API serving GADM v4.1 administrative boundary vectors and spatial density point layers.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],
    allow_headers=["*"],
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

BOUNDARIES_MAP = {
    0: "assets/optimized_geojson/gadm41_IND_0_ultra_opt.geojson",
    1: "assets/optimized_geojson/gadm41_IND_1_ultra_opt.geojson",
    2: "assets/optimized_geojson/gadm41_IND_2_ultra_opt.geojson",
    3: "assets/optimized_geojson/gadm41_IND_3_ultra_opt.geojson"
}

@app.get("/", summary="Render WebGIS Application UI", tags=["Frontend Application"])
async def render_map():
    index_path = os.path.join(BASE_DIR, "index.html")
    if not os.path.exists(index_path):
        raise HTTPException(status_code=404, detail="index.html not found.")
    return FileResponse(index_path, media_type="text/html")


@app.get(
    "/api/v1/boundaries/{level}",
    summary="Get Boundary GeoJSON Payload",
    tags=["Administrative Boundaries"]
)
async def get_boundary(
    level: int,
    state: str = Query(None, description="Optional State filter to reduce payload size (e.g. 'Telangana')")
):
    """
    Fetch GADM v4.1 Administrative Boundaries:
    - **0**: National Outline
    - **1**: State Boundaries
    - **2**: District Boundaries
    - **3**: Sub-District / Taluka Boundaries
    """
    if level not in BOUNDARIES_MAP:
        raise HTTPException(status_code=400, detail="Invalid boundary level. Choose 0, 1, 2, or 3.")
    
    file_path = os.path.join(BASE_DIR, BOUNDARIES_MAP[level])
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail=f"Boundary file level {level} not found on server.")
    
    # If state filter is supplied, filter in-memory to prevent browser UI hanging
    if state and level > 0:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        filtered_features = [
            feat for feat in data.get("features", [])
            if feat.get("properties", {}).get("NAME_1", "").lower() == state.lower()
        ]
        return JSONResponse(content={"type": "FeatureCollection", "features": filtered_features})

    return FileResponse(file_path, media_type="application/geo+json")


@app.get(
    "/api/v1/points/sample",
    summary="Get Spatial Sample Points & Weights",
    tags=["Point & Heatmap Data"]
)
async def get_sample_points():
    """Fetch point features with weight attributes for WebGL heatmap and circle marker rendering."""
    file_path = os.path.join(BASE_DIR, "assets/points/sample_points.geojson")
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Sample points dataset not found.")
    
    return FileResponse(file_path, media_type="application/geo+json")