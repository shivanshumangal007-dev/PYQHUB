from pydantic import BaseModel, Field, AnyUrl
from typing import Annotated, Literal, List


class PaperCreate(BaseModel):
    title : Annotated[str, Field(description="the title of the paper", min_length=1, max_length=200)]
    # subject : Annotated[str, Field(description="the subject of the paper")]
    subjectID : Annotated[int , Field(description="id of the subject")]
    year : Annotated[int, Field(description="the year of the paper")]
    examType : Annotated[Literal["midsem", "endsem"], Field(description="the type of the exam")]
    # branch : Annotated[str, Field(description="the branch of the paper")]
    semester : Annotated[int, Field(description="the semester of the paper")]
    pdf : Annotated[AnyUrl, Field(description="the link for the PDF file of the paper")]
    


class SubjectBulkCreate(BaseModel):
    semester: int
    subjects: List[str]


class getPaperSchema(BaseModel):
    semester : Annotated[int , Field(description="enter the semzter you want PYQS of" , gt=0 , le= 8)]
    exam : Annotated[Literal["midsem", "endsem"], Field(description="the type of the exam")]
    subject: Annotated[List[int] , Field(description="enter the array of subjectIds")]