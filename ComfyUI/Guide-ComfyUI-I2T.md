# Guide to ComfyUI - Image to Text (I2T)

There are two main approaches to Image to Text conversion in the context of Stable Diffusion and ComfyUI. The distinction lies in how the model interprets the visual data and the format of the output.

- Natural Language Captioning (Standard): This approach generates a descriptive, human-readable sentence or paragraph. Models like BLIP or LLaVA analyze the scene and create a coherent text describing subjects, actions, and the environment. This is ideal for understanding the general composition or for converting images into descriptive prompts for image-to-image workflows.

- Booru-style Tagging (Danbooru way): This approach uses models trained on specific datasets (like Danbooru) to output a flat list of comma-separated tags (e.g., 1girl, solo, masterpiece, illustration, blue hair). These tags are highly optimized for AI image generation models that were trained on tagged datasets (like Pony Diffusion or older SD 1.5 models), as they focus on specific attributes rather than grammatical sentences.

Use Captioning (BLIP/LLaVA) when you need to understand what is happening in an image or need a descriptive summary of a photograph. Use Tagging (WD14 Tagger/DeepDanbooru) when your goal is to extract prompt tags from an existing image to recreate a similar style or character in a new generation, especially when working with anime or stylized models.

## Parameters 

- **Mode:** Defines the task. Caption produces a descriptive sentence. The mode *interrogate* expects a specific prompt (below the parameter) and returns an answer based on the visual input. The mode **caption* ignores the prompt and descrives the whole image at once.
- **Min/Max Length:** Controls the token count of the output. Setting these too low may truncate sentences; too high may lead to repetitive or "hallucinated" filler text.
- **Num Beams:** Specifies the number of "paths" the model explores to find the best sentence. Higher values (e.g., 5-10) improve quality and coherence but increase processing time.
- **No Repeat Ngram Size:** Prevents the model from repeating a sequence of N words. Setting this to 2 or 3 helps avoid repetitive loops in generated text.
- **Early Stopping:** When enabled, the model stops generating text as soon as it reaches an end-of-sentence token, optimizing speed and efficiency.

<p align="center">
    <img width="1000" src="https://github.com/user-attachments/assets/3775d7aa-45a1-4940-8708-9f0ccbf81101" />
    <img width="1000" src="https://github.com/user-attachments/assets/2ae85057-3e73-4bc6-989e-17c83d531c9e" />
</p>

## Practical example

Now we will see in practice how to execute an I2T workflow in ComfyUI. We will use the [img2img_canon.json](https://github.com/felipebottega/AI-Audiovisual-Lab/blob/main/ComfyUI/workflows/img2text_canon.json) file in this tutorial. You can consider it as a canonical I2T file that can be modified gradually according to your needs.

<p align="center">
    <img width="1100" src="https://raw.githubusercontent.com/felipebottega/AI-Audiovisual-Lab/refs/heads/main/assets/workflow_i2i.png" />
</p>

This JSON provides the workflow to be used in the ComfyUI interface. It's possible to automate the workflow's execution and change its parameters programmatically; to do this, you must use the API-specific JSON from [this link](https://github.com/felipebottega/AI-Audiovisual-Lab/blob/main/ComfyUI/workflows-api/img2text_canon.json). 

You can use the script [run_workflow.py](https://github.com/felipebottega/AI-Audiovisual-Lab/blob/main/ComfyUI/scripts/run_workflow.py) for this example. You can use the script [run_workflow.py](https://github.com/felipebottega/AI-Audiovisual-Lab/blob/main/ComfyUI/scripts/run_workflow.py) for this example. If you want to change any parameter, edit the JSON above and then run the scrip with the command `python run_workflow.py "{path_to_workflow_json}"` in the terminal.

The workflow file also includes some optional post-processing nodes: upscale and downscale, quantize. These nodes come right after VAE decode and before Save Image. I've already configured these optional nodes for the current example workflow. 

> This example uses the checkpoint called `pixelArtDiffusionXL_spriteShaper`, which creates pixel art style images. It's always necessary to divide the size of the generated image by 8 (with the *Image Resize* node) so that each pixel (simulated) has the correct size. The quantize node is used to limit the number of colors in the palette, which is also useful for pixel art.

<p align="center">
    <img width="600" src="https://github.com/user-attachments/assets/58d62148-2a1c-4955-b04f-9488039732db" />
</p>
