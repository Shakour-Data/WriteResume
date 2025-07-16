# LLaMA Model and llama.cpp Setup Instructions

This document provides step-by-step instructions to set up the LLaMA model files and the llama.cpp executable required for the MCP AI server integration.

## Prerequisites

- Git
- CMake and a C++ compiler (e.g., gcc, clang)
- curl or wget for downloading files

## Step 1: Clone and Build llama.cpp

```bash
git clone https://github.com/ggerganov/llama.cpp.git
cd llama.cpp
make
```

This will build the `llama` executable in the `llama.cpp` directory.

## Step 2: Obtain LLaMA Model Files

The LLaMA model files are not publicly available and require permission from Meta. Follow these steps:

1. Request access to the LLaMA models from Meta's official channels.
2. Once approved, download the model files (e.g., `ggml-model.bin` for 7B model).
3. Place the downloaded model files in the `models/llama-7b/` directory in the project root.

## Step 3: Run Setup Script (Optional)

You can use the provided setup script to automate cloning and building llama.cpp and downloading model files (if URLs are available).

```bash
bash scripts/setup_llama.sh
```

**Note:** Update the `MODEL_URL` in the script with your actual model file download link.

## Step 4: Verify Setup

Ensure the following:

- The `llama.cpp/llama` executable exists and is executable.
- The model file `models/llama-7b/ggml-model.bin` exists.

## Step 5: Configure MCP AI Server

Update the MCP AI server configuration to point to the correct paths for the `llama` executable and model files.

Example in `mcp-ai-server/src/mcp-ai-server/index.ts`:

```typescript
this.llamaModel = new LlamaIntegration(
  'llama.cpp/llama',
  'models/llama-7b/ggml-model.bin'
);
```

## Additional Resources

- [llama.cpp GitHub Repository](https://github.com/ggerganov/llama.cpp)
- Meta LLaMA Model Access Information (official Meta channels)
