from fastapi import FastAPI
from fastapi.responses import JSONResponse
app = FastAPI()
from db import db_engine
from models import Base

Base.metadata.create_all(bind = db_engine)



@app.get("/")
def hello():
    return JSONResponse(status_code = 200, content = {"message": "hello man"})