# Theory

In this text we grouped many of the theory behind AI models used in this repository.

## How diffusion models work

A **diffusion model** is a type of generative AI that creates images or videos through an iterative denoising process. During training, the model learns how to recover visual information from data that has been progressively corrupted with random noise. During generation, it performs the reverse operation, starting from noise and gradually refining it over many steps into coherent visual content guided by conditioning inputs such as text prompts, images, or other control signals. This approach enables diffusion models to produce highly detailed and visually consistent results.

<p align="center">
    <img width="1100" src="https://github.com/user-attachments/assets/ad01adcb-d354-4162-bb88-5885452ac1de" />
</p>

## LoRA (Low-Rank Adaptation)

After understanding diffusion models, it is important to introduce how pre-trained networks can be adapted to new concepts, styles, or subjects without full retraining. This is where LoRA becomes relevant. **LoRA** (**Low-Rank Adaptation**) is a lightweight mechanism used to modify the behavior of a pre-trained model without retraining all of its parameters. Instead of updating the full set of model weights, LoRA freezes the original weights and injects small trainable modules in the form of low-rank matrix decompositions. These additional matrices learn the adaptation and are combined with the frozen weights during inference to subtly steer the model’s behavior. This approach makes LoRA memory-efficient, fast to train, and easy to share, enabling fine-tuning of large models for specific styles, characters, or visual domains using only a small fraction of the original model size.

<p align="center">
    <img width="900" src="https://github.com/user-attachments/assets/f8f533e5-863e-4569-9635-9373bc53b1b8" />
</p>
## Sampler

After understanding diffusion models and LoRAs, we need the component that actually runs the denoising loop: the **sampler**.

A sampler is responsible for turning random noise into an image by repeatedly applying the diffusion model over a sequence of steps. While the model defines *what* should be denoised, the sampler defines *how* that denoising process is executed over time. In practice, it is the part that makes generation actually happen, transforming theoretical denoising into a controlled iterative process that produces a final image.

## How it works

Generation starts from pure noise in latent space. At each step, the model predicts how the current noisy latent should be updated, and the sampler applies this update using a numerical method. Repeating this process gradually transforms noise into a structured image.

Different samplers, such as **Euler**, **Heun**, or **DPM++**, define different ways of approximating this update process, affecting sharpness, stability, and convergence speed.

## Automatic1111 vs ComfyUI

In **AUTOMATIC1111**, this appears mainly as **Sampling method** in the interface, where you directly choose the sampling algorithm.

In **ComfyUI**, the same idea is exposed through the **KSampler** node. It performs the sampling process as part of the workflow and combines the sampler choice with other generation controls such as steps, seed, CFG scale, and scheduler.

So the core concept is the same: both are selecting how the diffusion process is executed step by step. The difference is mostly in presentation and abstraction.

## Key controls

- **Steps**: number of refinement iterations
- **CFG Scale**: strength of prompt guidance
- **Sampler type**: update strategy, such as Euler or DPM++
- **Seed**: initial noise configuration

## Relationship to the full pipeline

Putting everything together:

- **Diffusion model**: defines the denoising behavior
- **LoRA**: modifies the model’s behavior in a lightweight way
- **Sampler / KSampler**: controls how denoising is applied over time

> PS: The "K" in KSampler comes from **Karras-style diffusion samplers**, a family of methods inspired by the work of **Tero Karras** and collaborators. These methods improved how noise schedules and step sizes are handled during sampling.
