from fastapi import APIRouter
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


router = APIRouter()

class FormData(BaseModel):
    startDate: datetime
    endDate: datetime
    agency: Optional[str] = None
    wildfireType: Optional[str] = None
    geographicArea: Optional[str] = None


@router.get("/")
async def root():
    return {'message': 'Hello From the Dummy router!'}

@router.post("/agency-containment-time-form")
async def submitContainmentForm(data: FormData):
    return {"message": "Form received", "data": data}

@router.post("/changes-in-size-and-frequency-form-submission")
async def submitContainmentForm(data: FormData):
    return {"message": "Form received", "data": data}


@router.post("/size-of-wildfire-types-form-submission")
async def submitSizeForm(data: FormData):
    return {"message": "Form received", "data": data}

@router.post("/type-of-wildfire-form-submission")
async def submitSizeForm(data: FormData):
    return {"message": "Form received", "data": data}

@router.post("/size-of-wildfire-based-on-geographic-area-form-submission")
async def submitSizeForm(data: FormData):
    return {"message": "Form received", "data": data}

