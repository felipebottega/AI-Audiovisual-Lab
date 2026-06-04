import os
import sys
import json
import time
import requests
from urllib import request


SERVER_URL = "http://127.0.0.1:8188"    # Local server address.
workflow_filepath = sys.argv[1]
parameters_filepath = sys.argv[2]


def update_workflow(workflow, params):
    for key, value in params.items():
        if key in ["path_to_input", "path_to_output"]:
            continue
        if key not in workflow:
            raise KeyError(f"Workflow key not found: {key}")
        if isinstance(value, dict):
            workflow.setdefault(key, {})
            update_workflow(workflow[key], value)
        else:
            workflow[key] = value   


# Loads the workflow from the JSON file (workflows-api).
with open(workflow_filepath, "r", encoding="utf-8") as f:
    workflow = json.load(f)
    
# Loads the parameters.
with open(parameters_filepath, "r", encoding="utf-8") as f:
    params = json.load(f)
    
    if "path_to_input" not in params.keys():
        sys.exit("Parameter path_to_input missing")
    else:
        for x in workflow:
            if workflow[x]['class_type'] == 'LoadImage':
                workflow[x]['inputs']['image'] = params["path_to_input"]
            
    if "path_to_output" not in params.keys():
        sys.exit("Parameter path_to_output missing")
    else:
        for x in workflow:
            if workflow[x]['class_type'] == 'SaveVideo':
                workflow[x]['inputs']['filename_prefix'] = params["path_to_output"]

update_workflow(workflow, params)
        
p = {"prompt": workflow}
data = json.dumps(p).encode('utf-8')

# Send workflow to execution.
req =  request.Request(f"{SERVER_URL}/prompt", data=data)
resp = request.urlopen(req)
prompt_id = json.load(resp)["prompt_id"]
print(f'Executing {prompt_id} - {params["path_to_input"]}')

# Wait to finish.
while True:
    status = requests.get(f"{SERVER_URL}/history/{prompt_id}").json()
    
    if prompt_id in status and "outputs" in status[prompt_id]:
        break
        
    time.sleep(10)    # Avoid hammering the ComfyUI API with continuous polling and exhausting local sockets.

print('Finished')
