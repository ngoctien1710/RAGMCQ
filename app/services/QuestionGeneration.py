import json
from app.microservice.CustomLanguageModel import CustomLanguageModel
from app.domain.MCQSet import MCQSet
from app.utils.JsonUtils import extract_json

class QuestionGenerator:

    def __init__(self, llm_type="mistral"):
        self.llm = CustomLanguageModel(llm_type)

    def generate(self, context: str, num_questions: int = 5, max_new_tokens: int = 512) -> MCQSet:
        prompt = self._build_prompt(context, num_questions)
        response = self.llm.generate(prompt, max_new_tokens=max_new_tokens)

        try:
            data = json.loads(response)
        except json.JSONDecodeError:
            data = extract_json(response)

        mcq_set = MCQSet(**data)

        if len(mcq_set.questions) != num_questions:
            raise ValueError("Wrong number of MCQs generated")

        return mcq_set
    

    def _build_prompt(self, context: str, num_questions: int) -> str:
        return f"""
            Từ nội dung sau, hãy tạo {num_questions} câu hỏi trắc nghiệm (MCQ).

            YÊU CẦU:
            - Mỗi câu hỏi có 4 lựa chọn (options)
            - Mỗi câu chỉ có 1 đáp án đúng
            - correct_index là chỉ số trong options
            - Không bịa ngoài nội dung
            - Không thêm text ngoài JSON
            - trong nội dung câu hỏi đừng nhắc đến câu hỏi được lấy từ trang nào, chương nào hay tài liệu nào cả nếu nó không cần thiết.

            OUTPUT PHẢI THEO JSON SCHEMA SAU:
            {MCQSet.model_json_schema()}

            NỘI DUNG:
            \"\"\"{context}\"\"\"
        """

if __name__ == "__main__":
    context = "Python is a high-level, interpreted programming language known for its readability and versatility. It supports multiple programming paradigms, including procedural, object-oriented, and functional programming."
    qg = QuestionGenerator()
    mcq_set = qg.generate(context, num_questions=3)
    print(mcq_set.model_dump_json(indent=4, ensure_ascii=False))