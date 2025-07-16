import { LlamaModel } from '../mcp-ai-server/src/mcp-ai-server/llama-integration.js';

async function testLlamaGenerate() {
  const modelPath = 'models/llama-7b/ggml-model.bin';
  const llama = new LlamaModel(modelPath);

  llama.start();

  const prompt = 'Hello, how are you?';
  const response = await llama.generate(prompt);

  console.log('LLaMA generate response:', response);

  llama.stop();

  if (!response || typeof response !== 'string') {
    throw new Error('LLaMA generate did not return a valid string');
  }

  if (!response.includes(prompt.substring(0, 5))) {
    throw new Error('LLaMA generate response does not contain prompt snippet');
  }

  console.log('LLaMA integration test passed');
}

testLlamaGenerate().catch((err) => {
  console.error('LLaMA integration test failed:', err);
  process.exit(1);
});
