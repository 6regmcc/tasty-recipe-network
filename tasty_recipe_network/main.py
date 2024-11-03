import os

import uvicorn
from fastapi import FastAPI
from contextlib import asynccontextmanager


from tasty_recipe_network.db.db_connection import db_create_all

from tasty_recipe_network.routes import user_auth_routes
from tasty_recipe_network.routes.recipe_routes import (
    recipe_router,
    recipe_router_no_auth,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    db_create_all()
    print("Creating/Updating db tables")
    print(f'Current env is {os.environ.get("ENVIRONMENT")}')
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(user_auth_routes.router, prefix="/user", tags=["User Auth"])
app.include_router(recipe_router)
app.include_router(recipe_router_no_auth)


@app.get("/")
async def root():
    return {"message": "Hello World"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
