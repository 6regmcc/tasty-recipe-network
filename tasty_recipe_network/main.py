import uvicorn
from fastapi import FastAPI, Depends
from contextlib import asynccontextmanager
from sqlalchemy.orm import Session

from tasty_recipe_network.db.db_connection import get_db, db_create_all
from tasty_recipe_network.models.user_models import Notes
from tasty_recipe_network.schemas.user_schema import Notes_Schema, Notes_Schema_response
from tasty_recipe_network.routes import user_auth_routes
from tasty_recipe_network.routes.recipe_routes import recipe_router, recipe_router_no_auth


@asynccontextmanager
async def lifespan(app: FastAPI):
    db_create_all()
    print('Creating/Updating db tables')
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(user_auth_routes.router, prefix="/user", tags=["User Auth"])
app.include_router(recipe_router)
app.include_router(recipe_router_no_auth)


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
