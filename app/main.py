import uvicorn
from fastapi import FastAPI, Depends
from contextlib import asynccontextmanager
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from db.db_connection import get_db, db_create_all
from models.user_models import Notes, Base
from schemas.user_schema import Notes_Schema, Notes_Schema_response
from authentication import user_auth_routes
from app.routes.recipe_routes import recipe_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    db_create_all()
    print('Creating/Updating db tables')
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(user_auth_routes.router, prefix="/user", tags=["User Auth"])
app.include_router(recipe_router)


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


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
