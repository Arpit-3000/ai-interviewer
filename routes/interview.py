from fastapi import APIRouter
from services.questions_generator import generate_questions

router = APIRouter()

@router.post("/start-interview")
def start_interview():

    question = generate_questions(
        "",""
    )

    return {
        "questions":question
    }