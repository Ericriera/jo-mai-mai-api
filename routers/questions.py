from datetime import datetime, timezone
from fastapi import APIRouter, HTTPException, status
from db.models.question import Question
from db.schemas.question import full_question_schema, questions_schema
from db.client import db_client

router = APIRouter(prefix="/questions", tags=["questions"])
questions = db_client.collection("questions")


@router.get("/", response_model=list)
async def get_questions(category: str = None):
    if category:
        questions_ref = questions.where(
            "categories", "array_contains", category
        ).stream()
    else:
        questions_ref = questions.stream()

    question_list = [{**q.to_dict(), "id": q.id} for q in questions_ref]

    return questions_schema(question_list)


@router.get("/{id}", response_model=Question)
async def get_question(id: str):
    return search_question(id)


@router.post("/", response_model=Question, status_code=status.HTTP_201_CREATED)
async def post_question(question: Question):
    question_dict = dict(question)
    del question_dict["id"]
    time = datetime.now(timezone.utc).isoformat()
    question_dict["created_at"] = time
    question_dict["updated_at"] = time

    _, question_ref = questions.add(question_dict)
    return search_question(question_ref.id)


@router.put("/", response_model=Question)
async def put_question(question: Question):
    question_dict = dict(question)
    del question_dict["id"]
    time = datetime.now(timezone.utc).isoformat()
    question_dict["updated_at"] = time

    question_ref = questions.document(question.id)
    question = question_ref.get()

    if not question.exists:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The question does not exist",
        )

    question_ref.set(question_dict)

    return search_question(question.id)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_question(id: str):
    question_ref = questions.document(id)
    question = question_ref.get()

    if not question.exists:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The question does not exist",
        )

    question_ref.delete()


def search_question(id: str):
    question_ref = questions.document(id)
    question = question_ref.get()

    if not question.exists:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The question does not exist",
        )

    question_data = question.to_dict()
    question_data["id"] = question.id

    return Question(**full_question_schema(question_data))
