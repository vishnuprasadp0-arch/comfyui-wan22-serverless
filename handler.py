"""
RunPod Serverless Handler for Wan 2.2 ComfyUI Worker
"""

import runpod
import json
import urllib.request
import urllib.parse
import time
import os
import base64
from pathlib import Path

# ComfyUI API endpoint
COMFY_HOST = "127.0.0.1:8188"
COMFY_URL = f"http://{COMFY_HOST}"

def queue_prompt(prompt):
    """Queue a prompt to ComfyUI"""
    p = {"prompt": prompt}
    data = json.dumps(p).encode('utf-8')
    req = urllib.request.Request(f"{COMFY_URL}/prompt", data=data)
    response = urllib.request.urlopen(req)
    return json.loads(response.read())

def get_history(prompt_id):
    """Get the history/result of a prompt"""
    with urllib.request.urlopen(f"{COMFY_URL}/history/{prompt_id}") as response:
        return json.loads(response.read())

def get_output_files(prompt_id, output_dir="/comfyui/output"):
    """Wait for and collect output files from ComfyUI"""
    max_retries = 60
    retry_delay = 5
    
    for i in range(max_retries):
        history = get_history(prompt_id)
        
        if prompt_id in history:
            outputs = history[prompt_id].get('outputs', {})
            output_files = []
            
            for node_id, node_output in outputs.items():
                if 'images' in node_output:
                    for img in node_output['images']:
                        filename = img['filename']
                        subfolder = img.get('subfolder', '')
                        file_path = os.path.join(output_dir, subfolder, filename) if subfolder else os.path.join(output_dir, filename)
                        
                        if os.path.exists(file_path):
                            output_files.append(file_path)
                
                if 'gifs' in node_output:
                    for gif in node_output['gifs']:
                        filename = gif['filename']
                        subfolder = gif.get('subfolder', '')
                        file_path = os.path.join(output_dir, subfolder, filename) if subfolder else os.path.join(output_dir, filename)
                        
                        if os.path.exists(file_path):
                            output_files.append(file_path)
                
                if 'videos' in node_output:
                    for video in node_output['videos']:
                        filename = video['filename']
                        subfolder = video.get('subfolder', '')
                        file_path = os.path.join(output_dir, subfolder, filename) if subfolder else os.path.join(output_dir, filename)
                        
                        if os.path.exists(file_path):
                            output_files.append(file_path)
            
            if output_files:
                return output_files
        
        time.sleep(retry_delay)
    
    raise TimeoutError(f"Timeout waiting for outputs for prompt {prompt_id}")

def encode_file_to_base64(file_path):
    """Encode a file to base64 string"""
    with open(file_path, 'rb') as f:
        return base64.b64encode(f.read()).decode('utf-8')

def download_input_file(url, dest_path):
    """Download an input file from URL"""
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    urllib.request.urlretrieve(url, dest_path)
    return dest_path

def handler(job):
    """
    RunPod serverless handler function
    
    Expected input format:
    {
        "input": {
            "workflow": {...},  # ComfyUI workflow JSON (required)
            "input_image_url": "https://...",  # Optional: URL to input image
            "return_base64": true  # Optional: return files as base64 (default: false)
        }
    }
    """
    job_input = job['input']
    
    # Validate required inputs
    if 'workflow' not in job_input:
        return {
            "error": "Missing required 'workflow' in input"
        }
    
    workflow = job_input['workflow']
    
    try:
        # Download input image if provided
        if 'input_image_url' in job_input:
            input_url = job_input['input_image_url']
            filename = os.path.basename(urllib.parse.urlparse(input_url).path)
            input_path = f"/comfyui/input/{filename}"
            download_input_file(input_url, input_path)
            
            # Update workflow with the downloaded filename if needed
            # This is a simple approach - you may need to adjust based on your workflow structure
            for node_id, node in workflow.items():
                if node.get("class_type") == "LoadImage":
                    if "inputs" in node:
                        node["inputs"]["image"] = filename
        
        # Queue the workflow
        response = queue_prompt(workflow)
        prompt_id = response['prompt_id']
        
        # Wait for and collect outputs
        output_files = get_output_files(prompt_id)
        
        # Prepare response
        result = {
            "prompt_id": prompt_id,
            "output_files": []
        }
        
        # Return base64 encoded files if requested
        if job_input.get('return_base64', False):
            for file_path in output_files:
                result["output_files"].append({
                    "filename": os.path.basename(file_path),
                    "data": encode_file_to_base64(file_path),
                    "type": "base64"
                })
        else:
            # Just return file paths
            result["output_files"] = [
                {
                    "filename": os.path.basename(f),
                    "path": f
                } for f in output_files
            ]
        
        return result
        
    except Exception as e:
        return {
            "error": str(e),
            "error_type": type(e).__name__
        }

# Start the RunPod serverless worker
if __name__ == "__main__":
    runpod.serverless.start({"handler": handler})
