from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import questions, suggestions


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(questions.router)
app.include_router(suggestions.router)
