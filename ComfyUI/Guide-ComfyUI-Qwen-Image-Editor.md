# Guide to ComfyUI - Qwen Image Editor

*Qwen Image Edit* is an image editing model from the Qwen ecosystem designed to modify an existing image using natural language instructions. Instead of generating an image completely from scratch, it uses the input image as the main reference and applies the requested changes while trying to preserve the original composition, style, lighting, and visual coherence.

It can be used for tasks such as inpainting, object replacement, style changes, pose adjustments, background edits, outpainting-like expansions, and general image transformation. One of its strengths is that it can understand visual context very well, so it often works with simple prompts and can follow drawn guides, masks, or marked regions in the image.

However, Qwen Image Edit is not always perfectly literal. For precise edits, it is important to clearly describe what must change and what must stay the same. The prompt should usually define the input image as the source of truth and explicitly ask the model to preserve identity, pose, composition, lighting, outfit, background, or any other important element.

> PS: In this tutorial we will be working with *Qwen Image Editor 2509*. This number refers to the model release version, following a year-month style convention. Here, `25` means 2025 and `09` means September.

## Basic Workflow Diagram

This is the worflow for arbitrary checkpoints. 

```mermaid
flowchart LR
    A[Load Image 1] --> B[Image Edit Qwen 2509] --> F[Save Image]
    C[Load Image 2] --> B
    D[Load Image 3] --> B
    E[Prompt] --> B
```

The node `Image Edit Qwen 2509` is wrapper for a more complex subgraph of nodes. It is possible to access this subgraph by clicking on the expand icon on the upper right corner of the node. We will not discuss what is happening in this subgraph and will simply accept that it is working correctly.

<p align="center">
    <img width="300" src="https://github.com/user-attachments/assets/259573c5-3948-4d8c-83e2-59c9d0c2cfdd" />
    <img width="700" src="https://github.com/user-attachments/assets/04b4192a-e952-4133-bec6-132953e7aa0d" />
</p>

## How Qwen Image Edit Works

Qwen Image Edit combines the visual information from the input image with the instructions written in the prompt. The image provides the scene, composition, subject, pose, lighting, colors, and other visual details, while the prompt tells the model what should be changed, preserved, added, removed, or transformed. In this sense, the final result is not based on the prompt alone, but on the interaction between the image and the prompt.

For simple edits, one image is usually enough: the input image acts as the main source of truth, and the prompt describes the desired transformation. For example, when converting an anime illustration into a photorealistic image, the model reads the character, pose, outfit, expression, and framing from the original image, then tries to translate those elements into a realistic photographic style.

## Tips

Be clear about what must change and what must stay the same. Avoid vague prompts like “make it realistic” or “improve the image.” For controlled results, explicitly tell the model to preserve important elements such as identity, pose, outfit, expression, camera angle, background, and composition. When precision matters, drawn marks such as crosses, circles, arrows, or rough guides can help indicate where an edit should happen, but the prompt should also tell the model to remove those marks in the final image.

## Practical example

Now we will see in practice how to execute an inpainting workflow in ComfyUI. We will use the [IPAdapter.json](https://github.com/felipebottega/AI-Audiovisual-Lab/blob/main/ComfyUI/workflows/IPAdapter.json) file in this tutorial. You can consider it as a canonical file that can be modified gradually according to your needs.

<p align="center">
    <img width="1100" src="https://raw.githubusercontent.com/felipebottega/AI-Audiovisual-Lab/refs/heads/main/assets/workflow_IPAdapter.png" />
</p>

This JSON provides the workflow to be used in the ComfyUI interface. It's possible to automate the workflow's execution and change its parameters programmatically; to do this, you must use the API-specific JSON from [this link](https://github.com/felipebottega/AI-Audiovisual-Lab/blob/main/ComfyUI/workflows-api/IPAdapter.json). 

You can use the script [run_workflow.py](https://github.com/felipebottega/AI-Audiovisual-Lab/blob/main/ComfyUI/scripts/run_workflow.py) for this example. If you want to change any parameter, edit the JSON above and then run the scriptwith the command `python run_workflow.py "{path_to_workflow_json}"`.
