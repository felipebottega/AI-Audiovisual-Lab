import os
import re
import json
import time
import shutil
import datetime
import requests
from pathlib import Path
from urllib import request

try:
    from moviepy import ImageSequenceClip
except ImportError:
    from moviepy.editor import ImageSequenceClip


### Constants ###
SERVER_URL = "http://127.0.0.1:8188"
API_JSON_FILE = "ComfyUI/user/default/workflows-api/FFLF_Sequence.json"
VIDEO_FILE = f"ComfyUI/output/FFLF_video_{datetime.datetime.now().strftime('%Y-%m-%d-%H_%M_%S')}.mp4"
TEMP_VIDEO_DIR = "ComfyUI/output"
FRAMES_PREFIX = "frames/frame"


### Parameters ###

# Input parameters.
inputs = [
    # First video
    {
        "97": {    # path to first frame
            "inputs": {
                "image": "C:\\Users\\Felipe\\Pictures\\Screenshots\\a1.png",
            }
        },
        "142": {
            "inputs": {
                "image": "C:\\Users\\Felipe\\Pictures\\Screenshots\\a2.png",
            }
        },
        "93": {    # positive prompt
            "inputs": {
                "text": "In a static anime scene viewed from a slightly elevated angle, three young men stand on a stone pavement. The blond man in a white suit begins with his arms crossed and then smoothly uncrosses his arms and leans forward into a polite bow. The pink-haired boy also tilts his head and upper body forward into a bow. The tall white-haired man in dark purple clothing remains mostly still with his hands in his pockets, showing only very subtle natural motion. Smooth continuous motion, consistent anatomy, consistent faces, consistent outfits, stable background, no camera movement.",
            }
        },
        "89": {    # negative prompt
            "inputs": {
                "text": "sudden change, abrupt transition, jump cut, flicker, morphing artifacts, extra fingers, deformed hand, missing fingers, warped face, distorted mouth, different character, identity change, background change, camera movement, blurry frames, inconsistent anatomy, duplicated flower",
            }
        }
    },
    # Second video
    {
        "97": {    # path to first frame
            "inputs": {
                "image": "C:\\Users\\Felipe\\Pictures\\Screenshots\\a2.png",
            }
        },
        "142": {
            "inputs": {
                "image": "C:\\Users\\Felipe\\Pictures\\Screenshots\\a3.png",
            }
        },
        "93": {    # positive prompt
            "inputs": {
                "text": "In a static anime scene viewed from a slightly elevated angle, three young men stand on a stone pavement. The blond man in a white suit rises smoothly from a bowed position back to an upright posture and then places one hand on his hip in a relaxed manner. The pink-haired boy also lifts his head and upper body back up from the bow to a more upright position. The tall white-haired man in dark purple clothing remains mostly still with his hands in his pockets, with only subtle natural motion. Smooth continuous motion, consistent anatomy, consistent faces, consistent outfits, stable background, no camera movement.",
            }
        },
        "89": {    # negative prompt
            "inputs": {
                "text": "sudden change, abrupt transition, jump cut, flicker, morphing artifacts, extra fingers, deformed hand, missing fingers, warped face, distorted mouth, different character, identity change, background change, camera movement, blurry frames, inconsistent anatomy, duplicated flower",
            }
        }
    },
]

# Optional parameters.
param_opt = {
    "143": {
        "inputs": {
            "width": 800,
            "height": 350
        }
    },
    "141": {
        "inputs": {
            "filename_prefix": FRAMES_PREFIX,
        }
    }
}

FPS = None          # None = use the FPS from the workflow, or 24 if unavailable.


### Functions ### 
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

def run_workflow_and_wait(workflow):
    """
    Sends one workflow to ComfyUI and waits until its history is available.
    """
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

def get_frames_dir():
    """
    Returns the output folder implied by the SaveImage filename prefix.
    """
    filename_prefix = param_opt["141"]["inputs"]["filename_prefix"]
    folder_name = str(filename_prefix).replace("\\", "/").split("/")[0]
    return os.path.join(TEMP_VIDEO_DIR, folder_name)

def get_output_prefix():
    """
    Returns the SaveImage filename prefix using forward slashes.
    """
    return str(param_opt["141"]["inputs"]["filename_prefix"]).replace("\\", "/")

def clean_frames_dir():
    """
    Deletes the frames folder and recreates it before starting the sequence.
    """
    frames_dir = Path(TEMP_VIDEO_DIR) / FRAMES_PREFIX.split("/")[0]

    if frames_dir.exists():
        shutil.rmtree(frames_dir)

    frames_dir.mkdir(parents=True, exist_ok=True)
    
    return

def frame_sort_key(path):
    """
    Sorts frame filenames by their numeric parts.
    """
    path = Path(path)
    numbers = [int(x) for x in re.findall(r"\d+", path.stem)]
    return numbers, path.name

def get_png_frames():
    """
    Collects all generated PNG frames in ComfyUI output order.
    """
    frames_dir = Path(get_frames_dir())
    frames = list(frames_dir.glob("*.png"))

    if not frames:
        prefix = get_output_prefix()

        if "/" not in prefix:
            frames = list(Path(TEMP_VIDEO_DIR).glob(f"{prefix}*.png"))

    return sorted(frames, key=frame_sort_key)

def delete_last_frame():
    """
    Removes the last frame to avoid duplicating the transition frame.
    """
    frames = get_png_frames()

    if not frames:
        raise RuntimeError("No PNG frames found to delete.")

    os.remove(frames[-1])
    print(f"Deleted last frame: {frames[-1]}")

def get_workflow_fps():
    """
    Reads the video FPS from the workflow unless FPS was manually set.
    """
    if FPS is not None:
        return FPS

    with open(API_JSON_FILE, "r", encoding="utf-8") as f:
        workflow = json.load(f)

    return workflow.get("94", {}).get("inputs", {}).get("fps", 24)

def make_video_from_frames(output_file):
    """
    Builds the final MP4 from the generated PNG frames.
    """
    frames = get_png_frames()

    if not frames:
        raise RuntimeError("No PNG frames found to create the final video.")

    fps = get_workflow_fps()

    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    clip = ImageSequenceClip([str(frame) for frame in frames], fps=fps)

    clip.write_videofile(output_file, codec="libx264", audio=False, fps=fps, preset="medium")

    clip.close()


### Execution ###
# Start with a clean frames folder.
clean_frames_dir()

for i, param_input in enumerate(inputs):
    # Load a fresh workflow for each FFLF transition.
    with open(API_JSON_FILE, "r", encoding="utf-8") as f:
        workflow = json.load(f)
        workflow = apply_param_overrides(workflow, param_input)
        workflow = apply_param_overrides(workflow, param_opt)

    print(f"Executing video {i + 1}/{len(inputs)}")
    prompt_id, history_item = run_workflow_and_wait(workflow)

    # Remove the duplicated endpoint frame between consecutive transitions.
    if i < len(inputs) - 1:
        delete_last_frame()

# Join all generated PNG frames into a single final video.
make_video_from_frames(VIDEO_FILE)

print(f"Finished. Video saved at: {VIDEO_FILE}")
