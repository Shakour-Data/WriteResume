#!/bin/bash
# Script to download and setup llama.cpp and LLaMA model files

set -e

# Directory for llama.cpp
LLAMA_CPP_DIR="llama.cpp"
# Directory for models
MODELS_DIR="models/llama-7b"

echo "Cloning llama.cpp repository..."
if [ ! -d "$LLAMA_CPP_DIR" ]; then
  git clone https://github.com/ggerganov/llama.cpp.git "$LLAMA_CPP_DIR"
else
  echo "llama.cpp directory already exists, skipping clone."
fi

echo "Building llama.cpp with CMake..."
cd "$LLAMA_CPP_DIR"
mkdir -p build
cd build
cmake ..
make
cd ../..

echo "Creating models directory..."
mkdir -p "$MODELS_DIR"

echo "Downloading LLaMA 7B model files..."
# Note: The actual LLaMA model files require access permissions from Meta.
# This script assumes you have the download links or have placed the files manually.
# Replace the following URLs with your actual model file URLs or instructions.

MODEL_URL="https://example.com/path/to/ggml-model.bin"

if [ ! -f "$MODELS_DIR/ggml-model.bin" ]; then
  echo "Downloading model file..."
  curl -L -o "$MODELS_DIR/ggml-model.bin" "$MODEL_URL"
else
  echo "Model file already exists, skipping download."
fi

echo "Setup complete. Please verify the model files and llama.cpp executable."
