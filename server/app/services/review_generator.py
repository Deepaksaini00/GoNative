import json

from .client import gemini_request
from .prompts import REVIEW_GENERATOR_SYSTEM

REVIEW_SCHEMA = """
Return JSON with this exact shape:
{
  "session_rationale_hi": "string",
  "review_questions": [
    {
      "concept_slug": "string",
      "concept_title_hi": "string",
      "type": "translate_to_en|fill_blank|fix_error|multiple_choice",
      "prompt_hi": "string",
      "prompt_en": "string",
      "options": ["string"] or null,
      "correct_answer": "string",
      "why_reviewing_hi": "string"
    }
  ],
  "concepts_reviewed": ["string"]
}
Provide exactly 5 review_questions.
"""


async def generate_daily_review(progress_history: list[dict]) -> dict:
    user_prompt = (
        f"User learning history:\n{json.dumps(progress_history, ensure_ascii=False, indent=2)}\n"
        f"{REVIEW_SCHEMA}"
    )
    return await gemini_request(REVIEW_GENERATOR_SYSTEM, user_prompt)
