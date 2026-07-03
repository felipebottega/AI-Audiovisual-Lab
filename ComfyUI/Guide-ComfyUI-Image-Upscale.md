# Guide to ComfyUI - Image Upscale

## Main nodes

Basically there are three to generate the upscale of an image. The first one, and the most basic, is the node *Upscale Image*. With this node, you are able to choose a method (*nearest-exact, bilinear, area, bicubic, lanczos*) and the target resolution.

<p align="center">
    <img width="300" src="https://github.com/user-attachments/assets/bb2b7469-311c-440b-b875-daa9cadd3620" />
</p>

The second one is the node called *Image Resize*. This is the one usually used in our examples. With this node, you are able to choose a method (*lanczos, nearest, bilinear, bicubic*). If the mode is set to *scale*, you can change the parameter *rescale_factor* to multiply the original resolution by this factor. In this mode the parameters *resize_width* and *resize_height* are ignored. The other method is the *resize*, where you just the parameters *resize_width* and *resize_height*.

<p align="center">
    <img width="320" src="https://github.com/user-attachments/assets/c59d2da6-70ba-43f5-984e-eb17c0539d34" />
</p>

The third one is the node *Upscale Image (using Model)*, which be use use in conjunction with the node *Load Upscale Model*. These model use AI to generate the upscale, instead of a deterministic algorithm. The biggest difference is that AI may create new detail in the image.

<p align="center">
    <img width="650" src="https://github.com/user-attachments/assets/3ed52c5e-99eb-4abc-b601-a241e3f32d8b" />
</p>

> PS: The 2x and 4x in the model name means the model will upscale the image by a factor of 2x or 4x, respectively. These factors can't be changed.

## Differences

Each method has its pros ands cons. I won't discuss this subject here, but I will leave the image below for reference.

<p align="center">
    <img width="1100" src="https://github.com/user-attachments/assets/e47b993d-0a69-4a50-8917-3363a3376e0b" />
</p>

## Practical example

You can use the [img_upscale.json](https://github.com/felipebottega/AI-Audiovisual-Lab/blob/main/ComfyUI/workflows/img_upscale.json) file in this tutorial. 

This JSON provides the workflow to be used in the ComfyUI interface. It's possible to automate the workflow's execution and change its parameters programmatically; to do this, you must use the API-specific JSON from [this link](https://github.com/felipebottega/AI-Audiovisual-Lab/blob/main/ComfyUI/workflows-api/img_upscale.json). 

You can use the script [run_workflow.py](https://github.com/felipebottega/AI-Audiovisual-Lab/blob/main/ComfyUI/scripts/run_workflow.py) for this example. If you want to change any parameter, edit the JSON above and then run the scriptwith the command `python run_workflow.py "{path_to_workflow_json}"`.
