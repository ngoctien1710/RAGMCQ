import os
import json
from app.microservice.CustomLanguageModel import CustomLanguageModel
from app.utils.JsonUtils import extract_json
from app.domain.Book import assign_hierarchical_ids, Book


class TOCBuilder:

    def __init__(self, llm_type: str, path: str):
        
        if not os.path.exists(path) or os.path.getsize(path) == 0:
            self.data = []
        else:
            with open(path, "r", encoding="utf-8") as f:
                self.data = json.load(f)
        self.llm = CustomLanguageModel(llm_type)

    def has_book(self, book_id: str) -> bool:
        return any(b.get("book_id") == book_id for b in self.data)

    @staticmethod
    def parse_book(response: str) -> Book:
        try:
            raw_toc = json.loads(response)
        except json.JSONDecodeError:
            raw_toc = extract_json(response)

        return Book(**raw_toc)
  

    def append(self, book_toc: str, path: str, book_id: str, max_new_tokens: int = 12000):
        if self.has_book(book_id):
            print("Book TOC already exists. Skipping append.")
            return
        
        prompt = self._build_prompt(book_toc)
        response = self.llm.generate(prompt, max_new_tokens=max_new_tokens)

        book = self.parse_book(response)
        book = assign_hierarchical_ids(book_id, book)

        self.data.append(book.model_dump())

        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.data, f, ensure_ascii=False, indent=4)

    def _build_prompt(self, toc: str) -> str:
        return f"""
            Dựa trên nội dung mục lục sau, hãy tạo cấu trúc sách đúng logic. 
            hãy bỏ qua các phần không liên quan đến mục lục.
            Không bịa thêm.

            FORMAT JSON:
            {Book.model_json_schema()}

            MỤC LỤC NGUỒN:
            \"\"\"{toc}\"\"\"

            CHỈ OUTPUT JSON OBJECT.
            KHÔNG markdown.
            KHÔNG ```json
            KHÔNG giải thích.

        """
