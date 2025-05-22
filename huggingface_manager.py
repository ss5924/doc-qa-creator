from huggingface_hub import InferenceClient

from config import HF_API_TOKEN

client = InferenceClient(
    model="", # todo
    token=HF_API_TOKEN
)


def generate_questions(chunk: str, num_q: int = 3):
    prompt = f"{chunk}\n\n이 내용을 기반으로 정보성 한국어 질문 {num_q}개 작성:"
    output = client.text_generation(prompt, max_new_tokens=512)
    return [q.strip("-• ").strip() for q in output.split("\n") if q.strip()]
