from .client import gemini_request
from .prompts import EVALUATOR_SYSTEM

EVAL_SCHEMA = """
Return JSON with this exact shape:
{
  "is_correct": boolean,
  "confidence_score": float,
  "correct_answer": "string",
  "accepted_alternatives": ["string"],
  "feedback_hi": "string",
  "grammar_breakdown": {
    "user_input_annotated": "string",
    "correct_annotated": "string",
    "rule_violated": "string",
    "rule_explanation_hi": "string"
  } or null
}
grammar_breakdown must be null when is_correct is true.
"""


async def evaluate_answer(
    question_text: str, correct_answer: str, user_answer: str, concept_slug: str
) -> dict:
    user_prompt = (
        f"Question: {question_text}\n"
        f"Correct Answer: {correct_answer}\n"
        f"User Answer: {user_answer}\n"
        f"Concept: {concept_slug}\n"
        f"{EVAL_SCHEMA}"
    )
    return await gemini_request(EVALUATOR_SYSTEM, user_prompt)
