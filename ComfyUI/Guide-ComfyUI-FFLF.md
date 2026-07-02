# Guide to ComfyUI - First Frame Last Frame (FFLF)

First Frame Last Frame (FFLF), or First Last Frame (FLF), is a method to create a video where its first and last frames match the images provided. Suppose you have two images that you want to use as initial and final frames of a certain scene or short video. It is possible to use Wan to create a transition video between both frames as first and last frame. The approach is very similar to the I2V workflow, but here we use two input images and the node *WanFirstLastFrametoVideo* instead of *WanImageToVideo*. This is the only difference between these workflows.

Below we show an example where we extracted the first and last frames of an existing video and fed them to the FFLF workflow.

<table>
  <tr>
    <td width="50%" align="center">
      <video src="https://github.com/user-attachments/assets/f72f73f7-c127-49b6-9f4b-bd843d48e103" width="100%" controls></video>
    </td>
    <td width="50%" align="center">
      <video src="https://github.com/user-attachments/assets/a4bf04b6-44f8-48b5-bd83-055fa88ae950" width="100%" controls></video>
    </td>
  </tr>
</table>

## Tips

FFLF in ComfyUI is useful, but it has a clear limitation, it constrains the first and last frames much more strongly than the intermediate transition. Because of this, the motion between them can become abrupt, delayed, or inconsistent, especially when the two endpoint images are too different.

To reduce this problem, it is helpful to follow these two guidelines:

1. **Write the prompt as a coherent temporal scene:** Describe the transition as a single evolving scene, using temporal language such as "slowly", "gradually", or "throughout the clip", so the model understands the intended progression from start to end.

2. **Break the animation into smaller segments:** Instead of connecting two very different frames at once, split the motion into shorter clips with minimal change and maximum visual continuity. This usually makes the interpolation smoother and more reliable.

For the previous example, we use the followinf prompt: *Fixed camera close-up of the same anime character in side profile. The video begins with the character biting his finger near his mouth. Then he slowly pulls his hand away from his mouth, revealing a small tooth held between his fingers. His expression gradually changes to a tense, painful, focused look. Preserve the same character, same hair, same skin tone, same background, same framing, same lighting, and same anime style. Smooth continuous motion, gradual transition from the first frame to the last frame, natural hand movement, subtle facial motion, coherent in-between frames.*

And here is the negative prompt: *sudden change, abrupt transition, jump cut, flicker, morphing artifacts, extra fingers, deformed hand, missing fingers, warped face, distorted mouth, different character, identity change, background change, camera movement, blurry frames, inconsistent anatomy, duplicated flower*


## Practical example

Now we will see in practice how to execute an FFLF workflow with WAN in ComfyUI. We will use the [FFLF.json](https://github.com/felipebottega/AI-Audiovisual-Lab/blob/main/ComfyUI/workflows/FFLF.json) file in this tutorial. You can consider it as a canonical FFLF file that can be modified gradually according to your needs.

<p align="center">
    <img width="1100" src="https://raw.githubusercontent.com/felipebottega/AI-Audiovisual-Lab/refs/heads/main/assets/workflow_fflf.png" />
</p>

This JSON provides the workflow to be used in the ComfyUI interface. It's possible to automate the workflow's execution and change its parameters programmatically, to do this, you must use the API-specific JSON from [this link](https://github.com/felipebottega/AI-Audiovisual-Lab/blob/main/ComfyUI/workflows-api/FFLF.json). 

You can use the script [run_workflow.py](https://github.com/felipebottega/AI-Audiovisual-Lab/blob/main/ComfyUI/scripts/run_workflow.py) for this example. If you want to change any parameter, edit the JSON above and then run the scriptwith the command `python run_workflow.py "{path_to_workflow_json}"` in the terminal.
