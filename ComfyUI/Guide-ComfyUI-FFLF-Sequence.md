# Guide to ComfyUI - FFLF Video Sequence

First Frame Last Frame (FFLF), or First Last Frame (FLF), is a method to create a video where its first and last frames match the images provided. Suppose you have several images that represent consecutive moments of the same scene. Instead of generating one single transition, we can use FFLF several times in sequence.

The idea is simple. If we have images $a_1, a_2, a_3, \ldots, a_n$, we generate one video from $a_1$ to $a_2$, another video from $a_2$ to $a_3$, and so on. At the end, we concatenate all generated frames into a single video.

For this application, we provide only the API workflow file. The reason is that the main logic is not inside a usual interactive ComfyUI session. The loop over several pairs of images is controlled by a Python script, not by the visual workflow itself. The ComfyUI workflow only describes one FFLF execution.

## Sequence logic

The full animation is built as a sequence of smaller FFLF transitions.

```text
Input images:

a1          a2          a3          a4
|-----------|-----------|-----------|
   FFLF 1      FFLF 2      FFLF 3

Executions:

1) a1 -> a2
2) a2 -> a3
3) a3 -> a4

Generated frames:

[a1 ... a2] + [a2 ... a3] + [a3 ... a4]
````

Since the last frame of one segment is also the first frame of the next segment, we remove the last frame of each intermediate segment. This avoids duplicating the transition frame.

```text
Before removing duplicated frames:

[a1 ... a2] + [a2 ... a3] + [a3 ... a4]

After removing duplicated frames:

[a1 ... before_a2] + [a2 ... before_a3] + [a3 ... a4]
```

This gives a smoother final sequence and avoids a small pause at the connection between clips.

## Tips

FFLF in ComfyUI is useful, but it has a clear limitation, it constrains the first and last frames much more strongly than the intermediate transition. Because of this, the motion between them can become abrupt, delayed, or inconsistent, especially when the two endpoint images are too different.

For a sequence of videos, this limitation becomes even more important. Each transition must work well by itself, but the transitions also need to connect naturally in the final video.

To reduce this problem, it is helpful to follow these guidelines:

1. **Use nearby frames:** Consecutive images should have minimal change and maximum visual continuity. The more different two images are, the harder the transition becomes.

2. **Write each prompt as a coherent temporal scene:** Describe the transition as a single evolving scene, using temporal language such as "slowly", "gradually", or "throughout the clip", so the model understands the intended progression from the first frame to the last frame.

3. **Keep the scene stable:** If the goal is to create a continuous sequence, avoid unnecessary changes in camera angle, background, lighting, character design, clothing, or composition.

4. **Use one prompt per transition:** The motion from $a_1$ to $a_2$ may be different from the motion from $a_2$ to $a_3$. Because of this, each pair of frames should have its own positive prompt.

For example, for a transition from a standing pose to a bowing pose, we could use:

*In a static anime scene viewed from a slightly elevated angle, three young men stand on a stone pavement. The blond man in a white suit begins with his arms crossed and then smoothly uncrosses his arms and leans forward into a polite bow. The pink-haired boy also tilts his head and upper body forward into a bow. The tall white-haired man in dark purple clothing remains mostly still with his hands in his pockets, showing only very subtle natural motion. Smooth continuous motion, consistent anatomy, consistent faces, consistent outfits, stable background, no camera movement.*

And for the opposite transition, we could use:

*In a static anime scene viewed from a slightly elevated angle, three young men stand on a stone pavement. The blond man in a white suit rises smoothly from a bowed position back to an upright posture and then places one hand on his hip in a relaxed manner. The pink-haired boy also lifts his head and upper body back up from the bow to a more upright position. The tall white-haired man in dark purple clothing remains mostly still with his hands in his pockets, with only subtle natural motion. Smooth continuous motion, consistent anatomy, consistent faces, consistent outfits, stable background, no camera movement.*

A possible negative prompt is:

*sudden change, abrupt transition, jump cut, flicker, morphing artifacts, extra fingers, deformed hand, missing fingers, warped face, distorted mouth, different character, identity change, background change, camera movement, blurry frames, inconsistent anatomy, duplicated objects*

## Practical example

Now we will see in practice how to execute a sequence of FFLF transitions with WAN in ComfyUI.

We will use the API workflow file [FFLF_Sequence.json](https://github.com/felipebottega/AI-Audiovisual-Lab/blob/main/ComfyUI/workflows-api/FFLF_Sequence.json). This file contains the logic for one FFLF execution. The sequence itself is controlled by the Python script.

In the script, the main object is the list `inputs`. Each element of this list describes one FFLF transition. For example, the first item can describe the transition from the first image to the second image, and the second item can describe the transition from the second image to the third image.

A simplified structure is:

```python
inputs = [
    # First video
    {
        "97": {
            "inputs": {
                "image": "path_to_first_image.png",
            }
        },
        "142": {
            "inputs": {
                "image": "path_to_second_image.png",
            }
        },
        "93": {
            "inputs": {
                "text": "positive prompt for the first transition",
            }
        },
        "89": {
            "inputs": {
                "text": "negative prompt",
            }
        }
    },

    # Second video
    {
        "97": {
            "inputs": {
                "image": "path_to_second_image.png",
            }
        },
        "142": {
            "inputs": {
                "image": "path_to_third_image.png",
            }
        },
        "93": {
            "inputs": {
                "text": "positive prompt for the second transition",
            }
        },
        "89": {
            "inputs": {
                "text": "negative prompt",
            }
        }
    },
]
```

The script will execute these items in order. After each execution, ComfyUI saves the generated PNG frames in the `frames` folder. When the current transition is not the last one, the script deletes the last generated frame. This avoids repeating the same endpoint frame in the final video.

At the end, all PNG files in the `frames` folder are joined into a single MP4 video.

You can use the script [FFLF_Sequence.py](https://github.com/felipebottega/AI-Audiovisual-Lab/blob/main/ComfyUI/scripts/FFLF_Sequence.py) for this example. If you want to add more transitions, just add more items to the `inputs` list. Then run the script with  `python FFLF_Sequence.py`.
