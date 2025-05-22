from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import QAPair


async def qa_pair_exists(session: AsyncSession, arxiv_id):
    result = await session.execute(
        select(QAPair)
        .where(QAPair.arxiv_id == arxiv_id)
        .limit(1))
    return result
