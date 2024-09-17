from datetime import datetime, timezone
from fastapi import APIRouter, HTTPException, status
from db.models.question import Question
from db.schemas.question import full_question_schema, questions_schema
from db.client import db_client
from bson import ObjectId

router = APIRouter(prefix="/questions", tags=["questions"])


@router.get("/", response_model=list)
async def get_questions():
    return questions_schema(
        db_client.questions.find(
            projection={"created_at": False, "updated_at": False}
        )
    )


@router.get("/{id}", response_model=Question)
async def get_question(id: str):
    return search_question("_id", ObjectId(id))


@router.post("/", response_model=Question, status_code=status.HTTP_201_CREATED)
async def post_question(question: Question):
    question_dict = dict(question)
    del question_dict["id"]
    time = datetime.now(timezone.utc).isoformat()
    question_dict["created_at"] = time
    question_dict["updated_at"] = time

    id = db_client.questions.insert_one(question_dict).inserted_id

    return search_question("_id", ObjectId(id))


@router.put("/", response_model=Question)
async def put_question(question: Question):
    question_dict = dict(question)
    del question_dict["id"]
    time = datetime.now(timezone.utc).isoformat()
    question_dict["updated_at"] = time

    updated = db_client.questions.find_one_and_replace(
        {"_id": ObjectId(question.id)}, question_dict
    )

    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The question does not exist",
        )

    return search_question("_id", ObjectId(question.id))


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_question(id: str):
    found = db_client.questions.find_one_and_delete({"_id": ObjectId(id)})

    if not found:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The question does not exist",
        )


def search_question(field: str, key):
    question = db_client.questions.find_one({field: key})

    if not question:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The question does not exist",
        )

    return Question(**full_question_schema(question))
