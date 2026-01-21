import os
import requests
import logging
import dotenv

dotenv.load_dotenv()

LLM_MODEL_NAME_DICT = {
    "mistral": "mistral-large-latest",
}

LLM_MODEL_URL_DICT = {
    "mistral": "https://api.mistral.ai/v1/chat/completions",
}

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CustomLanguageModel:

    def __init__(self, llm_type: str):
        self.api_key = os.getenv("MISTRAL_API_KEY")
        if self.api_key is None:
            raise ValueError("Missing MISTRAL_API_KEY")

        self.llm_type = llm_type
        self.model = {
            "model_name": LLM_MODEL_NAME_DICT[llm_type],
            "model_url": LLM_MODEL_URL_DICT[llm_type]
        }

        self.max_retry_times = 3

    def generate(self, query: str, max_new_tokens: int = 512) -> str:
        url = self.model["model_url"]

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }

        payload = {
            "model": self.model["model_name"],
            "messages": [
                {"role": "user", "content": query}
            ],
            "max_tokens": max_new_tokens,
            "temperature": 0.01
        }

        for _ in range(self.max_retry_times):
            response = requests.post(url, headers=headers, json=payload)
            if response.status_code == 200:
                return response.json()["choices"][0]["message"]["content"]
            else:
                logger.warning(f"Status {response.status_code}: {response.text}")

        raise RuntimeError("Failed after retries")


if __name__ == "__main__":
    clm = CustomLanguageModel("mistral")
    response = clm.generate("why is the sky blue?")
    print(response)
