from fastapi import FastAPI, Depends
from contextlib import asynccontextmanager

from sqlalchemy.orm import Session

from db.db_connection import get_db, db_create_all
from models.user_models import Notes, Base
from schemas.user_schema import Notes_Schema, Notes_Schema_response


@asynccontextmanager
async def lifespan(app: FastAPI):
    db_create_all()
    print('Creating/Updating db tables')
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/create_note", response_model=Notes_Schema_response)
def create_note(note: Notes_Schema, db: Session = Depends(get_db)):
    new_note = Notes(
        test_note=note.test_note
    )
    db.add(new_note)
    db.commit()
    return new_note
