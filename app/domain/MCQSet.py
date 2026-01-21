from typing import List
from pydantic import BaseModel
from app.domain.MCQ import MCQ

class MCQSet(BaseModel):
    questions: List[MCQ]
