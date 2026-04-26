import json
import re
from groq import Groq
from backend.config import GROQ_API_KEY, MODEL_NAME, MAX_TOKENS, TEMPERATURE

client = Groq(api_key=GROQ_API_KEY)

def ask_question(context: str, question: str) -> str:
    prompt = f"""You are an expert research assistant. Use the following context from a research paper to answer the question accurately and concisely. Always cite specific parts of the context in your answer.

Context:
{context}

Question: {question}

Answer:"""

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=MAX_TOKENS,
        temperature=TEMPERATURE
    )
    return response.choices[0].message.content

def generate_summary(text: str) -> dict:
    prompt = f"""You are an expert research assistant. Analyze this research paper and provide a structured analysis.

Paper content:
{text[:12000]}

You MUST respond with ONLY a valid JSON object. No markdown, no backticks, no extra text before or after.

The JSON must have exactly these keys:
{{
  "title": "paper title if found, else Research Paper",
  "summary": "2-3 sentence overview of the paper",
  "problem": "what problem does this paper solve?",
  "methodology": "what methods or approaches were used?",
  "key_findings": ["finding 1", "finding 2", "finding 3"],
  "limitations": "main limitations of the study",
  "applications": "real-world applications of this research"
}}"""

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1500,
        temperature=0.1
    )

    raw = response.choices[0].message.content.strip()

    # Try to extract JSON if wrapped in backticks
    json_match = re.search(r'\{.*\}', raw, re.DOTALL)
    if json_match:
        raw = json_match.group()

    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        # Fallback
        return {
            "title": "Research Paper",
            "summary": raw,
            "problem": "Could not parse",
            "methodology": "Could not parse",
            "key_findings": ["Could not parse structured findings"],
            "limitations": "Could not parse",
            "applications": "Could not parse"
        }