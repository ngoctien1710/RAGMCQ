from typing import List
from pydantic import BaseModel
from app.domain.MCQ import MCQ
from pydantic import Field
class MCQSet(BaseModel):
    questions: List[MCQ] = Field(description="List of multiple choice questions")
