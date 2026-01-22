from pydantic import BaseModel, Field
from typing import List

class MCQ(BaseModel):
    stem: str = Field(description="The question text")
    options: List[str] = Field(description="List of answer options")
    correct_index: int = Field(description="0-based index of the correct option")
    rationale: str = Field(
        description="The content provided is intended to prove the correct answer."
    )
    book_id: str = Field(description="Book ID copied exactly from the prompt")
    part_id: str = Field(description="part ID is the ID of the section of the page whose content is used to create the question. please follow toc structure.")

