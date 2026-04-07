from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from db import Base
    
class Subject(Base):
    __tablename__ = "subjects"

    id = Column(Integer, primary_key=True)
    name = Column(String , nullable=False)
    semester = Column(Integer , nullable=False)

    papers = relationship("Papers", back_populates="subject")

class Papers(Base):
    __tablename__ = "papers"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    subjectID = Column(Integer, ForeignKey(Subject.id), nullable=False)
    subject = relationship("Subject" , back_populates="papers")
    year = Column(Integer, nullable=False)
    examType = Column(String, nullable=False)
    # branch = Column(String, nullable=False)
    semester = Column(Integer , nullable=False)
    pdf = Column(String, nullable=True)

