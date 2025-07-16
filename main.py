import os
import re
import json
import time
import sys
import asyncio
import subprocess
from datetime import datetime
from mcp import ClientSession as McpClient  # Assuming MCP Python client library is installed
import anyio
from anyio.streams.memory import MemoryObjectReceiveStream, MemoryObjectSendStream

class AsyncStreamWrapper:
    def __init__(self, stream):
        self._stream = stream
        self._loop = asyncio.get_event_loop()

    async def send(self, data):
        def write():
            # Serialize data to string if needed
            if not isinstance(data, str):
                try:
                    data_str = data.json()
                except Exception:
                    data_str = str(data)
            else:
                data_str = data
            self._stream.write(data_str)
            self._stream.flush()
        await self._loop.run_in_executor(None, write)

    async def receive(self):
        def read():
            return self._stream.read(1)
        return await self._loop.run_in_executor(None, read)

# MCP AI Configuration
MCP_SERVER_NAME = "mcp-ai-server"
MCP_TOOL_NAME = "simple_ai_completion"

# Fixed Paths Configuration
RESUME_PATH = "Information/resume_en.md"
JOB_DESCRIPTION_PATH = "Information/About_job.md"
OUTPUT_DIR = "Output"
OPTIMIZED_RESUME_PATH = os.path.join(OUTPUT_DIR, "Optimized_Resume.md")
COVER_LETTER_PATH = os.path.join(OUTPUT_DIR, "Cover_Letter.md")
ANALYSIS_REPORT_PATH = os.path.join(OUTPUT_DIR, "Optimization_Report.md")

def create_output_dir():
    """Create output directory if not exists"""
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

def read_md_file(file_path):
    """Read content from Markdown file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        print(f"Error reading file: {str(e)}")
        return None

def save_to_file(content, file_path):
    """Save content to file"""
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)
        return True
    except Exception as e:
        print(f"Error saving file: {str(e)}")
        return False

async def get_mcp_ai_response(prompt, max_retries=1):
    """Call MCP AI tool for completion with retry logic"""
    # Launch MCP server subprocess
    mcp_server_process = subprocess.Popen(
        ["node", "mcp-ai-server/build/mcp-ai-server/index.js"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=0,
    )

    # Connect MCP client streams to subprocess pipes with async wrappers
    read_stream = AsyncStreamWrapper(mcp_server_process.stdout)
    write_stream = AsyncStreamWrapper(mcp_server_process.stdin)

    client = McpClient(read_stream, write_stream)
    for attempt in range(max_retries):
        try:
            response = await client.call_tool(
                name=MCP_TOOL_NAME,
                arguments={"prompt": prompt}
            )
            # Assuming response content is a list with text type content
            for content in response.get("content", []):
                if content.get("type") == "text":
                    # Terminate MCP server process after use
                    mcp_server_process.terminate()
                    return content.get("text", "")
            mcp_server_process.terminate()
            return ""
        except Exception as e:
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt
                print(f"Retry {attempt+1}/{max_retries} in {wait_time} seconds...")
                time.sleep(wait_time)
                continue
            print(f"API Error: {str(e)}")
            mcp_server_process.terminate()
            return ""

def calculate_acceptance_probability(resume_text, cover_letter, job_description):
    """Calculate job acceptance probability"""
    prompt = f"""
    Estimate job acceptance probability (0-100%) based on:
    - Resume relevance to job requirements
    - Cover letter effectiveness
    - Overall qualifications match
    
    Consider:
    1. Skill alignment
    2. Experience relevance
    3. Quantifiable achievements
    4. Cultural fit indicators
    5. Problem-solving approach
    
    Return ONLY the number. Example: "75"
    
    [JOB DESCRIPTION]
    {job_description[:3000]}
    
    [RESUME]
    {resume_text[:2000]}
    
    [COVER LETTER]
    {cover_letter[:2000]}
    """
    
    response = asyncio.run(get_mcp_ai_response(prompt)).strip()
    match = re.search(r'\d+', response)
    if match:
        return min(100, max(0, int(match.group())))
    return 0

def optimize_resume(original_resume, job_description):
    """Ethically optimize resume for target job"""
    prompt = f"""
    Optimize this resume for the target job WITHOUT adding false information.
    Use only the original content and restructure ethically:
    
    1. KEYWORD OPTIMIZATION: Mirror 5-7 key terms from job description
    2. PRIORITIZATION: Reorder sections by job relevance
    3. ACHIEVEMENT FORMULA: Use "Action Verb + Metric + Skill"
    4. INDUSTRY LANGUAGE: Adopt terminology from job description
    5. TARGETED SUMMARY: Create professional summary focused on job needs
    
    Return optimized resume in Markdown format ONLY.
    
    [JOB DESCRIPTION]
    {job_description[:3000]}
    
    [ORIGINAL RESUME]
    {original_resume}
    """
    
    return asyncio.run(get_mcp_ai_response(prompt))

def generate_cover_letter(resume_text, job_description):
    """Generate professional cover letter"""
    prompt = f"""
    Create a cover letter using this structure:
    
    1. Why I'm a strong fit for this position
    2. SWOT Analysis (markdown table):
        | Strengths          | Weaknesses        |
        |--------------------|-------------------|
        | [Content]          | [Content]         |
        | Opportunities      | Threats           |
        |--------------------|-------------------|
        | [Content]          | [Content]         |
    3. Converting weaknesses into strengths
    4. Transforming threats into opportunities
    5. Collaboration Concepts
    
    Use natural business English. Focus on measurable achievements.
    
    [JOB DESCRIPTION]
    {job_description[:4000]}
    
    [RESUME CONTENT]
    {resume_text[:4000]}
    """
    
    return asyncio.run(get_mcp_ai_response(prompt))

def generate_analysis_report(original_prob, resume_opt_prob, final_prob, optimization_changes, cover_letter_strategies):
    """Generate detailed optimization report"""
    date_str = datetime.now().strftime("%Y-%m-%d %H:%M")
    resume_improvement = resume_opt_prob - original_prob
    cover_improvement = final_prob - resume_opt_prob
    total_improvement = final_prob - original_prob
    
    report = f"""
