#!/usr/bin/env bash
# CivitAI model downloader for GPU server ComfyUI
# Usage: civitai-download.sh <model_url_or_id> <type> [filename]
# Types: checkpoint, lora, vae, controlnet, embedding, upscale, textencoder, diffusion
#
# Examples:
#   civitai-download.sh 101055 checkpoint    # Download by model version ID
#   civitai-download.sh https://civitai.com/models/133005 lora
#
# Requires CIVITAI_API_KEY env var or ~/.civitai_key file

set -euo pipefail

COMFYUI_DIR="/mnt/storage-2tb/comfyui"

# Map type to ComfyUI model directory
declare -A TYPE_MAP=(
  [checkpoint]="checkpoints"
  [lora]="loras"
  [vae]="vae"
  [controlnet]="controlnet"
  [embedding]="embeddings"
  [upscale]="upscale_models"
  [textencoder]="text_encoders"
  [diffusion]="diffusion_models"
  [clip]="clip"
)

# Get API key
API_KEY="${CIVITAI_API_KEY:-}"
if [ -z "$API_KEY" ] && [ -f ~/.civitai_key ]; then
  API_KEY=$(cat ~/.civitai_key)
fi

if [ -z "$API_KEY" ]; then
  echo "Error: No CivitAI API key found. Set CIVITAI_API_KEY or create ~/.civitai_key"
  exit 1
fi

MODEL_INPUT="${1:?Usage: civitai-download.sh <model_url_or_id> <type> [filename]}"
MODEL_TYPE="${2:?Specify type: checkpoint, lora, vae, controlnet, embedding, upscale, textencoder, diffusion}"
CUSTOM_NAME="${3:-}"

# Resolve type to directory
DEST_DIR="${TYPE_MAP[$MODEL_TYPE]:-}"
if [ -z "$DEST_DIR" ]; then
  echo "Error: Unknown type '$MODEL_TYPE'. Use: ${!TYPE_MAP[*]}"
  exit 1
fi

FULL_DEST="$COMFYUI_DIR/models/$DEST_DIR"

# Extract version ID from URL if needed
if [[ "$MODEL_INPUT" =~ civitai.com ]]; then
  # Try to extract modelVersionId from URL
  VERSION_ID=$(echo "$MODEL_INPUT" | grep -oP 'modelVersionId=\K[0-9]+' || true)
  if [ -z "$VERSION_ID" ]; then
    # Get model ID and fetch latest version
    MODEL_ID=$(echo "$MODEL_INPUT" | grep -oP 'models/\K[0-9]+')
    echo "Fetching latest version for model $MODEL_ID..."
    VERSION_ID=$(curl -sH "Authorization: Bearer $API_KEY" \
      "https://civitai.com/api/v1/models/$MODEL_ID" | \
      python3 -c "import sys,json; d=json.load(sys.stdin); print(d['modelVersions'][0]['id'])")
  fi
else
  VERSION_ID="$MODEL_INPUT"
fi

echo "Downloading version $VERSION_ID to $FULL_DEST..."

# Get download URL and filename
META=$(curl -sH "Authorization: Bearer $API_KEY" \
  "https://civitai.com/api/v1/model-versions/$VERSION_ID")

DOWNLOAD_URL=$(echo "$META" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d['downloadUrl'])")
DEFAULT_NAME=$(echo "$META" | python3 -c "import sys,json; d=json.load(sys.stdin); f=d['files'][0]; print(f['name'])")
MODEL_NAME=$(echo "$META" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d['model']['name'])" 2>/dev/null || echo "unknown")

FILENAME="${CUSTOM_NAME:-$DEFAULT_NAME}"

echo "Model: $MODEL_NAME"
echo "File: $FILENAME"
echo "Destination: $FULL_DEST/$FILENAME"

curl -L -H "Authorization: Bearer $API_KEY" \
  "$DOWNLOAD_URL" \
  -o "$FULL_DEST/$FILENAME" \
  --progress-bar

echo "✅ Downloaded: $FULL_DEST/$FILENAME"
