import requests

from fastapi import FastAPI, Response
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate

from models.question import Question

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/ask_question")
async def ask_question(question: Question):
    type = question.type
    if type == "langchain":
        llm = ChatOllama(
            model="llama3.2:1b",
            temperature=0,
            base_url="http://localhost:8080",
        )
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You are a helpful assistant.",
                ),
                ("human", "{input}"),
            ]
        )

        chain = prompt | llm
        output = chain.invoke(
            {
                "input": question.question,
            }
        )
        return Response(content=output.json(), media_type="application/json")
    if type == "request":
        response = requests.post("http://localhost:8080/api/generate", json={
            "prompt": question.question,
            "stream": False,
            "model": "llama3.2:1b"
        })
        if response.status_code != 200:
            return Response(content="Error", media_type="application/json", status_code=500)
        return Response(content=response.text, media_type="application/json")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)
