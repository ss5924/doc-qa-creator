import os
from dotenv import load_dotenv
import logging

# .env 파일 로드
load_dotenv(override=True)

# DB 설정
POSTGRESQL_DB_URL = os.getenv("POSTGRESQL_DB_URL")
MONGO_DB_URL = os.getenv("MONGO_DB_URL")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


# logging 설정
def setup_logger():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        filename='/app/logs/app.log',
    )
