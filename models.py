from sqlalchemy import Column, Integer, Text, TIMESTAMP
from sqlalchemy.orm import declarative_base

__Base = declarative_base()


class QAPair(__Base):
    __tablename__ = "qa_pairs"
    __table_args__ = {"schema": "arxiv_raw"}

    id = Column(Integer, primary_key=True, autoincrement=True)
    arxiv_id = Column(Text, nullable=False)
    chunk_index = Column(Integer, nullable=False)
    question = Column(Text, nullable=False)
    passage = Column(Text, nullable=False)
