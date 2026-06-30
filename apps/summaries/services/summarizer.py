import os
import json
from google import genai
import os
import json
import os

def mock_summary(emails):
    """
    Generate a basic summary from email data without using an AI model.

    This function extracts:
    - Unique actors (accountant email addresses)
    - Concluded discussions based on simple keyword matching
    - Open action items for remaining emails

    Args:
        emails (QuerySet): Collection of Email model instances.

    Returns:
        dict: Summary containing actors, concluded discussions,
        and open action items.
    """
    actors = set()
    open_items = []
    concluded = []

    for email in emails:
        actors.add(email.accountant.email)

        body = email.body.lower()

        if "received" in body or "thank you" in body:
            concluded.append(email.subject)
        else:
            open_items.append(email.subject)

    return {
        "actors": list(actors),
        "concluded_discussions": concluded,
        "open_action_items": open_items,
    }



def gemini_summary(emails_text):
    """
    Generate an email summary using Gemini 2.5 Flash.
    """

    client = genai.Client(
        api_key=os.getenv("GEMINI_API_KEY")
    )

    prompt = f"""
You are an AI system that extracts structured JSON from email threads.

STRICT RULES:
- Return ONLY valid JSON
- Do NOT include markdown, explanations, or text
- Always include ALL keys even if empty
- Never omit any field

OUTPUT FORMAT:
{{
    "actors": ["email1", "email2"],
    "concluded_discussions": ["..."],
    "open_action_items": ["..."]
}}

RULES FOR ACTORS:
- Extract ALL unique email addresses found in emails
- Include both sender and recipient if available

Emails:
{emails_text}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )

    text = response.text.strip()

    if text.startswith("```"):
        text = (
            text.replace("```json", "")
            .replace("```", "")
            .strip()
        )

    try:
        return json.loads(text)
    except Exception:
        import re
        json_text = re.search(r"\{.*\}", text, re.S)
        if json_text:
            return json.loads(json_text.group())
        raise


import os
import json

def generate_summary(emails):
    """
    Generate email summary using Gemini (preferred) with safe fallback.

    Flow:
    1. Convert emails → text
    2. Try Gemini summary
    3. If fails → use mock summary
    4. Ensure actors are always correct (Python fallback)
    """

    # -----------------------------
    # STEP 1: Build email text
    # -----------------------------
    emails_text = "\n\n".join(
        f"Subject: {email.subject}\nBody: {email.body}"
        for email in emails
    )

    # -----------------------------
    # STEP 2: Always compute actors safely (Python fallback)
    # -----------------------------
    fallback_actors = list(
        set(email.accountant.email for email in emails)
    )

    # -----------------------------
    # STEP 3: Check API key
    # -----------------------------
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key or not api_key.strip():
        result = mock_summary(emails)
        result["actors"] = fallback_actors
        return result

    # -----------------------------
    # STEP 4: Try Gemini
    # -----------------------------
    try:
        result = gemini_summary(emails_text)

        # -----------------------------
        # STEP 5: Safety fixes
        # -----------------------------
        if not isinstance(result, dict):
            result = mock_summary(emails)

        # Ensure keys exist
        result.setdefault("actors", [])
        result.setdefault("concluded_discussions", [])
        result.setdefault("open_action_items", [])

        # IMPORTANT: enforce correct actors
        if not result["actors"]:
            result["actors"] = fallback_actors

        return result

    except Exception as e:
        print("Gemini Error:", e)

        result = mock_summary(emails)
        result["actors"] = fallback_actors
        return result