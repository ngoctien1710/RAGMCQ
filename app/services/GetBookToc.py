import json


def get_toc(path_book_toc: str, id_book: str) -> dict | None:
    with open(path_book_toc, "r", encoding="utf-8") as f:
        toc_data = json.load(f)
    for book in toc_data:
        if book["book_id"] == id_book:
            return book
    return None

if __name__ == "__main__":  
    path_book_toc = "book_toc.json"
    id_book = "f5e98f33-0d76-4605-a029-ebb255b57091"
    toc = get_toc(path_book_toc, id_book)
    if toc:
        print(json.dumps(toc, ensure_ascii=False, indent=4))
    else:
        print("Book TOC not found.")