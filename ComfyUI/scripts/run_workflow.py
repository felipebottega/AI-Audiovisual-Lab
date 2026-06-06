import os
import sys
import json
import time
import requests
from urllib import request

SERVER_URL = "http://127.0.0.1:8188"    # Local server address.

if len(sys.argv) < 2:
    sys.exit("Usage: python run_workflow.py <path_to_workflow.json>")

workflow_filepath = sys.argv[1]

# Loads the workflow directly from the JSON file.
with open(workflow_filepath, "r", encoding="utf-8") as f:
    workflow = json.load(f)
    
# Dynamically checks if the workflow contains an input node for logging purposes.
input_log = "Direct execution"
for x in workflow:
    if workflow[x].get('class_type') == 'LoadImage':
        input_log = workflow[x]['inputs'].get('image', 'Image Node')

p = {"prompt": workflow}
data = json.dumps(p).encode('utf-8')

# Send workflow directly to execution.
req = request.Request(f"{SERVER_URL}/prompt", data=data)
resp = request.urlopen(req)
prompt_id = json.load(resp)["prompt_id"]
print(f'Executing {prompt_id} - {input_log}')

# Wait to finish.
while True:
    status = requests.get(f"{SERVER_URL}/history/{prompt_id}").json()
    
    if prompt_id in status and "outputs" in status[prompt_id]:
        break
        
    time.sleep(10)    # Avoid hammering the ComfyUI API with continuous polling and exhausting local sockets.

print('Finished')