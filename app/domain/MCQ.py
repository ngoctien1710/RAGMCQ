from pydantic import BaseModel
from typing import List

class MCQ(BaseModel):
    stem: str
    options: List[str]
    correct_index: int
    rationale: str

