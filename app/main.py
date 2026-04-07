from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import JSONResponse
app = FastAPI()
from sqlalchemy.orm import session
from db import db_engine,SessionLocal
from models import Base, Papers, Subject
from schema import PaperCreate, SubjectBulkCreate, getPaperSchema

Base.metadata.create_all(bind=db_engine)


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


# @app.get("/")
# def hello():
#     return JSONResponse(status_code = 200, content = {"message": "hello man"})


@app.post("/add-paper")
def createPaper(paper : PaperCreate,db : session = Depends(get_db)):
    new_paper = Papers(
        title=paper.title,
        subjectID=paper.subjectID,
        year=paper.year,
        examType = paper.examType,
        semester=paper.semester,
        pdf=str(paper.pdf)
    )
    db.add(new_paper)
    db.commit()
    db.refresh(new_paper)
    
    return new_paper

@app.post("/subjects")
def addSubjects(data : SubjectBulkCreate, db : session = Depends(get_db)):
    try:
        new_subjects = []

        for subject in data.subjects:
            sub = Subject(
                name = subject,
                semester = data.semester
            )
            new_subjects.append(sub)

        
        db.add_all(new_subjects)
        db.commit()

        return JSONResponse(status_code=200 , content= {
            "message" : "subjects added successfully",
            "subjects" : data.subjects 
        })
    except Exception as err:
        return HTTPException(status_code=402 , detail=f"error in adding subjects : {err}")


@app.get("/subject/{semester}")
def get_subjectsBysemester(semester : int , db : session = Depends(get_db)):
    subjects = db.query(Subject).filter(Subject.semester == semester).all()

    result = []
    for sub in subjects:
        result.append({
            "id" : sub.id,
            "name" : sub.name 
        })
    
    return JSONResponse(status_code=200, content={
        "message" : "request recieved succesfully",
        "semester" : semester,
        "subjects" : result
    })

@app.post("/get-paper")
def getPaper(data :getPaperSchema , db : session = Depends(get_db)):
    papers = db.query(Papers).filter(Papers.subjectID.in_(data.subject)).all()
    result = []

    for paper in papers:
        result.append({
            "id": paper.id,
            "title": paper.title,
            "subject": paper.subject.name,  # 🔥 relation
            "year": paper.year,
            "examType": paper.examType,
            "semester": paper.semester,
            "pdf": paper.pdf
        })

    return JSONResponse(content= {
        "papers" : result
    }, status_code=201)