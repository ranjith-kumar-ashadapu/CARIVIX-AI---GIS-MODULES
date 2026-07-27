import json
import os


def optimize_geojson(input_path, output_path, decimals=5):
    encodings = ('utf-8-sig', 'utf-8', 'cp1252', 'latin-1')
    data = None

    for encoding in encodings:
        try:
            with open(input_path, 'r', encoding=encoding, errors='replace') as f:
                data = json.load(f)
            break
        except (UnicodeDecodeError, json.JSONDecodeError):
            continue

    if data is None:
        raise ValueError(f'Unable to read GeoJSON file: {input_path}')

    def round_coords(coords):
        if isinstance(coords[0], list):
            return [round_coords(c) for c in coords]
        return [round(c, decimals) for c in coords]

    for feature in data.get('features', []):
        feature['geometry']['coordinates'] = round_coords(feature['geometry']['coordinates'])

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, separators=(',', ':'), ensure_ascii=False)


if __name__ == '__main__':
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    raw_dir = os.path.join(BASE_DIR, 'assets', 'raw_geojson')
    opt_dir = os.path.join(BASE_DIR, 'assets', 'optimized_geojson')
    input_path = os.path.join(raw_dir, 'gadm41_IND_0.geojson')
    output_path = os.path.join(opt_dir, 'gadm41_IND_0_opt.geojson')
    optimize_geojson(input_path, output_path)