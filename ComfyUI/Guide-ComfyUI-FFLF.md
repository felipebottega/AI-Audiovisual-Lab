# Guide to ComfyUI - First Frame Last Frame (FFLF)

Suppose you have tow images that you want to use as initial and final frame of a certain scene or short video. It is possible to use Wan to create a video connectiong both frames as first and last frame.

<table>
  <tr>
    <td width="50%" align="center">
      <video src="https://github.com/user-attachments/assets/f72f73f7-c127-49b6-9f4b-bd843d48e103" width="100%" controls></video>
    </td>
    <td width="50%" align="center">
      <video src="https://github.com/user-attachments/assets/c4642c94-fa2b-43c1-bfa7-5fd9920d5422" width="100%" controls></video>
    </td>
  </tr>
</table>

## Practical example

Now we will see in practice how to execute an T2V workflow with WAN in ComfyUI. We will use the [txt2vid_canon.json](https://github.com/felipebottega/AI-Audiovisual-Lab/blob/main/ComfyUI/workflows/txt2vid_canon.json) file in this tutorial. You can consider it as a canonical T2V file that can be modified gradually according to your needs.

<p align="center">
    <img width="1100" src="https://raw.githubusercontent.com/felipebottega/AI-Audiovisual-Lab/refs/heads/main/assets/workflow_t2v.png" />
</p>

This JSON provides the workflow to be used in the ComfyUI interface. It's possible to automate the workflow's execution and change its parameters programmatically, to do this, you must use the API-specific JSON from [this link](https://github.com/felipebottega/AI-Audiovisual-Lab/blob/main/ComfyUI/workflows-api/txt2vid_canon.json). 

You can use the script [run_workflow.py](https://github.com/felipebottega/AI-Audiovisual-Lab/blob/main/ComfyUI/scripts/run_workflow.py) for this example. If you want to change any parameter, edit the JSON above and then run the scriptwith the command `python run_workflow.py "{path_to_workflow_json}"` in the terminal.

The workflow file also includes some optional post-processing nodes: color and brightness node, upscale and downscale, background removal, and saving frames as PNG. These nodes come right after `VAE decode` and before `Create Video`.

<p align="center">
    <img width="1100" src="https://raw.githubusercontent.com/felipebottega/AI-Audiovisual-Lab/refs/heads/main/assets/workflow_i2v_optional.png" />
</p>
