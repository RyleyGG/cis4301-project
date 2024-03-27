from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel, Session, select
from models.db_models import Dummy

from routers import dummy_router
from services.api_utility_service import engine, get_session


@asynccontextmanager
async def on_startup(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield

app = FastAPI(
    lifespan=on_startup
)

app.include_router(dummy_router.router, prefix='/dummy', tags=['Dummy'])

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/write")
async def root(db: Session = Depends(get_session)):
    newDummy = Dummy(some_str='Hello world')
    db.add(newDummy)
    db.commit()

    return {'message': 'Hello World'}


@app.get("/read")
async def root(db: Session = Depends(get_session)):
    dummy_val = db.exec(select(Dummy)).first()
    return {'message': dummy_val.some_str}