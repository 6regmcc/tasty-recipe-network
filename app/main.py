from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from db.db_connection import get_db, db_create_all
from models.user_models import Notes, Base
from schemas.user_schema import Notes_Schema

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}



@app.post("/create_user")
def create_user(note: Notes_Schema, db: Session = Depends(get_db)):
    new_note = Notes(
        test_note = note.test_note
    )
    db.add(new_note)
    db.commit()


@app.on_event("startup")
def create_tables():
    db_create_all()
    print('Creating/Updating db tables')
