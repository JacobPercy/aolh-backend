import os
import json
import base64

def encode_image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

def gm(memory_id: int):
    folder_name = f"m_{memory_id:03}"
    
    base_dir = "/Users/jacobpercy/Desktop/github/aolh-backend/memories"
    memory_path = os.path.join(base_dir, folder_name)

    if not os.path.isdir(memory_path):
        return {"error": f"Memory folder '{folder_name}' not found"}

    json_path = os.path.join(memory_path, "data.json")
    if not os.path.isfile(json_path):
        return {"error": f"Missing data.json in '{folder_name}'"}

    with open(json_path, "r") as f:
        memory = json.load(f)

    images = memory.get("media", {}).get("images", [])
    image_data = []
    for image_filename in images:
        image_path = os.path.join(memory_path, "images", image_filename)
        if os.path.isfile(image_path):
            image_data.append({
                "filename": image_filename,
                "data_base64": encode_image_to_base64(image_path)
            })

    memory["media"]["images_data"] = image_data
    return memory
