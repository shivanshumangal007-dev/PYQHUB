from sqlalchemy import Column, Integer, String
from db import Base

class Papers(Base):
    __tablename__ = "papers"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    subject = Column(String, nullable=False)
    year = Column(Integer, nullable=False)
    examType = Column(String, nullable=False)
    # branch = Column(String, nullable=False)
    semester = Column(Integer, nullable=False)
    pdf = Column(String, nullable=True)
    