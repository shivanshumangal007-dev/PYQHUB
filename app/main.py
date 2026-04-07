import os

from fastapi import FastAPI, Depends, HTTPException, Form , UploadFile, File
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from jose import JWTError, jwt

from auth import create_access_token, create_refresh_token, get_current_user
app = FastAPI()
from sqlalchemy.orm import session
from db import db_engine,SessionLocal
from models import Base, Papers, Subject
from schema import LoginRequest, PaperCreate, SubjectBulkCreate, getPaperSchema
import cloudinary.uploader

Base.metadata.create_all(bind=db_engine)

app = FastAPI()

origins = [
    "http://localhost:5173",   # React
    "http://127.0.0.1:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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
async def createPaper(
    title: str = Form(...),
    subject_id: int = Form(...),
    year: int = Form(...),
    examType: str = Form(...),
    semester: int = Form(...),
    file: UploadFile = File(...),
    user=Depends(get_current_user), 
    db: session = Depends(get_db)
):

    result = cloudinary.uploader.upload(
        file.file,
        resource_type="raw"
    )

    file_url = result["secure_url"]


    new_paper = Papers(
        title=title,
        subjectID=subject_id,
        year=year,
        examType=examType,
        semester=semester,
        pdf=file_url
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

@app.post("/get-papers")
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


@app.post("/login")
def login(data : LoginRequest):
    
    # TEMP: hardcoded user
    if data.username != os.getenv("USERNAME") or data.password != os.getenv("PASSWORD"):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    access_token = create_access_token({"sub": data.username})
    refresh_token = create_refresh_token({"sub": data.username})

    return {
        "access": access_token,
        "refresh": refresh_token
    }


@app.post("/refresh-token")
def refresh_token(token: str = Form(...)):
    try:
        payload = jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=[os.getenv("ALGORITHM")])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    new_access_token = create_access_token({"sub": username})
    return {"access": new_access_token}