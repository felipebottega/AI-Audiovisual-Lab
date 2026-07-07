# Guide to ComfyUI - IP-Adapter

*IP-Adapter* is ...

## Basic Workflow Diagram

This is the worflow for arbitrary checkpoints. 

```mermaid
flowchart LR
    A[Checkpoint] --> B[CLIP] --> C[Sampler]
    A --> D[LoRas] --> F[IPAdapter] --> C
    E[Load Image] --> F
    C --> G[VAE Decode] --> H[Save Image]
    A --> G
```

## Parameters

### Preset

The `preset` defines what kind of information the IP-Adapter tries to extract from the reference image. Some presets are better for general appearance, some for composition, and some are specialized for faces.

General presets:

| Preset | Main use | Practical note |
|---|---|---|
| `LIGHT` | Subtle reference influence | Good when the reference should only slightly guide the result. |
| `STANDARD` | General-purpose reference | Usually the safest starting point. Try this first before using stronger presets. |
| `VIT-G` | Richer visual reference | Can capture more details, but may also become harder to control. |
| `PLUS` | Stronger reference influence | Useful when `STANDARD` is too weak, but it can start copying the reference too much. |
| `PLUS (kolors general)` | General Kolors usage | Use mainly with Kolors-based workflows. |
| `REGULAR - FLUX and SD3.5 only` | Flux / SD3.5 workflows | Do not use this with normal SDXL or SD1.5 workflows. |
| `COMPOSITION` | Pose, layout, framing, structure | Useful when you care more about the image structure than the character identity or style. |

Face presets:

| Preset | Best for | Practical note |
|---|---|---|
| `PLUS FACE` | General portrait guidance | Good when you want the face to resemble the reference, but not necessarily preserve identity perfectly. |
| `FULL FACE` | Stronger portrait guidance | SD1.5 only. Stronger than `PLUS FACE`, but less flexible. |
| `FACEID` | Facial identity | Better when the goal is to preserve the identity of a person. |
| `FACEID PLUS` | Stronger facial identity | More aggressive than `FACEID`. Can help with consistency, but may reduce freedom. |
| `FACEID PLUS KOLORS` | Face identity with Kolors | Specific variant for Kolors workflows. |
| `FACEID PLUS V2` | Refined facial identity | Usually a better option when available, especially for identity consistency. |
| `FACEID PORTRAIT` | Portrait / style transfer | More focused on portrait appearance and style transfer than pure identity locking. |
| `FACEID PORTRAIT UNNORM` | Strong SDXL portrait transfer | SDXL only. Stronger and less normalized, so it can be powerful but also less predictable. |

A simple rule:

| Goal | Suggested preset |
|---|---|
| General visual reference | `STANDARD` |
| Stronger visual reference | `PLUS` |
| Keep the same face/person | `FACEID`, `FACEID PLUS`, or `FACEID PLUS V2` |
| Transfer pose/layout/composition | `COMPOSITION` |
| Light influence only | `LIGHT` |

### Weight

The `weight` controls how strongly the IP-Adapter pushes the generation toward the reference image. This is one of the most important parameters. A higher value does not simply mean “better consistency”. If the weight is too high, the IP-Adapter may start copying the reference image too literally. 

### Start At

The `start_at` value defines when the IP-Adapter starts influencing the denoising process. Early denoising steps define the large structure of the image: pose, layout, silhouette, camera angle, and general composition. Later steps refine details, textures, colors, and small visual features. Because of that, `start_at` changes the type of influence the reference image has.

| Start At | Effect |
|---|---|
| `0.0` | The reference influences the image from the beginning. Stronger effect on pose, layout, and structure. |
| `0.2` to `0.4` | A balanced range. The base model can establish the scene before the reference becomes stronger. |
| `0.5` to `0.7` | The reference mostly affects appearance, texture, and details. Less structural influence. |
| Very late | The reference may become too weak to meaningfully guide the image. |

The following image was provided to IP-Adapter to influence the given prompt. 

<p align="center">
    <img width="200" src="https://github.com/user-attachments/assets/7b80a02e-ab2d-4e6c-8eef-50c1c63d4969" />
    <img width="400" src="https://github.com/user-attachments/assets/dbd0f7b7-99fa-4744-b32f-3a7e409b2571" />
</p>

Below we have a grid of image resulting from the combination of weights (horizontal) and starting points (vertical). In all cases, the end point was set to 1, which means the Ip-Adapter influenced the denoising process until the end. Note that the later we allow the IP-Adapter to start influencing the process, the less relevant the weight value becomes.

<p align="center">
    <img width="1100" src="https://github.com/user-attachments/assets/24c52c29-22c4-4fc2-8f71-d68785f7c40c" />
</p>

> PS: In this examples we used the checkpoint *Juggernaut XL*, which is a realistic checkpoint.

### End At

The `end_at` value defines when the IP-Adapter stops influencing the denoising process. If `end_at` is set to `1.0`, the IP-Adapter remains active until the end of the generation. This usually preserves the reference more strongly. If it stops earlier, the model has more freedom in the final details.

| End At | Effect |
|---|---|
| `0.5` | The reference stops early. The model has more freedom afterward. |
| `0.7` to `0.9` | Balanced behavior. The reference guides the image but does not dominate until the final step. |
| `1.0` | The reference remains active until the end. Stronger preservation. |

A useful strategy is to control *when* the IP-Adapter acts instead of only changing the weight. For example:

