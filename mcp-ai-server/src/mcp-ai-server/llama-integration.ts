import { spawn } from 'child_process';
import path from 'path';

export class LlamaIntegration {
  private llamaCppPath: string;
  private modelPath: string;

  constructor(llamaCppPath: string, modelPath: string) {
    this.llamaCppPath = llamaCppPath;
    this.modelPath = modelPath;
  }

  generate(prompt: string, maxTokens: number = 128): Promise<string> {
    return new Promise((resolve, reject) => {
      const args = [
        '-m',
        this.modelPath,
        '-p',
        prompt,
        '-n',
        maxTokens.toString(),
        '--temp',
        '0.7',
        '--repeat_penalty',
        '1.1',
      ];

      const llamaProcess = spawn(this.llamaCppPath, args);

      let output = '';
      let errorOutput = '';

      llamaProcess.stdout.on('data', (data) => {
        output += data.toString();
      });

      llamaProcess.stderr.on('data', (data) => {
        errorOutput += data.toString();
      });

      llamaProcess.on('close', (code) => {
        if (code === 0) {
          resolve(output.trim());
        } else {
          reject(new Error(`llama.cpp process exited with code ${code}: ${errorOutput}`));
        }
      });
    });
  }
}
