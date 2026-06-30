# Guide to ComfyUI - Image Grid

In this tutorial, we will how to create 2D parameter grid with ComfyUI and a Python script. Since ComfyUI is more "node oriented", the interface is not friendly to loops. However, we can use the workflow in API format to make requests using a Python script. 

## API JSON file

All API JSON files are contained in the folder `workflows-api` of this repository. For example, below we have the beggining of the file https://github.com/felipebottega/AI-Audiovisual-Lab/blob/main/ComfyUI/workflows-api/txt2img_canon.json:

```
{
  "3": {
    "inputs": {
      "seed": 566510339945522,
      "steps": 20,
      "cfg": 5,
      "sampler_name": "euler",
      "scheduler": "normal",
      "denoise": 1,
      "model": [
        "11",
        0
      ],
      "positive": [
        "6",
        0
      ],
      "negative": [
        "7",
        0
      ],
      "latent_image": [
        "5",
        0
      ]
    },
    "class_type": "KSampler",
    "_meta": {
      "title": "KSampler"
    }
  },
  "4": {
    "inputs": {
      "ckpt_name": "pixelArtDiffusionXL_spriteShaper.safetensors"
    },
    "class_type": "CheckpointLoaderSimple",
    "_meta": {
      "title": "Load Checkpoint"
    }
  },
```

As mentioned in many other tutorials, you can use the script [run_workflow.py](https://github.com/felipebottega/AI-Audiovisual-Lab/blob/main/ComfyUI/scripts/run_workflow.py) to run the API JSON workflows with the command `python run_workflow.py "{path_to_workflow_json}"` in the terminal. However, editing the parameters manually in the JSON is not ideal. Now we introduce another script, which will change up to two parameters in a list of values and execute the workflow programatically.


