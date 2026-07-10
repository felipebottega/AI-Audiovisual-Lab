import os
import json
import time
import datetime
import requests
import numpy as np
from pathlib import Path
from urllib import request
from itertools import product
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont

try:
    from moviepy import VideoFileClip, CompositeVideoClip, ImageClip, concatenate_videoclips
except ImportError:
    from moviepy.editor import VideoFileClip, CompositeVideoClip, ImageClip, concatenate_videoclips


### Constants ###
SERVER_URL = "http://127.0.0.1:8188"
API_JSON_FILE = "ComfyUI/user/default/workflows-api/vid2vid_canon.json"
BIG_GRID_FILE = f"ComfyUI/output/grid_{datetime.datetime.now().strftime('%Y-%m-%d-%H_%M_%S')}.mp4"
TEMP_VIDEO_DIR = "ComfyUI/output"


### Parameters ###

# Grid parameters.
param1 = {
    "86": {
        "inputs": {
            "cfg": [1, 2]
        }
    }
}
param2 = {
    "103": {
        "inputs": {
            "shift": [2, 5]
        }
    }
}

# Input parameters.
image_path = "...picture.png"
video_path = "...video.mp4"

# Optional parameters.
param_opt = {
    "93": {    
        "inputs": {
            "text":
                "A dark-haired woman wearing a red shirt and a red hat walks quietly through a clear modern city street. Bright direct sunlight, deep blue cloudless sky, crisp dry air, strong natural contrast, sharp visibility, clearly defined buildings in the distance, clean urban background, hard-edged sunlight and distinct shadows on the ground. No fog, no haze, no mist, no smoke, no overcast sky, no washed-out atmosphere. Smooth natural motion, stable character appearance."
        }
    },
    "89": {    
        "inputs": {
            "text":
                "Overexposure, static, blurred details, subtitles, paintings, pictures, still, overall gray, worst quality, low quality, JPEG compression residue, ugly, mutilated, redundant fingers, poorly painted hands, poorly painted faces, deformed, disfigured, deformed limbs, fused fingers, cluttered background, slow motion,fog, haze, mist, smoke, smog, overcast, cloudy sky, gray atmosphere, washed-out colors, low contrast, diffused light, volumetric fog, atmospheric perspective, blurry background"
        }
    }
}

# Video grid options.
LOOPS = 5
FPS = None          # None = use the FPS from the first video, or 24 if unavailable.
GAP = 0
LABEL_H = 64
LABEL_FONT_SIZE = 22
KEEP_TEMP_VIDEOS = True


