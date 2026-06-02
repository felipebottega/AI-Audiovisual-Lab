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

## KSampler (Sampling Process)

A **KSampler** (K-Diffusion Sampler) is responsible for turning random noise into an image by repeatedly applying the diffusion model over a sequence of steps. While the model defines how to denoise, the sampler defines how this denoising process is *executed over time*. In practice, the KSampler is what makes generation *actually happen*, turning theoretical denoising into a controlled iterative process that produces usable outputs.

In practice, generation starts from pure noise in the latent space, and the KSampler progressively refines it. At each step, the model predicts how the current noisy latent should be updated, and the sampler applies this update using a chosen numerical method. Repeating this process gradually transforms noise into a structured image.

Different samplers (such as Euler, Heun, or DPM++) define different ways of approximating this update process, affecting sharpness, stability, and convergence speed.

Key controls of a KSampler include:

- **Steps**: number of refinement iterations  
- **CFG Scale**: strength of prompt guidance  
- **Sampler type**: update strategy (e.g., Euler, DPM++)  
- **Seed**: initial noise configuration  

In summary, the KSampler is the mechanism that *orchestrates the denoising process*, defining how the diffusion model is applied step by step until an image is formed.

### Relationship to the full pipeline

Putting everything together:

- **Diffusion model:** Defines the denoising behavior.  
- **LoRA:** Modifies the model’s behavior in a lightweight way.  
- **KSampler:** Controls how denoising is applied over time.

> PS: The "K" in KSampler comes from **Karras-style diffusion samplers**, a family of methods inspired by work from Tero Karras and collaborators. These methods improved how noise schedules and step sizes are handled during sampling.
