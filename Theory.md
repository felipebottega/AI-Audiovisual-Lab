# Theory

In this text we grouped many of the theory behind AI models used in this repository.

## How diffusion models work

A **diffusion model** is a type of generative AI that creates images or videos through an iterative denoising process. During training, the model learns how to recover visual information from data that has been progressively corrupted with random noise. During generation, it performs the reverse operation, starting from noise and gradually refining it over many steps into coherent visual content guided by conditioning inputs such as text prompts, images, or other control signals. This approach enables diffusion models to produce highly detailed and visually consistent results. [1]

<p align="center">
    <img width="1100" src="https://github.com/user-attachments/assets/ad01adcb-d354-4162-bb88-5885452ac1de" />
</p>

### Image Space vs Latent Space

When we look at an image, we see pixels. However, most modern diffusion models do not perform the denoising process directly in pixel space. Instead, the input is first compressed into a lower-dimensional representation called **latent space**. This latent representation preserves the most important visual information while requiring far less memory and computation. [2]

The diffusion process then operates on these latents rather than the original pixels. Once denoising is complete, the latent representation is decoded back into an image or video frame. This approach makes generation significantly more efficient while maintaining high visual quality. For this reason, models such as Stable Diffusion and many modern video diffusion models are often referred to as **latent diffusion models**. [2]

## LoRA (Low-Rank Adaptation)

After understanding diffusion models, it is important to introduce how pre-trained networks can be adapted to new concepts, styles, or subjects without full retraining. This is where LoRA becomes relevant. **LoRA** (**Low-Rank Adaptation**) is a lightweight mechanism used to modify the behavior of a pre-trained model without retraining all of its parameters. Instead of updating the full set of model weights, LoRA freezes the original weights and injects small trainable modules in the form of low-rank matrix decompositions. These additional matrices learn the adaptation and are combined with the frozen weights during inference to subtly steer the model’s behavior. This approach makes LoRA memory-efficient, fast to train, and easy to share, enabling fine-tuning of large models for specific styles, characters, or visual domains using only a small fraction of the original model size. [3]

<p align="center">
    <img width="900" src="https://github.com/user-attachments/assets/f8f533e5-863e-4569-9635-9373bc53b1b8" />
</p>

## Sampler

After understanding diffusion models and LoRAs, we need the component that actually runs the denoising loop, the **sampler**.

A sampler is responsible for turning random noise into an image by repeatedly applying the diffusion model over a sequence of steps. While the model defines *what* should be denoised, the sampler defines *how* that denoising process is executed over time. In practice, it is the part that makes generation actually happen, transforming theoretical denoising into a controlled iterative process that produces a final image.

### How it works

Generation starts from pure noise in latent space. At each step, the model predicts how the current noisy latent should be updated, and the sampler applies this update using a numerical method. Repeating this process gradually transforms noise into a structured image.

Different samplers, such as **Euler**, **Heun**, or **DPM++**, define different ways of approximating this update process, affecting sharpness, stability, and convergence speed.

### Automatic1111 vs ComfyUI

In **AUTOMATIC1111**, this appears mainly as **Sampling method** in the interface, where you directly choose the sampling algorithm.

In **ComfyUI**, the same idea is exposed through the **KSampler** node. It performs the sampling process as part of the workflow and combines the sampler choice with other generation controls such as steps, seed, CFG scale, and scheduler.

So the core concept is the same: both are selecting how the diffusion process is executed step by step. The difference is mostly in presentation and abstraction.

### Key controls

- **Steps**: number of refinement iterations
- **CFG Scale**: strength of prompt guidance
- **Sampler type**: update strategy, such as Euler or DPM++
- **Seed**: initial noise configuration

### Relationship to the full pipeline

Putting everything together:

- **Diffusion model**: defines the denoising behavior
- **LoRA**: modifies the model’s behavior in a lightweight way
- **Sampler / KSampler**: controls how denoising is applied over time

> PS: The "K" in KSampler comes from **Karras-style diffusion samplers**, a family of methods inspired by the work of **Tero Karras** and collaborators. These methods improved how noise schedules and step sizes are handled during sampling. [6]

## Checkpoints

A **checkpoint** is a saved state of a trained model. It contains the learned weights that determine how the model interprets prompts and performs the denoising process during generation. Depending on the ecosystem, it can appear as a single file such as `.ckpt` or `.safetensors`, or as a Diffusers-style folder where the components are stored separately. See the [Hugging Face docs](https://huggingface.co/docs/diffusers/en/using-diffusers/other-formats) for the main format differences.

A checkpoint is not a different kind of model. It is the model at a specific saved state. That is why checkpoints are used to resume training, compare variants, or run inference with one particular learned behavior. See the [Hugging Face docs](https://huggingface.co/docs/hub/en/models-uploading) for more on model uploads and saved model states.

### Checkpoints for images

The focus of a checkpoint for images is spatial structure: shapes, textures, lighting, composition, and prompt alignment inside a single frame. Latent diffusion models were built around this image-synthesis setting, using denoising in latent space instead of working directly in pixel space. [2]

### Checkpoints for videos

A checkpoint for videos has to do everything an image checkpoint does, but it also has to keep frames temporally consistent. A video model is not only asked to produce good individual frames, it must also preserve motion, continuity, and object identity across time. In practice, many video diffusion models start from a pretrained image model and add temporal layers, or use a space-time U-Net that models space and time together. [4]

### What is a U-Net?

The U-Net is the backbone network that usually performs the denoising step. The original architecture uses a contracting path to capture context and a symmetric expanding path to recover detail, with skip connections between matching resolutions. In diffusion models, that makes U-Net a good fit for estimating the reverse step of the process, which is why it became the default backbone in early DDPM-style models and later latent diffusion models. [5]

In simple terms: the checkpoint is the saved brain, and the U-Net is the part of that brain that learns how to clean noise step by step. The difference between image and video checkpoints is mostly in what that brain was trained to understand: a single frame, or a sequence of frames with time consistency. [4]

## References

[1]: https://arxiv.org/abs/2006.11239 "Denoising Diffusion Probabilistic Models — Jonathan Ho, Ajay Jain, Pieter Abbeel (2020)"

[2]: https://arxiv.org/abs/2112.10752 "High-Resolution Image Synthesis with Latent Diffusion Models — Robin Rombach, Andreas Blattmann, Dominik Lorenz, Patrick Esser, Björn Ommer (2022)"

[3]: https://arxiv.org/abs/2106.09685 "LoRA: Low-Rank Adaptation of Large Language Models — Edward J. Hu, Yelong Shen, Phillip Wallis, Zeyuan Allen-Zhu, Yuanzhi Li, et al. (2021)"

[4]: https://arxiv.org/abs/2311.15127 "Stable Video Diffusion: Scaling Latent Video Diffusion Models to Large Datasets — Andreas Blattmann, et al. (2023)"

[5]: https://arxiv.org/abs/1505.04597 "U-Net: Convolutional Networks for Biomedical Image Segmentation — Olaf Ronneberger, Philipp Fischer, Thomas Brox (2015)"

[6]: https://arxiv.org/abs/2206.00364 "Elucidating the Design Space of Diffusion-Based Generative Models — Tero Karras, Miika Aittala, Timo Aila, Samuli Laine, et al. (2022)"
