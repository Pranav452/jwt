from fastapi import FastAPI
from app.db import Base, engine
from app.routers import users, groups, expenses

from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(lifespan=lifespan)

@app.get("/")
def root():
    return {"message": "Hello World"}

app.include_router(users.router)
app.include_router(groups.router)
app.include_router(expenses.router)

# To enable 'reload' or 'workers', run with:
# uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
