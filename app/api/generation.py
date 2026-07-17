from fastapi import APIRouter

from app.llm.generator import LLMGenerator
from app.llm.validator import LLMValidator

router = APIRouter(
    prefix="/generate",
    tags=["Generation"]
)


@router.post("/")
def generate(document: str):

    result = LLMGenerator.generate(document)

    parsed = LLMValidator.validate(result)

    if parsed is None:
        return {
            "error": "Invalid JSON returned from LLM."
        }

    return parsed