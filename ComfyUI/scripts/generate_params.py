import os
import sys
import json


workflow_path = sys.argv[1]    # workflow-api json
output_path = sys.argv[2]    # parameters json


if not os.path.exists(workflow_path):
    sys.exit(f"Error: File {workflow_path} not found.")

with open(workflow_path, "r", encoding="utf-8") as f:
    workflow = json.load(f)

params = {
    "path_to_input": "",
    "path_to_output": "ComfyUI"
}

target_fields = {
    "KSampler": ["seed", "steps", "cfg", "denoise"],
    "CLIPTextEncode": ["text"],
    "EmptyLatentImage": ["width", "height", "batch_size"],
    "LoraLoaderModelOnly": ["strength_model"]
}

for node_id, node_data in workflow.items():
    class_type = node_data.get("class_type")
    
    if class_type in target_fields:
        node_inputs = node_data.get("inputs", {})
        extracted_inputs = {}

        for field in target_fields[class_type]:
            if field in node_inputs:
                if not isinstance(node_inputs[field], list):
                    extracted_inputs[field] = node_inputs[field]

        if extracted_inputs:
            params[node_id] = {"inputs": extracted_inputs}

with open(output_path, "w", encoding="utf-8") as f:
    json.dump(params, f, indent=4, ensure_ascii=False)

print(f"File '{output_path}' was generated correctly.")
