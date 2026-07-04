# Guide to ComfyUI - Inpainting

*Inpainting* is a technique used to replace or modify a masked region of an image while keeping the rest mostly unchanged. We will consider two workflows in this tutorial. The first one uses an arbitrary checkpoint to perform the inpainting, whereas the second one uses a diffusion model from the [*Qwen*](https://qwen.ai/home) ecosystem specifically trained for inpainting. 

In theory, any checkpoint can be used for inpainting. This makes the workflow simpler, but it also requires more trial and error until you find a good result. Most of this tutorial will be explained with this workflow in mind. At the end, we will see that the Qwen workflow only requires a few modifications.

## Basic Workflow Diagram

This is the worflow for arbitrary checkpoints. 

```mermaid
flowchart LR
    A[Checkpoint] --> B[CLIP] --> C[Sampler]
    D[Load Image] --> E[Grow and Blur Mask] --> G
    D --> F[VAE Encode] --> G[Set Latent Noise Mask] --> C
    H[VAE Decode] --> I[Image Composition Masked] --> J[Save Image]
    E --> I
    D --> I
    A --> C
    A --> F
    A --> H
    C --> H
```

## Grow and Blur Mask

This node adjusts the mask before the inpainting step. This is useful because the original mask is often too sharp or too tight around the region to be edited. Expanding and blurring the mask helps the model blend the new content with the surrounding pixels.

* **Expand:** increases or decreases the size of the mask. Positive values make the masked region larger, which gives the model more space to modify the image around the object. This is useful to avoid hard borders or visible leftovers from the original image.
* **Blur Radius:** softens the edges of the mask. A higher value creates a smoother transition between the edited region and the unchanged part of the image. This helps avoid sharp seams, but too much blur may affect areas that should remain unchanged.

## Image Composite Masked

This node pastes one image over another using a mask. In inpainting workflows, it is used because the model may slightly alter the entire image, not only the masked region. The node composites only the masked area from the generated result onto the original image, preserving the unmasked area exactly as it was.

* **x:** horizontal position where the source image will be pasted onto the destination image. Usually this is set to `0` when both images have the same size.
* **y:** vertical position where the source image will be pasted onto the destination image. Usually this is also set to `0` when both images have the same size.
* **Resize Source:** if enabled, the source image is resized to match the destination image before being composited. This is useful when the images may have different dimensions, but for standard inpainting workflows they usually already have the same size.

## Practical example

Now we will see in practice how to execute an inpainting workflow in ComfyUI. We will use the [inpainting.json](https://github.com/felipebottega/AI-Audiovisual-Lab/blob/main/ComfyUI/workflows/inpainting.json) file in this tutorial. You can consider it as a canonical file that can be modified gradually according to your needs.

<p align="center">
    <img width="1100" src="https://raw.githubusercontent.com/felipebottega/AI-Audiovisual-Lab/refs/heads/main/assets/workflow_inpainting.png" />
</p>

This JSON provides the workflow to be used in the ComfyUI interface. It's possible to automate the workflow's execution and change its parameters programmatically; to do this, you must use the API-specific JSON from [this link](https://github.com/felipebottega/AI-Audiovisual-Lab/blob/main/ComfyUI/workflows-api/inpainting.json). 

You can use the script [run_workflow.py](https://github.com/felipebottega/AI-Audiovisual-Lab/blob/main/ComfyUI/scripts/run_workflow.py) for this example. If you want to change any parameter, edit the JSON above and then run the scriptwith the command `python run_workflow.py "{path_to_workflow_json}"`.

For this example we use this image below. Our goal is to have the monster (Eddie, from Iron Maiden) hold a basketball.

<p align="center">
    <img width="400" src="https://github.com/user-attachments/assets/99bfb02d-ee70-4518-beaf-5c6916ac3b6e" />
</p>

First select the image in the *Load Image* node, right click on it and select *Open in Mask Editor | Image Canvas*. This will open an image editor as we can see below.

<table align="center">
  <tr>
    <td style="padding-right: 30px;">
      <img width="300" src="https://github.com/user-attachments/assets/f75bb2cd-3da0-4181-9836-f975e9a3e7cf" />
    </td>
    <td>
      <img width="700" src="https://github.com/user-attachments/assets/09fe473e-e2bf-4a1d-8aed-007d9b93c100" />
    </td>
  </tr>
</table>

Click on the *Color Selector* to choose a color and the select the icon <img width="29" height="31" alt="image" src="https://github.com/user-attachments/assets/0e643bd2-20df-4045-b804-9156097754ce" /> to start painting over the image. The idea is to give the model an idea of what you want. This is just a sketch. You can use as many colors and details as you want, but for this example we just used one color and a single shape for simplicity. 

<p align="center">
    <img width="300" src="https://github.com/user-attachments/assets/757859f8-d45f-49dc-8ca9-a06c2046d810" />
</p>

Once you have finished painting, select the icon <img width="26" height="27" alt="image" src="https://github.com/user-attachments/assets/94719fde-aece-40fc-b992-455fff645ba7" /> to apply the mask. You should apply exactly over the area you painted the colors, which is the area you want to inpaint. The final result is shown below.

<p align="center">
    <img width="300" src="https://github.com/user-attachments/assets/4be2dfa9-6e73-492d-8196-4417f8b3b577" />
</p>

Inpainting with normal checkpoints is not easy, you test several values for CFG, denoise, sampler, scheduler, expand and blur radius. In some tests I had good results with CFG as high as 16, so don't be shy to try extreme values. I also recommend using the grid script for inpainting for testing, this will accelerate your search for good parameters.

For inpainting, keep the prompt short and focused on the masked region. Describe only the object or change you want to generate, plus a few important visual details such as color, material, shape, or lighting. Avoid long prompts describing the entire image, since ComfyUI may lose quality or become confused with very large prompts. The prompt should guide what happens inside the mask, while the workflow should preserve the rest of the image.

> PS: Painting colors is not mandatory, one can just paint the mask and run the program.

## Qwen Inpainting Workflow

This workflow uses the Qwen model together with the *InstantX Inpainting ControlNet* to edit only a selected region of an input image. The basic idea is simple: we load an image, paint a mask over the region that should be changed, and let the model regenerate only that masked area according to the prompt. The unmasked area is kept from the original image by compositing the generated result back over the input image.

The main blocks are:

1. **Model loading**

   The workflow loads the Qwen image diffusion model, the Qwen text encoder, the Qwen VAE, and the InstantX Inpainting ControlNet.

2. **Image and mask**

   The input image is loaded with the standard `Load Image` node. By right-clicking this node and selecting `Open in Mask Editor`, we can paint the mask directly inside ComfyUI.

   In the mask:

   - the painted region is the area to be regenerated
   - the unpainted region is the area to be preserved

3. **Prompt conditioning**

   The positive prompt describes what should appear in the masked region. The negative prompt can be used to avoid unwanted objects, artifacts, bad anatomy, text, watermarks, or other defects.

4. **Inpainting ControlNet**

   The masked image and the mask are passed to the Qwen InstantX Inpainting ControlNet. This gives the sampler information about both the original image and the region that should be edited.

5. **Latent sampling**

   The image is encoded into latent space, the mask is applied as a latent noise mask, and the sampler generates the edited result. The denoise value is usually set to `1` in this workflow, because the mask controls where the generation is allowed to happen.

6. **Decode and composite**

   After sampling, the latent result is decoded back into an image. Then `ImageCompositeMasked` is used to paste the generated masked region over the original image.

   This final compositing step is important because diffusion models may slightly modify pixels outside the mask. By compositing the result with the original image, the workflow guarantees that the unmasked area remains unchanged.

In short, the workflow is:

```text
Load Image
  ↓
Paint Mask in Mask Editor
  ↓
Qwen Model + Text Encoder + VAE
  ↓
Qwen InstantX Inpainting ControlNet
  ↓
VAE Encode + Set Latent Noise Mask
  ↓
KSampler
  ↓
VAE Decode
  ↓
ImageCompositeMasked
  ↓
Save Image
