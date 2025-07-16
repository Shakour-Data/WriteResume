#!/usr/bin/env node
import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import {
  CallToolRequestSchema,
  ErrorCode,
  ListToolsRequestSchema,
  McpError,
} from '@modelcontextprotocol/sdk/types.js';
import { LlamaIntegration } from './llama-integration.js';

class McpAiServer {
  server;
  llamaModel;

  constructor() {
    this.server = new Server(
      {
        name: 'mcp-ai-server',
        version: '0.2.0',
      },
      {
        capabilities: {
          resources: {},
          tools: {},
        },
      }
    );

    // Initialize LLaMA model with path to model file
    this.llamaModel = new LlamaIntegration('path/to/llama.cpp', 'models/llama-7b/ggml-model.bin');

    this.server.setRequestHandler(ListToolsRequestSchema, async () => ({
      tools: [
        {
          name: 'llama_ai_completion',
          description: 'AI completion tool using LLaMA model optimized for CPU inference',
          inputSchema: {
            type: 'object',
            properties: {
              prompt: {
                type: 'string',
                description: 'Prompt text for AI completion',
              },
            },
            required: ['prompt'],
          },
        },
      ],
    }));

    this.server.setRequestHandler(CallToolRequestSchema, async (request) => {
      if (request.params.name !== 'llama_ai_completion') {
        throw new McpError(
          ErrorCode.MethodNotFound,
          `Unknown tool: ${request.params.name}`
        );
      }
      if (!request.params.arguments || typeof request.params.arguments.prompt !== 'string') {
        throw new McpError(
          ErrorCode.InvalidParams,
          'Invalid or missing prompt argument'
        );
      }
      const prompt = request.params.arguments.prompt;
      // Use LLaMA model to generate response
      const responseText = await this.llamaModel.generate(prompt);
      return {
        content: [
          {
            type: 'text',
            text: responseText,
          },
        ],
      };
    });

    this.server.onerror = (error) => console.error('[MCP Error]', error);
    process.on('SIGINT', async () => {
      await this.server.close();
      process.exit(0);
    });
  }

  async run() {
    const transport = new StdioServerTransport();
    await this.server.connect(transport);

    console.error('MCP AI server with LLaMA model running on stdio');
  }
}

const server = new McpAiServer();
server.run().catch(console.error);
