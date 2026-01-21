from app.microservice.CustomLanguageModel import CustomLanguageModel
from app.services.TocBuilder import TOCBuilder
from app.services.BookReader import get_page_text
from app.services.QuestionGeneration import QuestionGenerator
from app.services.GetBookToc import get_toc
import json
path_book_toc = "book_toc.json"

def main():
    bookid = "f5e98f33-0d76-4605-a029-ebb255b57091"
    '''
    toc = get_page_text(bookid, start_page=0, num_pages=35) # lay muc luc tu 35 trang dau tien
    toc_builder = TOCBuilder(llm_type="mistral", path=path_book_toc) # tao doi tuong TOCBuilder
    toc_builder.append(toc, path_book_toc, bookid) # them muc luc vao file json'''

    #tao demo 3 cau hoi trac nghiem tu chuong 1 den chuong 2
    for chapter in get_toc(path_book_toc, bookid)["chapters"][:2]:
        print(f"Chương: {chapter['chapter_name']}")
        chapter_text = get_page_text(bookid, start_page=chapter["start_page"], num_pages = chapter["end_page"] - chapter["start_page"] + 1)
        qg = QuestionGenerator(llm_type="mistral")
        questions = qg.generate(chapter_text, num_questions=2, max_new_tokens=1024)
        print(questions.model_dump_json(indent=4, ensure_ascii=False))


if __name__ == "__main__":
    main()