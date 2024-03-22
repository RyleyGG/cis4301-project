from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import dummy_router


@asynccontextmanager
async def on_startup(app: FastAPI):
    # TODO: Get connection with Oracle working
    # SQLModel.metadata.create_all(engine)
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


@app.get("/")
async def root():
    return {'message': 'Hello World'}