# Guide to ComfyUI - Pixel Art

In this tutorial, we will look at how to transform images into pixel art-style images. After generating the image, you can use BLIP to generate a prompt from it and use both the image and the prompt to feed another part of the workflow that will convert them into an animated pixel art video.

## Image to Image

In this first stage, we work exactly as described in the [image-to-image](https://github.com/felipebottega/AI-Audiovisual-Lab/blob/main/ComfyUI/Guide-ComfyUI-I2I.md) tutorial. That is, we need to provide an input image and a guidance prompt to the program, and it will generate the corresponding image. For this to work, it is necessary to use the `pixelArtDiffusionXL_spriteShaper` checkpoint, which was trained for this purpose.

<p align=center">
    <img width="1100" src="https://github.com/user-attachments/assets/7c895043-c886-4a65-a591-75cf5387c1ef" />
</p>

It's always necessary to divide the size of the generated image by 8 (with the Image Resize node) so that each pixel (simulated) has the correct size. The quantize node is used to limit the number of colors in the palette, which is also useful for pixel art (optional).

<p align="center">
    <img width="800" src="https://github.com/user-attachments/assets/4d63fb38-6a58-45ea-80ef-c647e6e15b28" />
    <img width="600" src="https://github.com/user-attachments/assets/58d62148-2a1c-4955-b04f-9488039732db" />
</p>


### Image to Text

Once the image is generated, it is automatically sent to BLIP, which then generates a prompt describing the image.
Note that there is also a *String to Text* node in this section. You can use this node to add more details to the prompt if you deem it necessary. Since BLIP only describes a static image, it does not provide movement instructions for the model that will generate the video. For this example, I used the following additional prompt:

``
The animation retains the original pixel art style with crisp pixel edges. The original composition and character proportions remain unchanged. Subtle natural motion, gentle blinking, slight hair and clothing movement. Smooth temporal consistency.
``

<p align="center">
    <img width="1100" src="https://github.com/user-attachments/assets/9a843528-cef4-4a98-b3e9-3eb1742ad871" />
</p>

### Image to Video

Finally, we move to the stage where the image (and the guidance prompt) serves as the basis for the video-generating model. At this phase, we proceed exactly as described in the [image-to-video](https://github.com/felipebottega/AI-Audiovisual-Lab/blob/main/ComfyUI/Guide-ComfyUI-I2V.md) tutorial. 

<p align="center">
    <img width="1100" src="https://github.com/user-attachments/assets/921a28d2-3966-4806-a356-9e8a2ee77543" />
</p>

The entire setup is the same, except that here we will use the `birdmanstyleanimationwanlora` LoRa, in addition to Wan's `lightx2v` LoRas. There is another LoRa specialized in pixel art that you can test later: the `wan2.2_animate_adapter_model`. I tested both LoRas, and they seem to work well.

<p align="center">
    <img width="800" src="https://github.com/user-attachments/assets/afa739bf-2e8f-40eb-abaa-d102d1ba8955" />
</p>

Once the model has generated the video internally, there are three paths you can take.

1. The first is the standard approach: proceed to *Create Video* and *Save Video*.

2. The second path is to select *Save Image*; instead of creating a video file, this generates a folder containing image files for every frame of the video. This allows for precise, frame-by-frame editing and enables the output to be used by other interfaces that generate animations from image sequences.

3. The third path involves scaling the video before generating it. The advantage of this method is the ability to produce videos in different formats, such as animated GIFs. In my tests, scaling reduced video quality, though this is not necessarily always the case.

Generally, the first path is the best choice, but you may find a need for the other two options at some point.

<p align="center">
    <img width="800" src="https://github.com/user-attachments/assets/019eae5c-88da-4247-b8ea-7e5625d0b4fe" />
</p>

> PS: The *Remove Background* node is there just in case. It is useful when you want to create character animations and need to remove the background.

Pixel art videos require absolute sharpness, but some video players might smooth out the image, potentially making the output look poor. It is worth keeping this in mind: the video itself might be perfectly sharp, but your player is misleading you. If you choose to save the PNGs (the second method), you can open them in *Aseprite* (or *LibreSprite*). In these programs, the frame sequence will render with true sharpness, allowing you to view the animation properly.

## Practical example

We can use the [pixelart.json](https://github.com/felipebottega/AI-Audiovisual-Lab/blob/main/ComfyUI/workflows/pixelart.json) file in this tutorial. You can consider it as a canonical file that can be modified gradually according to your needs.

This JSON provides the workflow to be used in the ComfyUI interface. It's possible to automate the workflow's execution and change its parameters programmatically; to do this, you must use the API-specific JSON from [this link](https://github.com/felipebottega/AI-Audiovisual-Lab/blob/main/ComfyUI/workflows-api/pixelart.json). 

You can use the script [run_workflow.py](https://github.com/felipebottega/AI-Audiovisual-Lab/blob/main/ComfyUI/scripts/run_workflow.py) for this example. If you want to change any parameter, edit the JSON above and then run the scriptwith the command `python run_workflow.py "{path_to_workflow_json}"`.
