from pydantic import BaseModel

class Question(BaseModel):
    question: str
    type: str
