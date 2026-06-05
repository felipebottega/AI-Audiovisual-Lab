# ComfyUI - Introduction

ComfyUI is a powerful node-based interface for [Stable Diffusion](https://en.wikipedia.org/wiki/Stable_Diffusion). It uses a modular system where you build and customize your entire generation pipeline by connecting individual nodes. This approach is primarily used for creating AI-generated images and videos.

## Installation

You can download and install ComfyUI via [this link](https://comfy.org/download). I recommend following the steps shown on GitHub for installation as a *Windows Portable* ([direct link to download here](https://github.com/comfyanonymous/ComfyUI/releases/latest/download/ComfyUI_windows_portable_nvidia.7z)). No installation is required in this case, just extract the files, it's a standalone application. Once everything is ready, the folder should have the structure shown below.

<p align="center">
    <img width="350" src="https://github.com/user-attachments/assets/c79592be-31e6-48c4-9918-ddf390dea92b" />
</p>

## Configuration and features

### Low quality rendering zoom threshold

Go to *settings → Lite Graph → Low quality rendering zoom threshold* and set the value to 0.01. This will cause the program to render the content of the nodes even when zoomed out.

<p align="center">
    <img width="800" src="https://github.com/user-attachments/assets/dfc6c8c6-825d-472d-9a93-40c1f1a78975" />
</p>

### Precision

Go to *settings → Lite Graph*, enable the option *Disable default float widget rounding* and set the value of *Float widget rounding decimal places* to 6. This will cause the program to use more decimal places for float numbers.

<p align="center">
    <img width="800" src="https://github.com/user-attachments/assets/85af53ee-9d53-42bd-9009-7fe9275464bb" />
</p>

In the example below, we want to apply a rescale of 0.125. The default precision would change this value to 0.13, but with the configuration above it does what is expected. Note that it is necessary to use a float node for this.

<p align="center">
    <img width="700" src="https://github.com/user-attachments/assets/49424446-07db-4dda-ba40-093c98801d89" />
</p>

### Bypass

Nodes in purple won't be executed. To disable a node, simply right-click on it and select the Bypass option, as shown below.

<p align="center">
    <img width="400" src="https://github.com/user-attachments/assets/aebba792-fac5-4f9b-b793-88e253df8b71" />
</p>

### Groups
The background box (named *UPSCALE* in this example) serves only to create a visual separation of a group of nodes. To create one, simply right-click on the empty space and select the Add Group option.

<p align="center">
    <img width="700" alt="image" src="https://github.com/user-attachments/assets/7b1915aa-197b-447f-a0ae-d210a07259b2" />
    <img width="300" alt="image" src="https://github.com/user-attachments/assets/eae99386-0204-42ab-ba1a-477766bd27b7" />
</p>
