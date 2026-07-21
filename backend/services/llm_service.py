import os
import json

from dotenv import load_dotenv
from google import genai
from streamlit import form
from rules.rule_service import load_custom_rules
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
"""

    # After collecting code context, load any custom rules and append them
    custom_rules = load_custom_rules()

    rule_text = ""

    if custom_rules:
        rule_text = "\n\nCustom Organization Rules:\n"
        for rule in custom_rules:
            rule_text += (
                f"- [{rule['id']}] "
                f"{rule['title']} : "
                f"{rule['description']} "
                f"(Severity: {rule['severity']})\n"
            )

    context += rule_text

    prompt = f"""
You are an expert software security reviewer.

Analyze the following source code.

User Request:
{query}

Source Code:
{context}
{rule_text}
Your task:

1. Identify security vulnerabilities using the OWASP Top 10 (2021) as the primary security standard.
2. Identify bugs.
3. Identify performance issues.
4. Identify code smells.
5. Recommend fixes.
6. If a security issue matches an OWASP category, mention the corresponding OWASP ID (e.g., A01: Broken Access Control, A03: Injection).
7. Follow ALL custom organization rules provided in the context.
OWASP Top 10 (2021):
- A01: Broken Access Control
- A02: Cryptographic Failures
- A03: Injection
- A04: Insecure Design
- A05: Security Misconfiguration
- A06: Vulnerable and Outdated Components
- A07: Identification and Authentication Failures
- A08: Software and Data Integrity Failures
- A09: Security Logging and Monitoring Failures
- A10: Server-Side Request Forgery (SSRF)

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
      "owasp_category": "",
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
- Leave "owasp_category" empty if the issue is not related to an OWASP Top 10 category.
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