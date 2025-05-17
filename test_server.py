import requests
import json

#GPT testing stuff

BASE_URL = "http://localhost:5004"

sample_memories = [
    {
        "id": "m_001",
        "title": "Beach Day",
        "description": "Fun day at the beach with family.",
        "timestamp": "2020-07-01T12:00:00",
        "location": {"name": "Santa Monica", "coordinates": {"lat": 34.0195, "lng": -118.4912}},
        "tags": ["beach", "family", "summer"],
        "people": [{"name": "mom", "relation": "mother"}],
        "media": {"images": []},
        "keywords": ["beach", "family", "fun"]
    },
    {
        "id": "m_002",
        "title": "Graduation Day",
        "description": "Graduated from university with honors.",
        "timestamp": "2019-05-15T15:30:00",
        "location": {"name": "University Hall", "coordinates": {"lat": 40.7128, "lng": -74.006}},
        "tags": ["graduation", "university"],
        "people": [{"name": "dad", "relation": "father"}],
        "media": {"images": []},
        "keywords": ["graduation", "honors", "university"]
    },
    {
        "id": "m_003",
        "title": "Camping Trip",
        "description": "Weekend camping in the mountains.",
        "timestamp": "2021-09-10T10:00:00",
        "location": {"name": "Rocky Mountains", "coordinates": {"lat": 39.113, "lng": -105.358}},
        "tags": ["camping", "mountains", "nature"],
        "people": [{"name": "sister", "relation": "sibling"}],
        "media": {"images": []},
        "keywords": ["camping", "mountains", "nature"]
    },
    {
        "id": "m_004",
        "title": "Christmas Eve",
        "description": "Family dinner and gift exchange.",
        "timestamp": "2020-12-24T19:00:00",
        "location": {"name": "Home", "coordinates": {"lat": 0, "lng": 0}},
        "tags": ["christmas", "family", "holiday"],
        "people": [{"name": "grandma", "relation": "grandmother"}],
        "media": {"images": []},
        "keywords": ["christmas", "family", "gifts"]
    },
    {
        "id": "m_005",
        "title": "First Job",
        "description": "Started first job at the tech company.",
        "timestamp": "2018-08-01T09:00:00",
        "location": {"name": "Tech HQ", "coordinates": {"lat": 37.7749, "lng": -122.4194}},
        "tags": ["work", "job", "career"],
        "people": [{"name": "boss", "relation": "manager"}],
        "media": {"images": []},
        "keywords": ["job", "career", "work"]
    }
]

def upload_memories():
    url = f"{BASE_URL}/memory/upload"
    for mem in sample_memories:
        resp = requests.post(url, json=mem)
        print(f"Uploaded {mem['id']} - Status: {resp.status_code} - Response: {resp.json()}")

def get_random_memory():
    url = f"{BASE_URL}/memory/random"
    resp = requests.get(url)
    if resp.status_code == 200:
        with open("test1.json", "w") as f:
            json.dump(resp.json(), f, indent=2)
        print("Random memory saved to test1.json")
    else:
        print("Failed to get random memory")

def get_memory_by_id(memory_id):
    url = f"{BASE_URL}/memory/{memory_id}"
    resp = requests.get(url)
    if resp.status_code == 200:
        with open("test2.json", "w") as f:
            json.dump(resp.json(), f, indent=2)
        print(f"Memory {memory_id} saved to test2.json")
    else:
        print(f"Failed to get memory {memory_id}")

def get_timeline():
    url = f"{BASE_URL}/timeline"
    resp = requests.get(url)
    if resp.status_code == 200:
        with open("test3.json", "w") as f:
            json.dump(resp.json(), f, indent=2)
        print("Timeline saved to test3.json")
    else:
        print("Failed to get timeline")

def search_memories(query):
    url = f"{BASE_URL}/search"
    params = {"query": query, "n": 5}
    resp = requests.get(url, params=params)
    if resp.status_code == 200:
        with open("test4.json", "w") as f:
            json.dump(resp.json(), f, indent=2)
        print(f"Search results for '{query}' saved to test4.json")
    else:
        print("Failed to search memories")

if __name__ == "__main__":
    print("Uploading sample memories...")
    upload_memories()
    print("Fetching random memory...")
    get_random_memory()
    print("Fetching memory by ID m_002...")
    get_memory_by_id(2)
    print("Fetching timeline...")
    get_timeline()
    print("Searching memories for 'family'...")
    search_memories("family")