| Problem | Possible adjustment |
|---|---|
| The result copies the reference pose too much | Increase `start_at` |
| The result copies the reference details too much | Decrease `end_at` or lower `weight` |
| The reference is barely visible | Lower `start_at`, increase `end_at`, or increase `weight` |
| The prompt is being ignored | Lower `weight` or shorten the active range |
| The image needs stronger identity preservation | Increase `weight` or keep `end_at` close to `1.0` |

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

Once you have finished painting, select the icon <img width="26" height="27" alt="image" src="https://github.com/user-attachments/assets/94719fde-aece-40fc-b992-455fff645ba7" /> to apply the mask. You should apply exactly over the area you painted the colors, which is the area you want to inpaint. When you click save, the file is saved to `ComfyUI\input\clipspace`, so you can reuse it later.

The final result is shown below.

<p align="center">
    <img width="300" src="https://github.com/user-attachments/assets/4be2dfa9-6e73-492d-8196-4417f8b3b577" />
</p>

Inpainting with normal checkpoints is not easy, you test several values for CFG, denoise, sampler, scheduler, expand and blur radius. In some tests I had good results with CFG as high as 16, so don't be shy to try extreme values. I also recommend using the grid script for inpainting for testing, this will accelerate your search for good parameters.

For inpainting, keep the prompt short and focused on the masked region. Describe only the object or change you want to generate, plus a few important visual details such as color, material, shape, or lighting. Avoid long prompts describing the entire image, since ComfyUI may lose quality or become confused with very large prompts. The prompt should guide what happens inside the mask, while the workflow should preserve the rest of the image.

> PS: Painting colors is not mandatory, one can just paint the mask and run the program.

## Qwen Inpainting Workflow

This workflow uses the Qwen model together with the *InstantX Inpainting ControlNet* to edit only a selected region of an input image. The basic idea is simple: we load an image, paint a mask over the region that should be changed, and let the model regenerate only that masked area according to the prompt. The unmasked area is kept from the original image by compositing the generated result back over the input image.

> PS: Use the file [inpainting.json](https://github.com/felipebottega/AI-Audiovisual-Lab/blob/main/ComfyUI/workflows/image_qwen_image_instantx_inpainting_controlnet.json) for the interactive workflow and [this one](https://github.com/felipebottega/AI-Audiovisual-Lab/blob/main/ComfyUI/workflows-api/image_qwen_image_instantx_inpainting_controlnet.json) for the API workflow.

The procedure is the same as before, except that this workflow uses only 4 steps in the sampler. This is because we are using the 4-step LoRA `Qwen-Image-Lightning-4steps-V1.0`.

This workflow is not just a generic checkpoint adapted for inpainting. Most of its models were trained specifically for this task. Because of that, the workflow is heavier and takes more time to run, but it can produce much better results in difficult cases. Even so, this does not mean that it will always be better. There are situations where the simpler approach works better, especially when the edit is small or the generic checkpoint already understands the object well. There is no universal rule: test both workflows and experiment with different parameters.

## Tips

### Iterate over the result

Inpainting is often an iterative process. Do not expect the perfect result in a single generation. A good strategy is to obtain a reasonable first result, save it, load it again in the inpainting workflow, and then improve smaller details step by step. For example, you can first generate the general object or shape, and then run inpainting again to fix borders, shadows, hands, texture, or small artifacts.

This process can also include switching between workflows. Sometimes the normal checkpoint workflow gives a better first approximation, while the Qwen workflow is better for refining the result. In other cases, the opposite happens. You can use one workflow to create the main edit and another one to polish the details.

### Use a mask larger than the object

The mask should usually be slightly larger than the exact region you want to change. If the mask is too tight, the model may not have enough space to blend the new content with the surrounding image. This can create hard borders, leftovers from the original object, or unnatural transitions.

For objects that interact with the environment, such as a hand holding a ball or a person sitting on a sofa, include some surrounding pixels in the mask. The model may need to modify contact regions, shadows, folds, or nearby contours.

### Adjust denoise according to the size of the change

Low denoise values preserve more of the original image, but they may leave visible traces of the old object. High denoise values allow stronger changes, but they also make the result less predictable. If the edit is small, start with moderate denoise. If you want to replace the masked content with something very different, you may need higher denoise.

A common problem is using a denoise value that is too low for a large semantic change. In this case, the model understands the prompt but cannot fully remove the original content.

### Keep the prompt focused

For inpainting, the prompt should focus on what must appear inside the masked region. Avoid describing the whole image again unless it is necessary. The model already receives the image as context, so a long prompt may confuse the edit.

A good prompt usually describes the new object, its position, material, color, and how it should blend with the image. For example, instead of writing a long description of the entire scene, write something like:

```text
a realistic orange basketball held by the hand, matching the original lighting and perspective
```

### Use visual guidance when the model is confused

Sometimes a mask and a prompt are not enough. If the model does not understand the shape, position, or scale of the object, paint a rough guide before applying the mask. The drawing does not need to be beautiful. A simple colored sketch can be enough to tell the model where the new object should be and how large it should be.

This is especially useful when inserting objects, changing poses, or creating contact between two elements, such as a hand holding an object.

### Do not rely on one seed

Inpainting is unstable. Two seeds with the same parameters may produce very different results. If the setup is almost working, test several seeds before changing the entire workflow. Sometimes the correct configuration is already there, but the current seed is bad.

### Preserve the original image with compositing

Even if the workflow is supposed to edit only the masked region, the generated image may contain small changes outside the mask. The *Image Composite Masked* node is useful because it pastes only the masked region from the generated image back onto the original image. This helps preserve the unmasked area exactly as it was.
