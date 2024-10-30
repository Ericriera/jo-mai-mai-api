from fastapi import FastAPI
from routers import questions, suggestions


app = FastAPI()

app.include_router(questions.router)
app.include_router(suggestions.router)
