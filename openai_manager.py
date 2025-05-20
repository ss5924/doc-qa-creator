import asyncio
import random
import logging
from openai import AsyncOpenAI
from config import OPENAI_API_KEY

client = AsyncOpenAI(api_key=OPENAI_API_KEY)

GPT_CONCURRENCY = 2
GPT_DELAY_RANGE = (2.5, 4.0)
gpt_semaphore = asyncio.Semaphore(GPT_CONCURRENCY)


async def generate_questions_throttled(chunk, num_q=3):
    async with gpt_semaphore:
        await asyncio.sleep(random.uniform(*GPT_DELAY_RANGE))
        prompt = f"""다음 단락을 바탕으로 한국어 질문 1~{num_q}개를 생성해 주세요.

\"\"\"
{chunk}
\"\"\"

질문:"""
        try:
            response = await client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
            )
            raw = response.choices[0].message.content.strip()
            return [q.strip("-•1234567890. ").strip() for q in raw.split("\n") if q.strip()]
        except Exception as e:
            logging.info(f"[GPT Error] {e}")
            return []
