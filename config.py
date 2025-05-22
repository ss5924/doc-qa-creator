import os

from dotenv import load_dotenv

load_dotenv(override=True)

POSTGRESQL_DB_URL = os.getenv("POSTGRESQL_DB_URL")
MONGO_DB_URL = os.getenv("MONGO_DB_URL")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GPT_CONCURRENCY = 2
GPT_DELAY_RANGE = (2.5, 4.0)

HF_API_TOKEN = os.getenv("HF_API_TOKEN")
