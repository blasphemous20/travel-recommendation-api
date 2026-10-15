import json
import threading
import time
import urllib.error
import urllib.request
import pandas as pd
import uvicorn

from app.main import app

# Start uvicorn server in a separate thread
config = uvicorn.Config(app, host="127.0.0.1", port=8002, log_level="error")
server = uvicorn.Server(config)
thread = threading.Thread(target=server.run)
thread.daemon = True
thread.start()
time.sleep(1.5)

base_url = "http://127.0.0.1:8002"


def make_request(method, path, body=None):
    url = f"{base_url}{path}"
    data = json.dumps(body).encode("utf-8") if body is not None else None
    headers = {"Content-Type": "application/json"} if body is not None else {}
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req) as resp:
            return resp.status, json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        err_content = e.read().decode("utf-8")
        try:
            return e.code, json.loads(err_content)
        except Exception:
            return e.code, err_content


print("=== 1. TEST GET /health ===")
status, res = make_request("GET", "/health")
assert status == 200, f"Expected 200, got {status}"
assert res["status"] == "success"
print("OK:", res)

print("\n=== 2. TEST GET /destinations ===")
status, res = make_request("GET", "/destinations")
assert status == 200, f"Expected 200, got {status}"
assert "destinations" in res
dest_count_initial = len(res["destinations"])
assert "image_url" in res["destinations"][0] and res["destinations"][0]["image_url"].startswith("http")
print(f"OK: Found {dest_count_initial} destinations. Sample first item:")
print(json.dumps(res["destinations"][0], indent=2))

print("\n=== 3. TEST GET /destinations/1 ===")
status, res = make_request("GET", "/destinations/1")
assert status == 200, f"Expected 200, got {status}"
assert res["id"] == 1
assert res["name"] == "Taman Mini Indonesia Indah"
assert "image_url" in res and res["image_url"].startswith("http")
print("OK:", json.dumps(res, indent=2))

print("\n=== 4. TEST POST /destinations ===")
new_dest_payload = {
    "name": "Kura Kura Ocean Park",
    "city": "Jepara",
    "country": "Indonesia",
    "address": "Pantai Kartini, Jepara, Jawa Tengah",
    "rating": 4.5,
    "review_count": 3200,
    "types": "tourist_attraction, park, aquarium",
    "latitude": -6.5925,
    "longitude": 110.6558,
    "culinary": 0,
    "culture": 0,
    "nature": 1,
    "shopping": 0,
    "adventure": 1,
    "history": 0,
    "family": 1
}
status, created_res = make_request("POST", "/destinations", new_dest_payload)
assert status == 201, f"Expected 201, got {status}: {created_res}"
created_id = created_res["id"]
assert created_id == 111, f"Expected ID 111, got {created_id}"
assert created_res["name"] == "Kura Kura Ocean Park"
print(f"OK (Status {status}): Created destination ID {created_id}:")
print(json.dumps(created_res, indent=2))

# Verify persistence in CSV
csv_df = pd.read_csv("app/data/destinations_clean.csv")
assert created_id in csv_df["id"].values, "Created ID not found in CSV!"
created_csv_row = csv_df[csv_df["id"] == created_id].iloc[0]
print(f"CSV persistence verified! category_count: {created_csv_row['category_count']}, review_log: {created_csv_row['review_log']:.4f}, rating_norm: {created_csv_row['rating_norm']:.4f}")

print(f"\n=== 5. TEST PUT /destinations/{created_id} ===")
update_payload = dict(new_dest_payload)
update_payload["name"] = "Kura Kura Ocean Park Renamed"
update_payload["rating"] = 4.7
status, updated_res = make_request("PUT", f"/destinations/{created_id}", update_payload)
assert status == 200, f"Expected 200, got {status}: {updated_res}"
assert updated_res["id"] == created_id, "ID must not change on update!"
assert updated_res["name"] == "Kura Kura Ocean Park Renamed"
assert updated_res["rating"] == 4.7
print(f"OK (Status {status}): Updated destination:")
print(json.dumps(updated_res, indent=2))

# Verify updated in CSV
csv_df = pd.read_csv("app/data/destinations_clean.csv")
assert csv_df[csv_df["id"] == created_id].iloc[0]["name"] == "Kura Kura Ocean Park Renamed"
print("CSV update persistence verified!")

print(f"\n=== 6. TEST DELETE /destinations/{created_id} ===")
status, delete_res = make_request("DELETE", f"/destinations/{created_id}")
assert status == 200, f"Expected 200, got {status}: {delete_res}"
assert delete_res["message"] == "Destination deleted successfully"
print(f"OK (Status {status}):", json.dumps(delete_res, indent=2))

# Verify deleted in CSV
csv_df = pd.read_csv("app/data/destinations_clean.csv")
assert created_id not in csv_df["id"].values, "Deleted ID still in CSV!"
assert len(csv_df) == dest_count_initial, f"Expected length {dest_count_initial}, got {len(csv_df)}"
print(f"CSV deletion verified! Length restored to {len(csv_df)}")

