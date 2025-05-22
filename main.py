import asyncio
import logging

import database
import logger_config
import qa_generator

logger_config.setup_logger()
logger = logging.getLogger(__name__)


async def run_batch(limit=10):
    cursor = database.mongo_collection.find({"cleaned_text": {"$exists": True}})
    count = 0

    async with database.async_session() as session:
        async for doc in cursor:
            await qa_generator.generate_qa_from_doc(doc, session)
            count += 1
            if count >= limit:
                break


def main():
    asyncio.run(run_batch(limit=10))


if __name__ == "__main__":
    main()
