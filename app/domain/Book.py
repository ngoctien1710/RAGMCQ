from typing import List, Optional
from pydantic import BaseModel


class Part(BaseModel):
    part_id: Optional[str]
    part_name: str
    start_page: int   # logical
    end_page: int     # logical


class Section(BaseModel):
    section_id: Optional[str]
    section_name: str
    start_page: int   # logical
    end_page: int
    parts: List[Part]


class Chapter(BaseModel):
    chapter_id: Optional[str]
    chapter_name: str
    start_page: int   # logical
    end_page: int
    sections: List[Section]


class Book(BaseModel):
    book_id: Optional[str]
    book_name: str

    content_start_page: int  
    # physical index where logical page == 1

    chapters: List[Chapter]


def assign_hierarchical_ids(book_id: str, book: Book) -> Book:
    book.book_id = book_id

    for ci, chapter in enumerate(book.chapters or [], start=1):
        chapter.chapter_id = f"{ci}"

        for si, section in enumerate(chapter.sections or [], start=1):
            section.section_id = f"{chapter.chapter_id}.{si}"

            for pi, part in enumerate(section.parts or [], start=1):
                part.part_id = f"{section.section_id}.{pi}"

    return book