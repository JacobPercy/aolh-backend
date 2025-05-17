import os
import json
import base64

BASE_DIR = "/Users/jacobpercy/Desktop/github/aolh-backend/memories"

def encode_image_to_base64(image_path):
    with open(image_path, "rb") as img:
        return base64.b64encode(img.read()).decode("utf-8")

def gt():
    timeline = []

    for folder in os.listdir(BASE_DIR):
        folder_path = os.path.join(BASE_DIR, folder)
        if not os.path.isdir(folder_path) or not folder.startswith("m_"):
            continue

        json_path = os.path.join(folder_path, "data.json")
        if not os.path.isfile(json_path):
            continue

        with open(json_path, "r") as f:
            data = json.load(f)

        images = data.get("media", {}).get("images", [])
        thumbnail_data = None
        if images:
            thumb_path = os.path.join(folder_path, "images", images[0])
            if os.path.isfile(thumb_path):
                thumbnail_data = encode_image_to_base64(thumb_path)

        timeline.append({
            "id": data.get("id", folder),
            "title": data.get("title", "Untitled Memory"),
            "timestamp": data.get("timestamp", ""),
            "thumbnail_base64": thumbnail_data
        })

    timeline.sort(key=lambda x: x["timestamp"])
    return timeline
