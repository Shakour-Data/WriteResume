# MCP AI Server with LLaMA Integration

This project provides an MCP AI server integrated with a lightweight LLaMA-based AI model optimized for CPU inference. It includes:

- MCP AI server implemented in TypeScript
- LLaMA model integration using llama.cpp subprocess
- Test suites for integration and functionality
- Setup instructions for llama.cpp and model files
- Documentation and usage guides

## Getting Started

1. Clone the repository.

2. Follow the setup instructions in `docs/llama_setup_instructions.md` to install llama.cpp and download the LLaMA model files.

3. Build the MCP AI server:

```bash
cd mcp-ai-server
npm install
npm run build
```

4. Run the MCP AI server:

```bash
npm start
```

5. Run tests to verify integration:

```bash
node tests/test_llama_integration.js
```

## Project Structure

See `project_structure.md` for detailed directory and file layout.

## Contributing

Contributions and improvements are welcome. Please follow the coding standards and add tests for new features.

## License

Specify your project license here.
