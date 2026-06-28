import os
import json


def mock_summary(emails):
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
    import google.generativeai as genai

    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    model = genai.GenerativeModel("gemini-1.5-flash")

    prompt = f"""
You are an AI assistant summarizing email threads.

Extract JSON with:
- actors
- concluded_discussions
- open_action_items

Emails:
{emails_text}

Return ONLY valid JSON. No markdown, no explanation.
"""

    response = model.generate_content(prompt)

    text = response.text.strip()

    # 🔥 Clean possible markdown formatting
    if "```" in text:
        text = text.replace("```json", "").replace("```", "").strip()

    return json.loads(text)


def generate_summary(emails):
    """
    Smart router:
    - If Gemini key exists → use Gemini
    - Else → fallback mock
    """

    emails_text = "\n".join(
        [f"{e.subject}: {e.body}" for e in emails]
    )

    if os.getenv("GEMINI_API_KEY") and os.getenv("GEMINI_API_KEY").strip():        
        try:
            return gemini_summary(emails_text)
        except:
            # fallback if API fails
            return mock_summary(emails)

    return mock_summary(emails)