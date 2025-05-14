from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from openai_service import call_llm


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


@app.get("/ask")
def handle_question(userid: str, question: str):
    """
    Handle the question from the user.
    """
    response = call_llm(userid, question)

    return {"response": response}