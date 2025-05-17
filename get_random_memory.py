import os
import random
import json
import base64

def get_random_folder(directory):
    folders = [
        folder for folder in os.listdir(directory)
        if os.path.isdir(os.path.join(directory, folder))
    ]
    if folders:
        return os.path.join(directory, random.choice(folders))
    return None

def encode_image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

def rm():
    directory = "/Users/jacobpercy/Desktop/github/aolh-backend/memories"
    random_folder = get_random_folder(directory)
    if not random_folder:
        return {"error": "No memory folders found"}

    json_path = os.path.join(random_folder, "data.json")
    if not os.path.isfile(json_path):
        return {"error": f"Missing data.json in {random_folder}"}

    with open(json_path, "r") as f:
        memory = json.load(f)

    # Add base64-encoded image data
    images = memory.get("media", {}).get("images", [])
    image_data = []
    for image_filename in images:
        image_path = os.path.join(random_folder, "images", image_filename)
        if os.path.isfile(image_path):
            image_data.append({
                "filename": image_filename,
                "data_base64": encode_image_to_base64(image_path)
            })

    memory["media"]["images_data"] = image_data
    return memory