### Functions ### 
def find_leaf_list_paths(d, path=None):
    """
    Finds all paths whose final value is a list.
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
    text = str(value)[:16]
    replacements = {
        "\\": "-",
        "/": "-",
        ":": "-",
        " ": "_",
        ".": "",
        ",": "",
        "(": "",
        ")": "",
    }

    for old, new in replacements.items():
        text = text.replace(old, new)

    return text

def set_filename_prefix(workflow, filename):
    """
    Sets filename_prefix in every output node that has this input.
    Works with SaveImage, SaveVideo, VideoCombine, and similar nodes.
    """
    changed = 0

    for node in workflow.values():
        if not isinstance(node, dict):
            continue

        inputs = node.get("inputs", {})

        if isinstance(inputs, dict) and "filename_prefix" in inputs:
            inputs["filename_prefix"] = filename
            changed += 1

    if changed == 0:
        print("Warning: no filename_prefix input found in workflow.")

    return workflow

def set_image_path(workflow, path):
    """
    Sets the path to the input image in LoadImage nodes only.
    Does not modify image links such as ["8", 0].
    """
    if path is None:
        return workflow

    changed = 0

    for node in workflow.values():
        if not isinstance(node, dict):
            continue

        if node.get("class_type") != "LoadImage":
            continue

        inputs = node.get("inputs", {})

        if isinstance(inputs, dict) and isinstance(inputs.get("image"), str):
            inputs["image"] = path
            changed += 1

    if changed == 0:
        print("Warning: no LoadImage node with image path found in workflow.")

    return workflow

def set_video_path(workflow, path):
    """
    Sets the path to the input video in LoadVideo nodes only.
    Does not modify video links such as ["143", 0].
    """
    if path is None:
        return workflow

    changed = 0

    for node in workflow.values():
        if not isinstance(node, dict):
            continue

        if node.get("class_type") != "LoadVideo":
            continue

        inputs = node.get("inputs", {})

        if isinstance(inputs, dict) and isinstance(inputs.get("file"), str):
            inputs["file"] = path
            changed += 1

    if changed == 0:
        print("Warning: no LoadVideo node with video path found in workflow.")

    return workflow

def apply_param_overrides(workflow, params, strict=True):
    """
    Applies fixed parameter overrides to a ComfyUI API workflow.
    """
    for node_id, node_data in params.items():
        if node_id not in workflow:
            if strict:
                raise KeyError(f"Node '{node_id}' not found in workflow.")
            workflow[node_id] = {}

        if not isinstance(node_data, dict):
            raise TypeError(f"Override for node '{node_id}' must be a dictionary.")

        for section_name, section_data in node_data.items():
            if section_name not in workflow[node_id]:
                if strict:
                    raise KeyError(f"Section '{section_name}' not found in node '{node_id}'.")
                workflow[node_id][section_name] = {}

            if not isinstance(section_data, dict):
                workflow[node_id][section_name] = section_data
                continue

            if not isinstance(workflow[node_id][section_name], dict):
                raise TypeError(
                    f"workflow['{node_id}']['{section_name}'] is not a dictionary."
                )

            for key, value in section_data.items():
                if strict and key not in workflow[node_id][section_name]:
                    raise KeyError(
                        f"Key '{key}' not found in workflow['{node_id}']['{section_name}']."
                    )

                workflow[node_id][section_name][key] = value

    return workflow

def get_first_output_video(history_item):
    """
    Extracts the first video-like output from a ComfyUI history item.
    Usually VideoCombine outputs videos under a key such as 'gifs'.
    """
    video_exts = {".mp4", ".webm", ".mov", ".mkv", ".gif"}
    outputs = history_item.get("outputs", {})

    for node_output in outputs.values():
        if not isinstance(node_output, dict):
            continue

        for value in node_output.values():
            if not isinstance(value, list):
                continue

            for item in value:
                if not isinstance(item, dict):
                    continue

                filename = item.get("filename", "")
                ext = Path(filename).suffix.lower()

                if ext in video_exts:
                    return item

    raise RuntimeError("No video output found in workflow history.")

def download_comfy_file(file_info, output_dir):
    """
    Downloads an output file from ComfyUI using the /view endpoint.
    """
    os.makedirs(output_dir, exist_ok=True)

    params = {
        "filename": file_info["filename"],
        "subfolder": file_info.get("subfolder", ""),
        "type": file_info.get("type", "output"),
    }

    resp = requests.get(f"{SERVER_URL}/view", params=params)
    resp.raise_for_status()

    local_path = Path(output_dir) / Path(file_info["filename"]).name

    with open(local_path, "wb") as f:
        f.write(resp.content)

    return str(local_path)

def get_font(size):
    for font_name in ["arial.ttf", "DejaVuSans-Bold.ttf", "DejaVuSans.ttf"]:
        try:
            return ImageFont.truetype(font_name, size)
        except Exception:
            pass

    return ImageFont.load_default()

def make_label_image(text, width, height=LABEL_H, font_size=LABEL_FONT_SIZE):
    """
    Creates a transparent RGBA label image with readable stroked text.
    """
    img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    bg = Image.new("RGBA", (width, height), (0, 0, 0, 120))
    img.alpha_composite(bg)

    draw = ImageDraw.Draw(img)

    current_size = font_size
    while current_size >= 10:
        font = get_font(current_size)
        bbox = draw.multiline_textbbox(
            (0, 0),
            text,
            font=font,
            spacing=4,
            stroke_width=2,
        )
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]

        if tw <= width - 20 and th <= height - 8:
            break

        current_size -= 2

    x = (width - tw) // 2
    y = (height - th) // 2

    draw.multiline_text(
        (x, y),
        text,
        fill="white",
        font=font,
        spacing=4,
        align="center",
        stroke_width=2,
        stroke_fill="black",
    )

    return img

def clip_subclip(clip, start, end):
    if hasattr(clip, "subclipped"):
        return clip.subclipped(start, end)
    return clip.subclip(start, end)

def clip_resize(clip, size):
    if hasattr(clip, "resized"):
        return clip.resized(size)
    return clip.resize(newsize=size)

def clip_position(clip, position):
    if hasattr(clip, "with_position"):
        return clip.with_position(position)
    return clip.set_position(position)

def clip_duration(clip, duration):
    if hasattr(clip, "with_duration"):
        return clip.with_duration(duration)
    return clip.set_duration(duration)

def make_video_grid(video_paths, values1, values2, name1, name2, output_file):
    """
    Creates a 2D video grid.
    Rows correspond to param1 and columns correspond to param2.
    Each cell receives a label with both parameter values.
    """
    rows = len(values1)
    cols = len(values2)

    clips = {}
    min_duration = None

    for i in range(rows):
        for j in range(cols):
            clip = VideoFileClip(video_paths[(i, j)])
            clips[(i, j)] = clip
            min_duration = clip.duration if min_duration is None else min(min_duration, clip.duration)

    first_clip = clips[(0, 0)]
    cell_w, cell_h = first_clip.size
    cell_w = int(cell_w)
    cell_h = int(cell_h)

    final_duration = min_duration * LOOPS
    final_fps = FPS or getattr(first_clip, "fps", None) or 24

    final_clips = []

    for i, val1 in enumerate(values1):
        for j, val2 in enumerate(values2):
            x = j * (cell_w + GAP)
            y = i * (cell_h + GAP)

            clip = clips[(i, j)]
            base = clip_subclip(clip, 0, min_duration)
            looped = concatenate_videoclips([base] * LOOPS)
            video = clip_position(clip_resize(looped, (cell_w, cell_h)), (x, y))

            label_text = f"{name1}={val1}\n{name2}={val2}"
            label_img = make_label_image(label_text, cell_w)
            label = ImageClip(np.array(label_img))
            label = clip_duration(label, final_duration)
            label = clip_position(label, (x, y + cell_h - LABEL_H - 8))

            final_clips.append(video)
            final_clips.append(label)

    canvas_w = cols * cell_w + (cols - 1) * GAP
    canvas_h = rows * cell_h + (rows - 1) * GAP

    final = CompositeVideoClip(final_clips, size=(canvas_w, canvas_h))

    print(f"Rendering {rows * cols} videos...")
    print(f"Grid: {rows} rows x {cols} columns")
    print(f"Cell size: {cell_w}x{cell_h}")
    print(f"Final resolution: {canvas_w}x{canvas_h}")

    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    final.write_videofile(
        output_file,
        codec="libx264",
        audio=False,
        fps=final_fps,
        preset="medium",
    )

    final.close()

    for clip in clips.values():
        clip.close()

def run_workflow_and_wait(workflow):
    p = {"prompt": workflow}
    data = json.dumps(p).encode("utf-8")

    req = request.Request(f"{SERVER_URL}/prompt", data=data)
    resp = request.urlopen(req)
    response = json.load(resp)

    if "prompt_id" not in response:
        raise RuntimeError(f"ComfyUI did not return a prompt_id: {response}")

    prompt_id = response["prompt_id"]

    while True:
        status = requests.get(f"{SERVER_URL}/history/{prompt_id}").json()

        if prompt_id in status and "outputs" in status[prompt_id]:
            return prompt_id, status[prompt_id]

        time.sleep(10)


### Execution ###
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

video_paths = {}

for i, val1 in enumerate(values1):
    for j, val2 in enumerate(values2):
        val1_name = clean_value_for_filename(val1)
        val2_name = clean_value_for_filename(val2)

        filename = f"video_{name1}_{val1_name}_{name2}_{val2_name}"

        with open(API_JSON_FILE, "r", encoding="utf-8") as f:
            workflow = json.load(f)
            workflow = set_filename_prefix(workflow, filename)
            workflow = set_image_path(workflow, image_path)
            workflow = set_video_path(workflow, video_path)
            workflow = apply_param_overrides(workflow, param_opt)

        set_nested_value(workflow, path1, val1)
        set_nested_value(workflow, path2, val2)

        print(f"Executing {filename}")
        prompt_id, history_item = run_workflow_and_wait(workflow)

        video_info = get_first_output_video(history_item)
        local_video = download_comfy_file(video_info, TEMP_VIDEO_DIR)
        video_paths[(i, j)] = local_video

make_video_grid(video_paths=video_paths, values1=values1, values2=values2, name1=name1, name2=name2, output_file=BIG_GRID_FILE)

if not KEEP_TEMP_VIDEOS:
    for path in video_paths.values():
        try:
            os.remove(path)
        except OSError:
            pass

print(f"Finished. Grid saved at: {BIG_GRID_FILE}")
