import requests

from fastapi import FastAPI, Response
from models.question import Question

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/ask_question")
async def ask_question(question: Question):
    response = requests.post("http://ollama:11434/api/generate", json={
        "prompt": question.question,
        "stream": False,
        "model": "llama3.2"
    })
    if response.status_code != 200:
        return Response(content="Error", media_type="application/json", status_code=500)
    return Response(content=response.text, media_type="application/json")
