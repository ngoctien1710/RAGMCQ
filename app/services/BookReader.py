import os
import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "https://qc.neureader.net/v2/readie/embedding"

TOKEN = os.getenv("NEUREADER_TOKEN")
assert TOKEN, "NEUREADER_TOKEN is not set"

HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

def get_page_text(book_id: str, start_page: int, num_pages: int = 1) -> str:
    texts = []

    for i in range(num_pages):
        payload = {
            "bookId": book_id,
            "pageNumber": start_page + i,
            "pageSize": 1
        }

        response = requests.post(
            BASE_URL,
            headers=HEADERS,
            json=payload,
            timeout=10
        )
        response.raise_for_status()

        texts.append(
            f'page physical: {start_page + i} \n' + response.json()["data"]["embeddings"][0]["text"]
        )

    return "\n".join(texts)


if __name__ == "__main__":
    book_id = "f5e98f33-0d76-4605-a029-ebb255b57091"
    start_page = 0
    num_pages = 3

    text = get_page_text(book_id, start_page, num_pages)
    print(text)