# JOB APPLICATION OPTIMIZATION REPORT
**Generated on**: {date_str}

## Probability Evolution
| Stage | Probability | Improvement |
|-------|-------------|-------------|
| Original Application | {original_prob}% | Baseline |
| After Resume Optimization | {resume_opt_prob}% | +{resume_improvement}% |
| After Cover Letter | {final_prob}% | +{cover_improvement}% |
| **Total Improvement** | | **+{total_improvement}%** |

## Resume Optimization Strategies
{optimization_changes}

## Cover Letter Key Strategies
{cover_letter_strategies}

## Probability Enhancement Analysis
- **Resume Optimization Impact**: {resume_improvement}% increase
- **Cover Letter Impact**: {cover_improvement}% increase
- **Combined Effectiveness**: {total_improvement}% total improvement

## Next Steps
{"✅ Strong candidate - proceed with application" if final_prob >= 70 else 
"📝 Good potential - consider minor refinements" if final_prob >= 50 else 
"⚠️ Needs improvement - review strategy for similar roles"}
"""
    return report

def extract_key_strategies(cover_letter):
    """Extract key strategies from cover letter"""
    prompt = f"""
    Extract key enhancement strategies from this cover letter:
    
    1. Impact opening statement
    2. Top 3 quantified achievements
    3. Main solution-focused approach
    4. Primary cultural alignment point
    5. Key collaboration concept
    
    Return as bullet points. Do not add explanations.
    
    [COVER LETTER]
    {cover_letter[:3000]}
    """
    
    try:
        return asyncio.run(get_mcp_ai_response(prompt))
    except:
        return "Strategies extraction failed"

def extract_resume_changes(original, optimized):
    """Extract key changes between resumes"""
    prompt = f"""
    Identify and list the main optimization changes between these resumes:
    
    1. Keyword additions
    2. Section reordering
    3. Achievement reformulations
    4. Terminology changes
    5. Summary refocusing
    
    Return as bullet points. Be specific.
    
    [ORIGINAL RESUME]
    {original[:2000]}
    
    [OPTIMIZED RESUME]
    {optimized[:2000]}
    """
    
    try:
        return asyncio.run(get_mcp_ai_response(prompt))
    except:
        return "Change extraction failed"

def main():
    print("=" * 60)
    print("JOB APPLICATION ENHANCEMENT SYSTEM")
    print("=" * 60)
    print("Ethically boosting acceptance probability by 10-20%\n")
    
    # Create output directory
    create_output_dir()
    
    # Read files from fixed paths
    print("📂 Reading input files...")
    original_resume = read_md_file(RESUME_PATH)
    job_desc = read_md_file(JOB_DESCRIPTION_PATH)
    
    if not original_resume or not job_desc:
        print("❌ Error reading files. Please check paths.")
        return
    
    # Calculate initial probability
    print("\n📈 Calculating initial acceptance probability...")
    original_prob = asyncio.run(calculate_acceptance_probability(original_resume, "", job_desc))
    print(f"🎯 Initial Probability: {original_prob}%")
    
    # Optimize resume
    print("\n🔄 Optimizing resume for target position...")
    optimized_resume = asyncio.run(optimize_resume(original_resume, job_desc))
    save_to_file(optimized_resume, OPTIMIZED_RESUME_PATH)
    print(f"✅ Optimized resume saved to: {OPTIMIZED_RESUME_PATH}")
    
    # Calculate probability after resume optimization
    print("📈 Calculating probability after resume optimization...")
    resume_opt_prob = asyncio.run(calculate_acceptance_probability(optimized_resume, "", job_desc))
    print(f"🎯 Post-Resume Probability: {resume_opt_prob}%")
    
    # Generate cover letter
    print("\n✍️ Generating cover letter...")
    cover_letter = asyncio.run(generate_cover_letter(optimized_resume, job_desc))
    save_to_file(cover_letter, COVER_LETTER_PATH)
    print(f"✅ Cover letter saved to: {COVER_LETTER_PATH}")
    
    # Calculate final probability
    print("\n📈 Calculating final acceptance probability...")
    final_prob = asyncio.run(calculate_acceptance_probability(optimized_resume, cover_letter, job_desc))
    print(f"🎯 Final Probability: {final_prob}%")
    
    # Extract changes and strategies
    print("\n🔍 Analyzing optimization changes...")
    resume_changes = asyncio.run(extract_resume_changes(original_resume, optimized_resume))
    cover_strategies = asyncio.run(extract_key_strategies(cover_letter))
    
    # Generate and save report
    report = generate_analysis_report(
        original_prob,
        resume_opt_prob,
        final_prob,
        resume_changes,
        cover_strategies
    )
    save_to_file(report, ANALYSIS_REPORT_PATH)
    print(f"📊 Full report saved to: {ANALYSIS_REPORT_PATH}")
    
    # Display summary
    improvement = final_prob - original_prob
    print("\n" + "=" * 60)
    print("OPTIMIZATION SUMMARY")
    print("=" * 60)
    print(f"Initial Probability: {original_prob}%")
    print(f"Final Probability: {final_prob}%")
    print(f"Total Improvement: {improvement}%")
    print("=" * 60)
    print("\n✅ Process completed successfully!")

if __name__ == "__main__":
    main()
