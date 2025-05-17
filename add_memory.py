import os
import json
import base64
from rake_nltk import Rake
import nltk
from nltk.corpus import stopwords

#nltk.download('stopwords')
#nltk.download('punkt')

BASE_DIR = "/Users/jacobpercy/Desktop/github/aolh-backend/memories"
TIMELINE_FILE = os.path.join(BASE_DIR, "timeline.json")

def get_next_id():
    existing = [
        int(folder.split("_")[1]) for folder in os.listdir(BASE_DIR)
        if folder.startswith("m_") and folder.split("_")[1].isdigit()
    ]
    next_id = max(existing) + 1 if existing else 1
    return f"m_{next_id:03}"

def decode_and_save_images(images_data, images_dir):
    saved_filenames = []
    os.makedirs(images_dir, exist_ok=True)
    for image in images_data:
        filename = image["filename"]
        image_bytes = base64.b64decode(image["data_base64"])
        path = os.path.join(images_dir, filename)
        with open(path, "wb") as f:
            f.write(image_bytes)
        saved_filenames.append(filename)
    return saved_filenames

def update_timeline_entry(memory_id, title, timestamp, thumbnail_filename):
    timeline = []
    if os.path.exists(TIMELINE_FILE):
        with open(TIMELINE_FILE, "r") as f:
            timeline = json.load(f)

    entry = {
        "id": memory_id,
        "title": title,
        "timestamp": timestamp,
        "thumbnail_base64": None
    }

    # Try to embed thumbnail
    thumb_path = os.path.join(BASE_DIR, memory_id, "images", thumbnail_filename)
    if os.path.isfile(thumb_path):
        with open(thumb_path, "rb") as img:
            entry["thumbnail_base64"] = base64.b64encode(img.read()).decode("utf-8")

    timeline.append(entry)
    timeline.sort(key=lambda x: x["timestamp"])

    with open(TIMELINE_FILE, "w") as f:
        json.dump(timeline, f, indent=2)

def extract_keywords(text, max_keywords=10):
    rake = Rake()
    rake.extract_keywords_from_text(text)
    keywords = rake.get_ranked_phrases()
    return keywords[:max_keywords]

def am(memory_data):
    memory_id = get_next_id()
    memory_folder = os.path.join(BASE_DIR, memory_id)
    os.makedirs(memory_folder, exist_ok=True)

    images_data = memory_data.get("media", {}).get("images_data", [])
    saved_filenames = decode_and_save_images(images_data, os.path.join(memory_folder, "images"))

    # Update media section with image filenames
    memory_data["id"] = memory_id
    memory_data["media"]["images"] = saved_filenames
    if "images_data" in memory_data["media"]:
        del memory_data["media"]["images_data"]

    # Extract keywords from description
    description = memory_data.get("description", "")
    keywords = extract_keywords(description)
    memory_data["keywords"] = keywords

    with open(os.path.join(memory_folder, "data.json"), "w") as f:
        json.dump(memory_data, f, indent=2)

    # Add to timeline
    update_timeline_entry(
        memory_id,
        memory_data.get("title", "Untitled"),
        memory_data.get("timestamp", ""),
        saved_filenames[0] if saved_filenames else ""
    )

    return {"status": "success", "id": memory_id}
