# India GIS Data Services REST API Specification

**Service Name:** India Boundary & Density Visualizer API  
**API Version:** 1.0.0  
**Base URL:** `http://localhost:8000` (Local Host)  
**Data Format:** GeoJSON (`application/geo+json`, `application/json`)  

---

## Endpoint 1: Application Web Entry Point

Renders the visualizer application HTML interface.

* **HTTP Method:** `GET`
* **Path:** `/`
* **Response:** HTML page containing MapLibre GL JS engine and layer control panels.

### Response Codes
| Status Code | Description | Content Type |
|---|---|---|
| `200 OK` | Map application successfully rendered. | `text/html` |
| `404 Not Found` | `index.html` not present on the server. | `application/json` |

---

## Endpoint 2: Administrative Boundaries Payload

Retrieves vector polygon boundary datasets for GADM administrative levels 0 through 3.

* **HTTP Method:** `GET`
* **Path:** `/api/v1/boundaries/{level}`

### Input Parameters

#### Path Parameters
| Field Name | Type | Required | Allowed Values | Description |
|---|---|---|---|---|
| `level` | `integer` | **Yes** | `0`, `1`, `2`, `3` | Administrative division level:<br>• `0`: Country boundary<br>• `1`: State boundaries<br>• `2`: District boundaries<br>• `3`: Sub-district / Taluka boundaries |

#### Query Parameters
| Field Name | Type | Required | Default | Description |
|---|---|---|---|---|
| `state` | `string` | No | `null` | Filters boundary features by State Name (e.g., `Telangana`). Recommended to prevent large browser payload rendering freezes. |

### Request Headers
```http
GET /api/v1/boundaries/2?state=Telangana HTTP/1.1
Host: localhost:8000
Accept: application/geo+json
```

### Response Body (200 OK)
```JSON
{
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "properties": {
        "GID_0": "IND",
        "NAME_0": "India",
        "GID_1": "IND.32_1",
        "NAME_1": "Telangana",
        "GID_2": "IND.32.1_1",
        "NAME_2": "Adilabad"
      },
      "geometry": {
        "type": "MultiPolygon",
        "coordinates": [
          [
            [
              [78.4812, 19.6734],
              [78.5201, 19.7011],
              [78.4812, 19.6734]
            ]
          ]
        ]
      }
    }
  ]
}
```

## Endpoint 3: Spatial Heatmap & Sample Points

Retrieves point coordinate feature collections with assigned density weights.

* **HTTP Method:** GET
* **Path:** /api/v1/points/sample

### Request Headers
```http
GET /api/v1/points/sample HTTP/1.1
Host: localhost:8000
Accept: application/geo+json
```

### Response Body (200 OK)
```json
{
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "properties": {
        "id": 1,
        "weight": 8.5,
        "name": "Hyderabad Node"
      },
      "geometry": {
        "type": "Point",
        "coordinates": [79.0193, 18.1124]
      }
    }
  ]
}
```

## HTTP Status Codes Table

| Code | Code Identifier | Cause / Remediation |
| --- | --- | --- |
| 200 | OK | Request successfully executed.| 
| 400 | BAD_REQUEST | Provided level integer is out of bounds (allowed range: 0–3).| 
| 404 | NOT_FOUND | Dataset file or filtered state payload does not exist.|
| 500 | INTERNAL_SERVER_ERROR | Internal server or JSON parsing failure. |