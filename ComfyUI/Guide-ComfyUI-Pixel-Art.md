# Guide to ComfyUI - Pixel Art

There are two main approaches to Image to Text conversion in the context of Stable Diffusion and ComfyUI. The distinction lies in how the model interprets the visual data and the format of the output.

- Natural Language Captioning (Standard): This approach generates a descriptive, human-readable sentence or paragraph. Models like BLIP or LLaVA analyze the scene and create a coherent text describing subjects, actions, and the environment. This is ideal for understanding the general composition or for converting images into descriptive prompts for image-to-image workflows.

- Booru-style Tagging (Danbooru way): This approach uses models trained on specific datasets (like Danbooru) to output a flat list of comma-separated tags (e.g., 1girl, solo, masterpiece, illustration, blue hair). These tags are highly optimized for AI image generation models that were trained on tagged datasets (like Pony Diffusion or older SD 1.5 models), as they focus on specific attributes rather than grammatical sentences.

Use Captioning (BLIP/LLaVA) when you need to understand what is happening in an image or need a descriptive summary of a photograph. Use Tagging (WD14 Tagger/DeepDanbooru) when your goal is to extract prompt tags from an existing image to recreate a similar style or character in a new generation, especially when working with anime or stylized models.

## Parameters 

### BLIP

- **Mode:** Defines the task. Caption produces a descriptive sentence. The mode *interrogate* expects a specific prompt (below the parameter) and returns an answer based on the visual input. The mode *caption* ignores the prompt and descrives the whole image at once.
- **Min/Max Length:** Controls the token count of the output. Setting these too low may truncate sentences; too high may lead to repetitive or "hallucinated" filler text.
- **Num Beams:** Specifies the number of "paths" the model explores to find the best sentence. Higher values (e.g., 5-10) improve quality and coherence but increase processing time.
- **No Repeat Ngram Size:** Prevents the model from repeating a sequence of N words. Setting this to 2 or 3 helps avoid repetitive loops in generated text.
- **Early Stopping:** When enabled, the model stops generating text as soon as it reaches an end-of-sentence token, optimizing speed and efficiency.

<p align="center">
    <img width="1000" src="https://github.com/user-attachments/assets/3775d7aa-45a1-4940-8708-9f0ccbf81101" />
    <img width="1000" src="https://github.com/user-attachments/assets/2ae85057-3e73-4bc6-989e-17c83d531c9e" />
</p>

### WD14

- **Model:** Selects the specific neural network architecture for image analysis. Different models are fine-tuned for various aesthetic styles (e.g., anime vs. photorealistic) or specific dataset categories.
- **Threshold:** The confidence level (0.0 to 1.0) required to accept a tag. Lower values include more (potentially inaccurate) descriptive details, higher values return only the most certain features.
- **Character Threshold:** A separate confidence threshold dedicated specifically to character identity tags. A higher value (e.g., 0.85) is recommended to prevent the model from misidentifying characters.
- **Replace Underscore:** When enabled, replaces the _ character in tags with spaces. This is useful for workflows that require natural text formatting rather than standard database tags.
- **Trailing Comma:** When enabled, appends a comma to the end of the final tag in the string.
- **Exclude Tags:** A field to list specific tags that should be ignored or removed from the output. This is effective for cleaning up unwanted noise like image quality keywords (e.g., "highres") or common subjects you wish to filter out.

## Practical example

We can use the [img2img_canon.json](https://github.com/felipebottega/AI-Audiovisual-Lab/blob/main/ComfyUI/workflows/img2txt_canon.json) file in this tutorial. You can consider it as a canonical I2T file that can be modified gradually according to your needs.

<p align="center">
    <img width="1100" src="https://raw.githubusercontent.com/felipebottega/AI-Audiovisual-Lab/refs/heads/main/assets/workflow_i2t.png" />
</p>

This JSON provides the workflow to be used in the ComfyUI interface. It's possible to automate the workflow's execution and change its parameters programmatically; to do this, you must use the API-specific JSON from [this link](https://github.com/felipebottega/AI-Audiovisual-Lab/blob/main/ComfyUI/workflows-api/img2txt_canon.json). 

You can use the script [run_workflow.py](https://github.com/felipebottega/AI-Audiovisual-Lab/blob/main/ComfyUI/scripts/run_workflow.py) for this example. You can use the script [run_workflow.py](https://github.com/felipebottega/AI-Audiovisual-Lab/blob/main/ComfyUI/scripts/run_workflow.py) for this example. If you want to change any parameter, edit the JSON above and then run the scrip with the command `python run_workflow.py "{path_to_workflow_json}"` in the terminal.
