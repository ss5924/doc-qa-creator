import asyncio
import logging
import random

from openai import AsyncOpenAI

from config import OPENAI_API_KEY, GPT_CONCURRENCY, GPT_DELAY_RANGE

__client = AsyncOpenAI(api_key=OPENAI_API_KEY)

__gpt_semaphore = asyncio.Semaphore(GPT_CONCURRENCY)


async def generate_questions(chunk, num_q=3):
    async with __gpt_semaphore:
        await asyncio.sleep(random.uniform(*GPT_DELAY_RANGE))
        prompt = f"{chunk}\n\n이 내용을 기반으로 정보성 한국어 질문 {num_q}개 작성:"
        try:
            response = await __client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
            )
            raw = response.choices[0].message.content.strip()
            return [q.strip("-•1234567890. ").strip() for q in raw.split("\n") if q.strip()]

        except Exception as e:
            logging.info(f"[GPT Error] {e}")
            return []
