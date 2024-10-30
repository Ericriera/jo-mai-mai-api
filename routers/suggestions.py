from datetime import datetime, timezone
from fastapi import APIRouter, HTTPException, status
from db.models.suggestion import Suggestion
from db.schemas.suggestion import full_suggestion_schema, suggestions_schema
from db.client import db_client
from bson import ObjectId

router = APIRouter(prefix="/suggestions", tags=["suggestions"])


@router.get("/", response_model=list)
async def get_suggestions():
    return suggestions_schema(
        db_client.suggestions.find(projection={"created_at": False})
    )


@router.get("/{id}", response_model=Suggestion)
async def get_suggestion(id: str):
    return search_suggestion("_id", ObjectId(id))


@router.post("/", response_model=Suggestion, status_code=status.HTTP_201_CREATED)
async def post_suggestion(suggestion: Suggestion):
    suggestion_dict = dict(suggestion)
    del suggestion_dict["id"]
    suggestion_dict["created_at"] = datetime.now(timezone.utc).isoformat()

    id = db_client.suggestions.insert_one(suggestion_dict).inserted_id

    return search_suggestion("_id", ObjectId(id))


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_suggestion(id: str):
    found = db_client.suggestions.find_one_and_delete({"_id": ObjectId(id)})

    if not found:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The suggestion does not exist",
        )


def search_suggestion(field: str, key):
    suggestion = db_client.suggestions.find_one({field: key})

    if not suggestion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The suggestion does not exist",
        )

    return Suggestion(**full_suggestion_schema(suggestion))
