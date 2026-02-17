# Start from RunPod worker-comfyui base image
# Replace <version> with the latest release from https://github.com/runpod-workers/worker-comfyui/releases
FROM runpod/worker-comfyui:5.5.1-base

# Install required custom nodes
RUN cd /comfyui/custom_nodes && \
    # ComfyUI Essentials (ImageResize+, GetImageSize+)
    git clone https://github.com/cubiq/ComfyUI_essentials.git && \
    cd ComfyUI_essentials && \
    pip install -r requirements.txt && \
    cd .. && \
    \
    # rgthree-comfy (Seed node)
    git clone https://github.com/rgthree/rgthree-comfy.git && \
    cd rgthree-comfy && \
    pip install -r requirements.txt && \
    cd .. && \
    \
    # wanBlockSwap
    git clone https://github.com/facok/ComfyUI-HunyuanVideoMultiLora.git && \
    cd ComfyUI-HunyuanVideoMultiLora && \
    pip install -r requirements.txt 2>/dev/null || true

# Download Wan 2.2 UNET models (high and low lighting)
RUN comfy model download \
    --url https://huggingface.co/FX-FeiHou/wan2.2-Remix/resolve/main/NSFW/Wan2.2_Remix_NSFW_i2v_14b_high_lighting_v2.0.safetensors \
    --relative-path models/unet \
    --filename Wan2.2_Remix_NSFW_i2v_14b_high_lighting_v2.0.safetensors

RUN comfy model download \
    --url https://huggingface.co/FX-FeiHou/wan2.2-Remix/resolve/main/NSFW/Wan2.2_Remix_NSFW_i2v_14b_low_lighting_v2.0.safetensors \
    --relative-path models/unet \
    --filename Wan2.2_Remix_NSFW_i2v_14b_low_lighting_v2.0.safetensors

# Download CLIP model
RUN comfy model download \
    --url https://huggingface.co/NSFW-API/NSFW-Wan-UMT5-XXL/resolve/main/nsfw_wan_umt5-xxl_fp8_scaled.safetensors \
    --relative-path models/clip \
    --filename nsfw_wan_umt5-xxl_fp8_scaled.safetensors

# Download VAE model
RUN comfy model download \
    --url https://huggingface.co/Comfy-Org/Wan_2.2_ComfyUI_Repackaged/resolve/main/split_files/vae/wan2.2_vae.safetensors \
    --relative-path models/vae \
    --filename wan_2.1_vae.safetensors

# Optional: Copy static input files if you have a default image
# Uncomment and place your example.png in an input/ folder next to the Dockerfile
# COPY input/ /comfyui/input/
