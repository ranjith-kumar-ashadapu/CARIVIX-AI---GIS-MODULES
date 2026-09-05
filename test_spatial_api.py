"""
test_spatial_api.py - Day 5 Automated Verification Suite for CARIVIX WebGIS Spatial APIs
"""

import sys
import json
from urllib.request import urlopen, Request
from urllib.error import HTTPError, URLError

BASE_URL = "http://127.0.0.1:8000"

def test_endpoint(url, description, expected_status=200):
    print(f"[TEST] {description}: {url} ... ", end="")
    req = Request(url, headers={"User-Agent": "CARIVIX-Test-Runner/1.0", "Accept": "application/json"})
    try:
        with urlopen(req, timeout=10) as response:
            status = response.getcode()
            body = response.read().decode('utf-8')
            if status == expected_status:
                print(f"PASSED ({status} OK, {len(body)} bytes)")
                return json.loads(body) if 'json' in response.headers.get('Content-Type', '') else body
            else:
                print(f"FAILED (Got status {status}, expected {expected_status})")
                return None
    except HTTPError as e:
        print(f"HTTP ERROR ({e.code})")
        return None
    except URLError as e:
        print(f"URL ERROR ({e.reason})")
        return None
    except Exception as e:
        print(f"EXCEPTION ({str(e)})")
        return None

def main():
    print("================================================================")
    print(" CARIVIX AI WebGIS -- Day 5 API Automated Verification Suite")
    print("================================================ fallbacks =====\n")

    # 1. Test Intelligence Summary
    summary = test_endpoint(f"{BASE_URL}/api/v1/spatial/intelligence/summary", "1. Intelligence Summary Endpoint")
    assert summary is not None, "Summary endpoint test failed"

    # 2. Test Spatial Analytics
    analytics = test_endpoint(f"{BASE_URL}/api/v1/spatial/analytics", "2. Spatial Analytics Telemetry Endpoint")
    assert analytics is not None, "Analytics endpoint test failed"

    # 3. Test Boundary Tiers
    for tier in [0, 1, 2]:
        boundary = test_endpoint(f"{BASE_URL}/api/v1/spatial/boundaries/{tier}", f"3. Boundary Tier {tier} Endpoint")
        assert boundary is not None, f"Boundary tier {tier} failed"

    # 4. Test State Filtering
    state_payload = test_endpoint(f"{BASE_URL}/api/v1/boundaries/2?state=Telangana", "4. State Filter Boundary Endpoint (?state=Telangana)")
    assert state_payload is not None, "State filter boundary test failed"

    # 5. Test Sample Points API
    points = test_endpoint(f"{BASE_URL}/api/v1/points/sample", "5. Sample Points & Density Weight Endpoint")
    assert points is not None, "Sample points endpoint test failed"

    # 6. Test Spatial Query Endpoint
    query_res = test_endpoint(f"{BASE_URL}/api/v1/spatial/query?q=Adilabad", "6. Spatial Attribute Query Endpoint (?q=Adilabad)")
    assert query_res is not None, "Spatial query endpoint test failed"

    print("\n================================================================")
    print(" ALL API ENDPOINT BENCHMARKS & SPATIAL VERIFICATIONS PASSED SUCCESSFUL")
    print("================================================================\n")

if __name__ == "__main__":
    main()
