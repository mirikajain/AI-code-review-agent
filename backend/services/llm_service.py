import os
import json

from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def generate_review(query, retrieved_chunks):
    """
    Generate a structured security report using Gemini.
    """
    print("Entered generate_review")

    context = ""

    for chunk in retrieved_chunks:
        context += f"""
File: {chunk['file']}
Lines: {chunk['start_line']} - {chunk['end_line']}

{chunk['content']}

---------------------------------------------------------
"""

    prompt = f"""
You are an expert software security reviewer.

Analyze the following source code.

User Request:
{query}

Source Code:
{context}

Your task:

1. Identify security vulnerabilities.
2. Identify bugs.
3. Identify performance issues.
4. Identify code smells.
5. Recommend fixes.

Return ONLY valid JSON.

Use exactly this format:

{{
  "summary": {{
    "critical": 0,
    "high": 0,
    "medium": 0,
    "low": 0
  }},
  "issues": [
    {{
      "file": "",
      "rule": "",
      "severity": "Critical",
      "description": "",
      "recommendation": ""
    }}
  ]
}}

Rules:
- Return ONLY JSON.
- Do not return Markdown.
- Do not use ```json.
- Every issue must belong to exactly one severity.
- Severity must be one of:
  Critical
  High
  Medium
  Low
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    response_text = response.text.strip()
    print("Response received")

    # Remove markdown if Gemini adds it
    if response_text.startswith("```json"):
        response_text = response_text.replace("```json", "")
        response_text = response_text.replace("```", "")
        response_text = response_text.strip()

    try:
        return json.loads(response_text)

    except Exception:

        return {
            "summary": {
                "critical": 0,
                "high": 0,
                "medium": 0,
                "low": 0
            },
            "issues": [],
            "raw_response": response_text
        }