from datetime import datetime, timezone
from fastapi import APIRouter, HTTPException, status
from db.models.suggestion import Suggestion
from db.schemas.suggestion import full_suggestion_schema, suggestions_schema
from db.client import db_client

router = APIRouter(prefix="/suggestions", tags=["suggestions"])
suggestions = db_client.collection("suggestions")


@router.get("/", response_model=list)
async def get_suggestions():
    suggestions_ref = suggestions.stream()

    suggestions_list = [{**s.to_dict(), "id": s.id} for s in suggestions_ref]

    return suggestions_schema(suggestions_list)


@router.get("/{id}", response_model=Suggestion)
async def get_suggestion(id: str):
    return search_suggestion(id)


@router.post("/", response_model=Suggestion, status_code=status.HTTP_201_CREATED)
async def post_suggestion(suggestion: Suggestion):
    suggestion_dict = dict(suggestion)
    del suggestion_dict["id"]
    suggestion_dict["created_at"] = datetime.now(timezone.utc).isoformat()

    _, suggestion_ref = suggestions.add(suggestion_dict)

    return search_suggestion(suggestion_ref.id)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_suggestion(id: str):
    suggestion_ref = suggestions.document(id)
    suggestion = suggestion_ref.get()

    if not suggestion.exists:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The suggestion does not exist",
        )

    suggestion_ref.delete()


def search_suggestion(id: str):
    suggestion_ref = suggestions.document(id)
    suggestion = suggestion_ref.get()

    if not suggestion.exists:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The suggestion does not exist",
        )

    suggestion_data = suggestion.to_dict()
    suggestion_data["id"] = suggestion.id

    return Suggestion(**full_suggestion_schema(suggestion_data))
