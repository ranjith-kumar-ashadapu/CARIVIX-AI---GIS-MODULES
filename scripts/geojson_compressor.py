import geopandas as gpd
import os

# Resolve paths relative to this script so the script works from any CWD
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_PATH = os.path.normpath(os.path.join(BASE_DIR, '..', 'assets', 'optimized_geojson', 'gadm41_IND_3_opt.geojson'))
OUTPUT_PATH = os.path.normpath(os.path.join(BASE_DIR, '..', 'assets', 'optimized_geojson', 'gadm41_IND_3_ultra_opt.geojson'))

# Load GeoJSON
gdf = gpd.read_file(INPUT_PATH)

# Simplify geometries slightly (e.g., 0.001 degree tolerance)
gdf['geometry'] = gdf['geometry'].simplify(tolerance=0.001, preserve_topology=True)

# Save with reduced float precision
gdf.to_file(OUTPUT_PATH, driver="GeoJSON", coordinate_precision=4)