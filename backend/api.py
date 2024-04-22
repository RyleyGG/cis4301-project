from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import func
from sqlmodel import SQLModel, Session, select
from models.db_models import Dummy, FireIncident, NWCGUnit, ReportingAgency
from models.dto_models import TblSizeResp

from routers import dummy_router, fire_incident_router, trend_router
from services.api_utility_service import engine, get_session


@asynccontextmanager
async def on_startup(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield

app = FastAPI(
    lifespan=on_startup
)

app.include_router(dummy_router.router, prefix='/dummy', tags=['Dummy'])
app.include_router(trend_router.router, prefix='/trends', tags=['Trends'])
app.include_router(fire_incident_router.router, prefix='/fire_incidents', tags=['FireIncidents'])

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/write')
async def root(db: Session = Depends(get_session)):
    newDummy = Dummy(some_str='Hello world')
    db.add(newDummy)
    db.commit()

    return {'message': 'Hello World'}


@app.get('/read')
async def root(db: Session = Depends(get_session)):
    dummy_val = db.exec(select(Dummy)).first()
    return {'message': dummy_val.some_str}


@app.get('/db_status', response_model=TblSizeResp, response_model_by_alias=False)
async def get_db_status(db: Session = Depends(get_session)):
    fire_count = select(func.count()).select_from(FireIncident)
    nwcg_count = select(func.count()).select_from(NWCGUnit)
    reporting_agency_count = select(func.count()).select_from(ReportingAgency)
    fire_size = db.exec(fire_count).one()
    ncwg_size = db.exec(nwcg_count).one()
    reporting_agency_size = db.exec(reporting_agency_count).one()
    total = fire_size + ncwg_size + reporting_agency_size

    return TblSizeResp(
        fire_incident_size=fire_size,
        nwcg_unit_size=ncwg_size,
        reporting_agency_size=reporting_agency_size,
        total_size=total
    )



