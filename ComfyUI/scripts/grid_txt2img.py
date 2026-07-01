import os
import json
import time
import datetime
import requests
from io import BytesIO
from urllib import request
from itertools import product
from PIL import Image, ImageDraw, ImageFont


# Server address.
SERVER_URL = "http://127.0.0.1:8188"

param1 = {"11": {"inputs": {"steps": [10, 20, 30, 50]}}}
param2 = {"3": {"inputs": {"cfg": [2, 7, 12, 20]}}}
api_json_file = "ComfyUI/user/default/workflows-api/txt2img_canon.json"
big_grid_file = f"ComfyUI/output/grid_{datetime.datetime.now().strftime('%Y-%m-%d-%H_%M_%S')}.png"


def find_leaf_list_paths(d, path=None):
    """
    Finds all paths whose final value is a list.

    Example:
        {"3": {"inputs": {"steps": [10, 20]}}}

    returns:
        [(("3", "inputs", "steps"), [10, 20])]
    """
    
    if path is None:
        path = []

    results = []

    if isinstance(d, dict):
        for key, value in d.items():
            results.extend(find_leaf_list_paths(value, path + [key]))

    elif isinstance(d, list):
        results.append((tuple(path), d))

    return results


def set_nested_value(d, path, value):
    """
    Sets d[path[0]][path[1]]...[path[-1]] = value.
    """
    
    current = d

    for key in path[:-1]:
        current = current[key]

    current[path[-1]] = value


def clean_value_for_filename(value):
    return str(value).replace(".", "")
    
    
def filename_prefix(workflow, filename):
        
    for x in workflow:
        if workflow[x]["class_type"] == "SaveImage":
            workflow[x]["inputs"]["filename_prefix"] = filename
            
    return workflow
    

def get_first_output_image(history_item):
    """
    Extracts the first image from a ComfyUI history item.
    """

    outputs = history_item.get("outputs", {})

    for node_id, node_output in outputs.items():
        if "images" in node_output and len(node_output["images"]) > 0:
            return node_output["images"][0]

    raise RuntimeError("No image output found in workflow history.")


def download_comfy_image(image_info):
    """
    Downloads an image from ComfyUI using the /view endpoint.
    """

    params = {
        "filename": image_info["filename"],
        "subfolder": image_info.get("subfolder", ""),
        "type": image_info.get("type", "output"),
    }

    resp = requests.get(f"{SERVER_URL}/view", params=params)
    resp.raise_for_status()

    return Image.open(BytesIO(resp.content)).convert("RGB")


def text_size(draw, text, font):
    bbox = draw.textbbox((0, 0), text, font=font)
    return bbox[2] - bbox[0], bbox[3] - bbox[1]


def make_big_grid(results, values1, values2, name1, name2, output_file):
    """
    Creates a 2D grid.

    Rows correspond to param1.
    Columns correspond to param2.
    """

    first_img = next(iter(results.values()))
    img_w, img_h = first_img.size

    label_w = 200
    label_h = 100

    grid_w = label_w + len(values2) * img_w
    grid_h = label_h + len(values1) * img_h

    grid = Image.new("RGB", (grid_w, grid_h), "white")
    draw = ImageDraw.Draw(grid)

    try:
        font = ImageFont.truetype("arial.ttf", 24)
        small_font = ImageFont.truetype("arial.ttf", 24)
    except:
        font = ImageFont.load_default()
        small_font = ImageFont.load_default()

    # Top-left label.
    draw.rectangle((0, 0, label_w, label_h), fill=(245, 245, 245), outline="gray")
    texts = [(f"{name2.upper()} →", label_h * 0.25), (f"{name1.upper()} ↓", label_h * 0.65)]

    for text, y_center in texts:
        tw, th = text_size(draw, text, small_font)
        x = (label_w - tw) // 2
        y = int(y_center - th // 2)
        draw.text((x, y), text, fill="black", font=small_font)

    # Column labels.
    for j, val2 in enumerate(values2):
        text = str(val2)
        tw, th = text_size(draw, text, font)

        x = label_w + j * img_w + img_w // 2 - tw // 2
        y = label_h // 2 - th // 2

        draw.text((x, y), text, fill="black", font=font)

    # Row labels.
    for i, val1 in enumerate(values1):
        text = str(val1)
        tw, th = text_size(draw, text, font)

        x = label_w // 2 - tw // 2
        y = label_h + i * img_h + img_h // 2 - th // 2

        draw.text((x, y), text, fill="black", font=font)

    # Images.
    for i, val1 in enumerate(values1):
        for j, val2 in enumerate(values2):
            img = results[(val1, val2)]

            x = label_w + j * img_w
            y = label_h + i * img_h

            grid.paste(img, (x, y))

    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    grid.save(output_file)


param1_paths = find_leaf_list_paths(param1)
param2_paths = find_leaf_list_paths(param2)

if len(param1_paths) != 1:
    raise ValueError(f"param1 should contain exactly one final list, but found {len(param1_paths)}.")

if len(param2_paths) != 1:
    raise ValueError(f"param2 should contain exactly one final list, but found {len(param2_paths)}.")

path1, values1 = param1_paths[0]
path2, values2 = param2_paths[0]

name1 = path1[-1]
name2 = path2[-1]

results = {}

for val1, val2 in product(values1, values2):
    val1_name = clean_value_for_filename(val1)
    val2_name = clean_value_for_filename(val2)

    filename = f"image_{name1}_{val1_name}_{name2}_{val2_name}"

    # Load the API JSON file.
    with open(api_json_file, "r", encoding="utf-8") as f:
        workflow = json.load(f)
        workflow = filename_prefix(workflow, filename)

    set_nested_value(workflow, path1, val1)
    set_nested_value(workflow, path2, val2)

    p = {"prompt": workflow}
    data = json.dumps(p).encode("utf-8")

    # Envia o workflow para execução.
    req = request.Request(f"{SERVER_URL}/prompt", data=data)
    resp = request.urlopen(req)
    prompt_id = json.load(resp)["prompt_id"]

    print(f"Executing {prompt_id} - {filename}")

    # Espera finalizar antes de enviar o próximo.
    while True:
        status = requests.get(f"{SERVER_URL}/history/{prompt_id}").json()

        if prompt_id in status and "outputs" in status[prompt_id]:
            break

        time.sleep(10)

    image_info = get_first_output_image(status[prompt_id])
    image = download_comfy_image(image_info)

    results[(val1, val2)] = image


make_big_grid(results=results, values1=values1, values2=values2, name1=name1, name2=name2, output_file=big_grid_file)

print(f"Finished. Grid saved at: {big_grid_file}")