print("\n=== 7. TEST POST /recommend/cities ===")
rec_city_payload = {
    "interests": ["culture", "history"],
    "activity": "Exploration",
    "travel_type": "Solo",
    "top_n": 5
}
status, rec_city_res = make_request("POST", "/recommend/cities", rec_city_payload)
assert status == 200, f"Expected 200, got {status}: {rec_city_res}"
assert "recommendations" in rec_city_res
assert len(rec_city_res["recommendations"]) == 5
print("OK: Top 5 Recommended Cities:")
for r in rec_city_res["recommendations"]:
    assert "description" in r and len(r["description"]) > 10, f"Missing or short description for {r['city']}"
    assert "image_url" in r and r["image_url"].startswith("http"), f"Missing or invalid image_url for {r['city']}"
    print(f"  - {r['city']}, {r['country']}: {r['score']}%\n    Foto: {r['image_url']}\n    Deskripsi: {r['description'][:60]}...")

print("\n=== 8. TEST POST /recommend/destinations ===")
rec_dest_payload = {
    "city": "Yogyakarta",
    "interests": ["culture", "history"],
    "activity": "Exploration",
    "travel_type": "Solo",
    "top_n": 5
}
status, rec_dest_res = make_request("POST", "/recommend/destinations", rec_dest_payload)
assert status == 200, f"Expected 200, got {status}: {rec_dest_res}"
assert rec_dest_res["city"] == "Yogyakarta"
assert len(rec_dest_res["recommendations"]) == 5
print("OK: Top 5 Destinations in Yogyakarta:")
for r in rec_dest_res["recommendations"]:
    assert "image_url" in r and r["image_url"].startswith("http"), f"Missing or invalid image_url for {r['name']}"
    print(f"  - {r['name']}: {r['score']}% (Foto: {r['image_url']})")

print("\n=== 9. EDGE CASES ===")

print("\n9a. ID tidak ditemukan (GET 9999):")
status, res = make_request("GET", "/destinations/9999")
assert status == 404, f"Expected 404, got {status}"
print(f"OK: Status {status}, detail: {res['detail']}")

print("\n9b. ID tidak ditemukan (PUT 9999):")
status, res = make_request("PUT", "/destinations/9999", new_dest_payload)
assert status == 404, f"Expected 404, got {status}"
print(f"OK: Status {status}, detail: {res['detail']}")

print("\n9c. ID tidak ditemukan (DELETE 9999):")
status, res = make_request("DELETE", "/destinations/9999")
assert status == 404, f"Expected 404, got {status}"
print(f"OK: Status {status}, detail: {res['detail']}")

print("\n9d. Rating di luar 0-5 (rating = 6.0):")
bad_rating_payload = dict(new_dest_payload)
bad_rating_payload["rating"] = 6.0
status, res = make_request("POST", "/destinations", bad_rating_payload)
assert status == 400, f"Expected 400, got {status}"
print(f"OK: Status {status}, error handled properly: {res['message']}")

print("\n9e. Review count negatif (review_count = -10):")
bad_rev_payload = dict(new_dest_payload)
bad_rev_payload["review_count"] = -10
status, res = make_request("POST", "/destinations", bad_rev_payload)
assert status == 400, f"Expected 400, got {status}"
print(f"OK: Status {status}, error handled properly: {res['message']}")

print("\n9f. Kategori selain 0/1 (culinary = 2):")
bad_cat_payload = dict(new_dest_payload)
bad_cat_payload["culinary"] = 2
status, res = make_request("POST", "/destinations", bad_cat_payload)
assert status == 400, f"Expected 400, got {status}"
print(f"OK: Status {status}, error handled properly: {res['message']}")

print("\n9g. Name kosong (name = '   '):")
bad_name_payload = dict(new_dest_payload)
bad_name_payload["name"] = "   "
status, res = make_request("POST", "/destinations", bad_name_payload)
assert status == 400, f"Expected 400, got {status}"
print(f"OK: Status {status}, error handled properly: {res['message']}")

print("\n9h. Duplicate ID check (creating 2 items sequentially):")
status1, r1 = make_request("POST", "/destinations", new_dest_payload)
status2, r2 = make_request("POST", "/destinations", new_dest_payload)
assert status1 == 201 and status2 == 201
assert r1["id"] != r2["id"], f"Duplicate ID detected: {r1['id']} and {r2['id']}"
print(f"OK: Consecutive IDs created: {r1['id']} and {r2['id']}. Cleaning up test items...")
make_request("DELETE", f"/destinations/{r1['id']}")
make_request("DELETE", f"/destinations/{r2['id']}")

server.should_exit = True
print("\n>>> ALL TESTS PASSED SUCCESSFULLY! <<<")
