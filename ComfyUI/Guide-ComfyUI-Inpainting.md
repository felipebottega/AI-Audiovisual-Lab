# Guide to ComfyUI - Inpainting

Image-to-Image, or I2I, is a generation method where the model receives an input image and uses it as a visual reference to create a new image. Instead of starting only from a text prompt, the workflow starts from an existing image and modifies it according to the prompt and the generation parameters.

This is useful when we want to preserve part of the original composition, pose, colors, or structure, while changing the style, details, lighting, background, or subject appearance. The strength of the transformation depends mainly on the denoise value: lower denoise values preserve more of the original image, while higher values allow stronger changes.

## Basic Workflow Diagram

```mermaid
flowchart LR
    A[Checkpoint] --> B[CLIP]
    B --> D
    A --> C[LoRAs] --> D[Sampler]
    E[Load Image] --> F[VAE Encode]
    D --> G[VAE Decode] --> H[Save Image]
    F --> D
    A --> F
    A --> G
```

## Required files

You only need a checkpoint file with the template. Optionally, you can have the LoRA files to apply. There are several templates and LoRAs available [here](https://civitai.com/), it will depend on your objective. 

## LoRAs

LoRAs (Low-Rank Adaptations) are small, specialized files used to modify or fine-tune a base checkpoint's behavior without altering the entire original model. In text-to-image (and text-to-video) workflows, they allow you to inject specific art styles, characters, poses, or structural concepts into your generation.

In ComfyUI, LoRAs are injected directly between the Checkpoint and the Sampler nodes. You can layer multiple LoRAs together, adjusting the strength of each individually to blend different styles or elements.

## Sampler

The Sampler is the core engine that removes random noise step-by-step to form the final image or video, guided by your prompt and settings. Key parameters in ComfyUI include:

* **Steps:** The number of denoising iterations. Standard models require 20–30 steps, while *Lightning* workflows need only 4–8 steps.
* **CFG Scale:** How strictly the model follows your prompt. Higher values force compliance but can cause artifacts, fast-sampling workflows typically use low values (1.0–2.0).
* **Sampler & Scheduler:** The mathematical algorithms used to denoise.
* **Denoise:** Controls how much of the input latent is replaced with noise (0-1), determining how strongly the model can modify the original image.

## Practical example

Now we will see in practice how to execute an I2I workflow in ComfyUI. We will use the [img2img_canon.json](https://github.com/felipebottega/AI-Audiovisual-Lab/blob/main/ComfyUI/workflows/img2img_canon.json) file in this tutorial. You can consider it as a canonical I2I file that can be modified gradually according to your needs.

<p align="center">
    <img width="1100" src="https://raw.githubusercontent.com/felipebottega/AI-Audiovisual-Lab/refs/heads/main/assets/workflow_i2i.png" />
</p>

This JSON provides the workflow to be used in the ComfyUI interface. It's possible to automate the workflow's execution and change its parameters programmatically; to do this, you must use the API-specific JSON from [this link](https://github.com/felipebottega/AI-Audiovisual-Lab/blob/main/ComfyUI/workflows-api/img2img_canon.json). 

You can use the script [run_workflow.py](https://github.com/felipebottega/AI-Audiovisual-Lab/blob/main/ComfyUI/scripts/run_workflow.py) for this example. If you want to change any parameter, edit the JSON above and then run the scriptwith the command `python run_workflow.py "{path_to_workflow_json}"`.

The workflow file also includes some optional post-processing nodes: upscale and downscale, quantize. These nodes come right after VAE decode and before Save Image. I've already configured these optional nodes for the current example workflow. 

> This example uses the checkpoint called `pixelArtDiffusionXL_spriteShaper`, which creates pixel art style images. It's always necessary to divide the size of the generated image by 8 (with the *Image Resize* node) so that each pixel (simulated) has the correct size. The quantize node is used to limit the number of colors in the palette, which is also useful for pixel art.

<p align="center">
    <img width="600" src="https://github.com/user-attachments/assets/58d62148-2a1c-4955-b04f-9488039732db" />
</p>
