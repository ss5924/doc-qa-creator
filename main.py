import asyncio
import logging
from tqdm import tqdm

from langchain.text_splitter import RecursiveCharacterTextSplitter

from sqlalchemy import select
from database import async_session, mongo_collection
from models import QAPair
from config import setup_logger
from openai_manager import generate_questions_throttled


def split_text(text, chunk_size=512, overlap=64):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=overlap,
        separators=["\n\n", "\n", ".", " "]  # 청크분할 우선순위
    )
    return splitter.split_text(text)


async def process_document(doc, session, num_questions=3):
    arxiv_id = doc.get("arxiv_id")
    text = doc.get("cleaned_text")
    if not arxiv_id or not text:
        return

    stmt = select(QAPair).where(QAPair.arxiv_id == arxiv_id).limit(1)
    result = await session.execute(stmt)
    if result.scalar():
        logging.info(f"[{arxiv_id}] Already processed.. Skip.")
        return

    chunks = split_text(text)
    qa_objs = []

    for idx, chunk in enumerate(tqdm(chunks, desc=f"[{arxiv_id}]")):
        questions = await generate_questions_throttled(chunk, num_q=num_questions)
        for q in questions:
            qa_objs.append(QAPair(
                arxiv_id=arxiv_id,
                chunk_index=idx,
                question=q,
                passage=chunk
            ))

    if qa_objs:
        session.add_all(qa_objs)
        await session.commit()
        logging.info(f"[{arxiv_id}] Completed. count:{len(qa_objs)}")


async def run_batch(limit=100):
    cursor = mongo_collection.find({"cleaned_text": {"$exists": True}})
    count = 0

    async with async_session() as session:
        async for doc in cursor:
            await process_document(doc, session)
            count += 1
            if count >= limit:
                break


if __name__ == "__main__":
    setup_logger()
    asyncio.run(run_batch(limit=100))
