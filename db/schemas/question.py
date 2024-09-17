def full_question_schema(question) -> dict:
    return {
        "id": str(question["_id"]),
        "question": question["question"],
        "categories": question["categories"],
        "created_at": question["created_at"],
        "updated_at": question["updated_at"],
    }


def question_schema(question) -> dict:
    return {
        "id": str(question["_id"]),
        "question": question["question"],
        "categories": question["categories"],
    }


def questions_schema(questions) -> list:
    return [question_schema(question) for question in questions]
