# Guide to ComfyUI - Pose

## Introduction to ControlNet

*ControlNet* is a method for guiding image generation with additional visual information. Instead of relying only on the text prompt, it allows the diffusion model to follow a structural reference such as a pose map, depth map, edge image, segmentation mask, line drawing, etc.

In this tutorial, ControlNet is used with an OpenPose image. The pose map defines the position of the body, limbs, hands, and face, while the checkpoint and text prompt determine the character, clothing, style, lighting, and background. In other words, ControlNet controls the composition and structure without replacing the normal generation process.

## Basic Workflow Diagram

Below is the diagram for creating the pose. The *OpenPose Studio* branch is optional, it is only useful if you want to edit the pose before saving. We will discuss this further later on.

```mermaid
flowchart LR
    A[Load Image] --> B[DWPose Estimator] --> C[Save Image]
    B --> D[OpenPose Studio] --> E[Save Image]
```

This will create the pose, which is just a PNG file. After that you need to insert it in a ControlNet node of a txt2img or img2img workflow. We show both workflows below.

### OpenPose in a txt2img workflow

```mermaid
flowchart LR
    A[Checkpoint] --> B[CLIP]
    A --> C[LoRAs] --> D[Sampler]
    E[Image Settings] --> D
    D --> F[VAE Decode] --> G[Create Video] --> H[Save Image]
    A --> F
    B --> I[Apply ControlNet] --> D
    J[Load Image] --> I
    K[Load ControlNet Model] --> I
    A --> I
```



## Required files

https://huggingface.co/xinsir/controlnet-openpose-sdxl-1.0/blob/main/diffusion_pytorch_model.safetensors

## LoRAs

LoRAs (Low-Rank Adaptations) are small, specialized files used to modify or fine-tune a base checkpoint's behavior without altering the entire original model. In text-to-image (and text-to-video) workflows, they allow you to inject specific art styles, characters, poses, or structural concepts into your generation.

In ComfyUI, LoRAs are injected directly between the Checkpoint and the Sampler nodes. You can layer multiple LoRAs together, adjusting the strength of each individually to blend different styles or elements.

## Sampler

The Sampler is the core engine that removes random noise step-by-step to form the final image or video, guided by your prompt and settings. Key parameters in ComfyUI include:

* **Steps:** The number of denoising iterations. Standard models require 20–30 steps, while *Lightning* workflows need only 4–8 steps.
* **CFG Scale:** How strictly the model follows your prompt. Higher values force compliance but can cause artifacts, fast-sampling workflows typically use low values (1.0–2.0).
* **Sampler & Scheduler:** The mathematical algorithms used to denoise.

## Practical example

Now we will see in practice how to execute an T2I workflow in ComfyUI. We will use the [txt2img_canon.json](https://github.com/felipebottega/AI-Audiovisual-Lab/blob/main/ComfyUI/workflows/txt2img_canon.json) file in this tutorial. You can consider it as a canonical T2I file that can be modified gradually according to your needs.

<p align="center">
    <img width="1100" src="https://raw.githubusercontent.com/felipebottega/AI-Audiovisual-Lab/refs/heads/main/assets/workflow_t2i.png" />
</p>

This JSON provides the workflow to be used in the ComfyUI interface. It's possible to automate the workflow's execution and change its parameters programmatically; to do this, you must use the API-specific JSON from [this link](https://github.com/felipebottega/AI-Audiovisual-Lab/blob/main/ComfyUI/workflows-api/txt2img_canon.json). Below, we show the beginning and end of this JSON, just to give an idea of ​​how it is structured.

```
{
  "3": {
    "inputs": {
      "seed": 566510339945522,
      "steps": 20,
      "cfg": 5,
      "sampler_name": "euler",
      "scheduler": "normal",
      "denoise": 1,
      "model": [
        "11",
        0
      ],
      "positive": [
        "6",
        0
      ],
      "negative": [
        "7",
        0
      ],
      "latent_image": [
        "5",
        0
      ]
    },
    "class_type": "KSampler",
    "_meta": {
      "title": "KSampler"
    }
  },
 
  ...

"13": {
    "inputs": {
      "filename_prefix": "ComfyUI",
      "images": [
        "8",
        0
      ]
    },
    "class_type": "SaveImage",
    "_meta": {
      "title": "Save Image"
    }
  }
}
```

You can use the script [run_workflow.py](https://github.com/felipebottega/AI-Audiovisual-Lab/blob/main/ComfyUI/scripts/run_workflow.py) for this example. If you want to change any parameter, edit the JSON above and then run the scriptwith the command `python run_workflow.py "{path_to_workflow_json}"`.

The workflow file also includes some optional post-processing nodes: upscale and downscale, quantize. These nodes come right after VAE decode and before Save Image. I've already configured these optional nodes for the current example workflow. 

> This example uses the checkpoint called `pixelArtDiffusionXL_spriteShaper`, which creates pixel art style images. It's always necessary to divide the size of the generated image by 8 (with the *Image Resize* node) so that each pixel (simulated) has the correct size. The quantize node is used to limit the number of colors in the palette, which is also useful for pixel art.

<p align="center">
    <img width="600" src="https://github.com/user-attachments/assets/58d62148-2a1c-4955-b04f-9488039732db" />
</p>
