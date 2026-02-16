# ComfyUI Wan 2.2 I2V RunPod Serverless

[![Runpod](https://api.runpod.io/badge/vishnuprasadp0-arch/comfyui-wan22-serverless)](https://console.runpod.io/hub/vishnuprasadp0-arch/comfyui-wan22-serverless)

Dockerized ComfyUI workflow for Wan 2.2 image-to-video generation on RunPod Serverless.

## Contents

* `Dockerfile` - Docker container configuration with Wan 2.2 models
* `handler.py` - RunPod serverless handler implementation
* `comfyui-wan-22-i2v-final-runpod-serverless.json` - ComfyUI workflow
* `example-request.json` - Example API request payload for testing

## Features

- Standard RunPod handler implementation
- Support for ComfyUI workflows
- Input image download from URL
- Optional base64 output encoding
- Handles videos, GIFs, and images

## Input Format

```json
{
  "input": {
    "workflow": { ... },           // ComfyUI workflow JSON (required)
    "input_image_url": "https://...", // Optional: URL to input image
    "return_base64": true          // Optional: return files as base64 (default: false)
  }
}
```

## Example Request

### Basic Request with Workflow

```json
{
  "input": {
    "workflow": {
      "1": {
        "class_type": "LoadImage",
        "inputs": {
          "image": "example.png"
        }
      },
      "2": {
        "class_type": "WanImageToVideo",
        "inputs": {
          "image": ["1", 0],
          "prompt": "A woman smiling and waving",
          "unet_name": "Wan2.2_Remix_NSFW_i2v_14b_high_lighting_v2.0.safetensors",
          "vae_name": "wan_2.1_vae.safetensors",
          "clip_name": "nsfw_wan_umt5-xxl_fp8_scaled.safetensors"
        }
      }
    },
    "input_image_url": "https://example.com/image.png",
    "return_base64": false
  }
}
```

## Response Format

### Success Response (return_base64: false)

```json
{
  "prompt_id": "12345-67890",
  "output_files": [
    {
      "filename": "output_video.mp4",
      "path": "/comfyui/output/output_video.mp4"
    }
  ]
}
```

### Success Response (return_base64: true)

```json
{
  "prompt_id": "12345-67890",
  "output_files": [
    {
      "filename": "output_video.mp4",
      "data": "base64_encoded_data...",
      "type": "base64"
    }
  ]
}
```

### Error Response

```json
{
  "error": "Error message here",
  "error_type": "ValueError"
}
```

## Building and Deploying

### Local Docker Build

```bash
# Build the Docker image
docker build -t comfyui-wan22-serverless .

# Run the container locally
docker run -p 8188:8188 comfyui-wan22-serverless
```

### Deploy to RunPod

1. Build and push the Docker image:
```bash
docker build -t your-registry/wan22-serverless:latest .
docker push your-registry/wan22-serverless:latest
```

2. Deploy on RunPod:
   - Go to RunPod Serverless
   - Create new template with your image
   - Set container disk to at least 20GB
   - Deploy endpoint

## Getting Your Workflow JSON

1. Use ComfyUI locally or on RunPod
2. Load the Wan 2.2 nodes and create your workflow
3. Enable "Dev mode" in ComfyUI settings
4. Click "Save (API Format)" to get the workflow JSON
5. Use this JSON as the `workflow` parameter

## Environment Variables

The handler uses these default values:
- `COMFY_HOST`: `127.0.0.1:8188` (ComfyUI endpoint)
- Output directory: `/comfyui/output`
- Input directory: `/comfyui/input`

## Timeout Settings

- Maximum wait time for outputs: 300 seconds (5 minutes)
- Retry interval: 5 seconds
- Adjust these in the `get_output_files()` function if needed

## Notes

- The handler automatically updates LoadImage nodes with downloaded input images
- Supports multiple output formats: images, GIFs, videos
- Base64 encoding is useful for immediate returns but increases payload size
- File paths are useful when using RunPod Network Volumes

---

Generated with **ComfyUI to Docker Wizard**
