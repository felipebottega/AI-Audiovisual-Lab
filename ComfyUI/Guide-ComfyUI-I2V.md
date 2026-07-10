# Guide to ComfyUI - Image to Video (I2V)

*Image-to-Video* (I2V) starts from a reference image and animates it according to the prompt, making it better for preserving a specific character, composition, outfit, or art style.

## Basic Workflow Diagram

Although WAN 2.2 internally uses separate high-noise and low-noise stages, most ComfyUI workflows expose these stages as distinct nodes and checkpoints. The image and prompt are first converted into conditioning information, then the generation process is split into two phases. The outputs of these stages are combined to produce the final video. In Lightning workflows, specialized LoRAs are often applied to both stages, allowing the model to generate high-quality results with very few sampling steps.

```mermaid
flowchart LR
    A1[WAN 2.2 I2V High Noise Model] --> B1[Apply High Noise LoRAs] --> C1[Model SamplingSD3] --> D1[KSampler]
    A2[WAN 2.2 I2V Low Noise Model] --> B2[Apply Low Noise LoRAs] --> C2[Model SamplingSD3] --> D2[KSampler]
    D1 --> D2 --> E[VAE Decode] --> F[Create Video] --> G[Save Video]
    A3[Load Image] --> B3[WanImageToVideo] --> D1
    A4[Load CLIP] --> B4[Prompt] --> B3
    A5[Load VAE] --> B3
    A5 --> E
```

## Required files

For a standard ComfyUI setup, you usually need the following files:

- **`wan2.2_i2v_high_noise_14B_fp8_scaled.safetensors`**  
  The high-noise checkpoint. It is responsible for the first part of the diffusion process, where the model decides motion, composition, and broad structure.

- **`wan2.2_i2v_low_noise_14B_fp8_scaled.safetensors`**  
  The low-noise checkpoint. It refines the video after the main structure is already in place.

- **`wan2.2_i2v_lightx2v_4steps_lora_v1_high_noise.safetensors`**
  The high-noise Lightx2V LoRA. It is applied to the high-noise checkpoint and helps the model achieve good results with fewer sampling steps, reducing generation time while preserving the overall motion and structure.

- **`wan2.2_i2v_lightx2v_4steps_lora_v1_low_noise.safetensors`**
  The low-noise Lightx2V LoRA. It is applied to the low-noise checkpoint and helps maintain visual quality during the refinement stage when using low step counts.

- **`umt5_xxl_fp8_e4m3fn_scaled.safetensors`**  
  The text encoder. It converts the prompt into features the model can use.

- **VAE file**  
  Usually the VAE provided for WAN 2.2 / WAN 2.1-compatible workflows. The VAE is what helps decode the latent representation into an actual image/video output.

- **Optional LoRA files**  
  Used to add style, motion, realism, or other visual behaviors without retraining the full model.

> A latent representation is a compressed version of an image or video that preserves its most important visual information. WAN 2.2 performs diffusion in this compressed space for efficiency, and the VAE later converts it back into normal pixels.

## Practical example

Now we will see in practice how to execute an I2V workflow with WAN in ComfyUI. We will use the [img2vid_canon.json](https://github.com/felipebottega/AI-Audiovisual-Lab/blob/main/ComfyUI/workflows/img2vid_canon.json) file in this tutorial. You can consider it as a canonical I2V file that can be modified gradually according to your needs.

<p align="center">
    <img width="1100" src="https://raw.githubusercontent.com/felipebottega/AI-Audiovisual-Lab/refs/heads/main/assets/workflow_i2v_vikings.png" />
</p>

This JSON provides the workflow to be used in the ComfyUI interface. It's possible to automate the workflow's execution and change its parameters programmatically, to do this, you must use the API-specific JSON from [this link](https://github.com/felipebottega/AI-Audiovisual-Lab/blob/main/ComfyUI/workflows-api/img2vid_canon.json). Below, we show the beginning and end of this JSON, just to give an idea of ​​how it is structured.

```
{
  "84": {
    "inputs": {
      "clip_name": "umt5_xxl_fp8_e4m3fn_scaled.safetensors",
      "type": "wan",
      "device": "default"
    },
    "class_type": "CLIPLoader",
    "_meta": {
      "title": "Load CLIP"
    }
  },
 
  ...

  "126": {
    "inputs": {
      "lora_name": "wan2.2_i2v_lightx2v_4steps_lora_v1_low_noise.safetensors",
      "strength_model": 1.0000000000000002,
      "model": [
        "96",
        0
      ]
    },
    "class_type": "LoraLoaderModelOnly",
    "_meta": {
      "title": "LoraLoaderModelOnly"
    }
  }
}
```

You can use the script [run_workflow.py](https://github.com/felipebottega/AI-Audiovisual-Lab/blob/main/ComfyUI/scripts/run_workflow.py) for this example. If you want to change any parameter, edit the JSON above and then run the scriptwith the command `python run_workflow.py "{path_to_workflow_json}"`.

The workflow file also includes some optional post-processing nodes: color and brightness node, upscale and downscale, background removal, and saving frames as PNG. These nodes come right after `VAE decode` and before `Create Video`.

<p align="center">
    <img width="1100" src="https://raw.githubusercontent.com/felipebottega/AI-Audiovisual-Lab/refs/heads/main/assets/workflow_i2v_optional.png" />
</p>
