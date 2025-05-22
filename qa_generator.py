import logging

from langchain.text_splitter import RecursiveCharacterTextSplitter
from tqdm import tqdm

import openai_manager
import posgresql_repository
from models import QAPair


def split_text(text, chunk_size=512, overlap=64):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=overlap,
        separators=["\n\n", "\n", ".", " "]
    )
    return splitter.split_text(text)


async def generate_qa_chunks(arxiv_id: str, text: str, num_questions=3):
    chunks = split_text(text)
    qa_objs = []

    for idx, chunk in enumerate(tqdm(chunks, desc=f"[{arxiv_id}]")):
        questions = await openai_manager.generate_questions(chunk, num_q=num_questions)
        for q in questions:
            qa_objs.append(QAPair(
                arxiv_id=arxiv_id,
                chunk_index=idx,
                question=q,
                passage=chunk
            ))

    return qa_objs


async def generate_qa_from_doc(doc, session, num_questions=3):
    arxiv_id = doc.get("arxiv_id")
    text = doc.get("cleaned_text")

    if not arxiv_id or not text:
        logging.warning("Missing arxiv_id or cleaned_text. Skipping document.")
        return

    if (await posgresql_repository.qa_pair_exists(session, arxiv_id)).scalar():
        logging.info(f"[{arxiv_id}] Already processed. Skipping.")
        return

    qa_objs = await generate_qa_chunks(arxiv_id, text, num_questions)

    if qa_objs:
        session.add_all(qa_objs)
        await session.commit()
        logging.info(f"[{arxiv_id}] QA generation complete. Total pairs: {len(qa_objs)}")
