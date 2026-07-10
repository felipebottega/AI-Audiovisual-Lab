# Guide to ComfyUI - Video to Video (V2V)

*Video-to-Video* (V2V) uses an existing video as the main source of motion, timing, camera movement, and scene structure, then transforms or edits it according to a prompt or other control inputs. Depending on the workflow, V2V can restyle the whole video, replace subjects, refine details, or follow structural guides such as pose, depth, or edges (using *ControlNet*).

## Basic Workflow Diagram

The workflow is very similar to the I2V workflow, except that here instead 

```mermaid
flowchart LR
    A1[WAN 2.2 I2V High Noise Model] --> B1[Apply High Noise LoRAs] --> C1[Model SamplingSD3] --> D1[KSampler]
    A2[WAN 2.2 I2V Low Noise Model] --> B2[Apply Low Noise LoRAs] --> C2[Model SamplingSD3] --> D2[KSampler]
    D1 --> D2 --> E[VAE Decode] --> F[Create Video] --> G[Save Video]
    A3[Load Video] --> B3[Get Video Components] --> D3[Wan22FunControlToVideo] --> D1
    A4[Load CLIP] --> B4[Prompt] --> D3
    A5[Load VAE] --> D3
    A6[Load Image] --> D3
    A5 --> E
```

## Required files

For a standard ComfyUI setup, you usually need the following files:

- **`wan2.2_fun_control_high_noise_14B_fp8_scaled.safetensors`**  
  The high-noise diffusion model. It handles the early denoising stage, where the overall composition, motion, body structure, camera behavior, and response to the control video are established.

- **`wan2.2_fun_control_low_noise_14B_fp8_scaled.safetensors`**  
  The low-noise diffusion model. It handles the later refinement stage, improving details, textures, edges, facial features, and temporal consistency after the main structure has already been created.

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

Now we will see in practice how to execute an I2V workflow with WAN in ComfyUI. We will use the [vid2vid_canon.json](https://github.com/felipebottega/AI-Audiovisual-Lab/blob/main/ComfyUI/workflows/vid2vid_canon.json) file in this tutorial. You can consider it as a canonical I2V file that can be modified gradually according to your needs.

<p align="center">
    <img width="1100" src="https://raw.githubusercontent.com/felipebottega/AI-Audiovisual-Lab/refs/heads/main/assets/workflow_v2v.png" />
</p>

This JSON provides the workflow to be used in the ComfyUI interface. It's possible to automate the workflow's execution and change its parameters programmatically, to do this, you must use the API-specific JSON from [this link](https://github.com/felipebottega/AI-Audiovisual-Lab/blob/main/ComfyUI/workflows-api/vid2vid_canon.json). 

You can use the script [run_workflow.py](https://github.com/felipebottega/AI-Audiovisual-Lab/blob/main/ComfyUI/scripts/run_workflow.py) for this example. If you want to change any parameter, edit the JSON above and then run the scriptwith the command `python run_workflow.py "{path_to_workflow_json}"`.

The workflow file also includes some optional post-processing nodes: color and brightness node, upscale and downscale, background removal, and saving frames as PNG. These nodes come right after `VAE decode` and before `Create Video`.

<p align="center">
    <img width="1100" src="https://raw.githubusercontent.com/felipebottega/AI-Audiovisual-Lab/refs/heads/main/assets/workflow_i2v_optional.png" />
</p>
