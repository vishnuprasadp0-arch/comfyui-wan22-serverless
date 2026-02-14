# clean base image containing only comfyui, comfy-cli and comfyui-manager
FROM runpod/worker-comfyui:5.5.1-base

# install custom nodes into comfyui (first node with --mode remote to fetch updated cache)
RUN comfy node install --exit-on-fail comfyui_essentials --mode remote

# The following unknown_registry custom nodes could not be automatically resolved because no aux_id (GitHub repo) was provided:
# Could not resolve unknown_registry node: ModelSamplingSD3 - no aux_id provided, skipping installation
# Could not resolve unknown_registry node: ModelSamplingSD3 - no aux_id provided, skipping installation
# Could not resolve unknown_registry node: INTConstant - no aux_id provided, skipping installation
# Could not resolve unknown_registry node: INTConstant - no aux_id provided, skipping installation
# Could not resolve unknown_registry node: Seed (rgthree) - no aux_id provided, skipping installation
# Could not resolve unknown_registry node: WanImageToVideo - no aux_id provided, skipping installation
# Could not resolve unknown_registry node: INTConstant - no aux_id provided, skipping installation
# Could not resolve unknown_registry node: wanBlockSwap - no aux_id provided, skipping installation
# Could not resolve unknown_registry node: wanBlockSwap - no aux_id provided, skipping installation
# Could not resolve unknown_registry node: VHS_VideoCombine - no aux_id provided, skipping installation
# Could not resolve unknown_registry node: INTConstant - no aux_id provided, skipping installation
# Could not resolve unknown_registry node: VAEDecodeTiled - no aux_id provided, skipping installation

# download models into comfyui
RUN comfy model download --url https://huggingface.co/Comfy-Org/Wan_2.2_ComfyUI_Repackaged/resolve/main/split_files/vae/wan2.2_vae.safetensors --relative-path models/vae --filename wan2.2_vae.safetensors
# RUN # Could not find URL for Wan2.2_Remix_NSFW_i2v_14b_high_lighting_v2.0.safetensors
# RUN # Could not find URL for Wan2.2_Remix_NSFW_i2v_14b_low_lighting_v2.0.safetensors
# RUN # Could not find URL for nsfw_wan_umt5-xxl_fp8_scaled.safetensors

# copy all input data (like images or videos) into comfyui (uncomment and adjust if needed)
# COPY input/ /comfyui/input/
