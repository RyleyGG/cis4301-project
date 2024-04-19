from fastapi import APIRouter, HTTPException
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


router = APIRouter()

class FormData(BaseModel):
    startDate: datetime
    endDate: datetime
    agency: Optional[str] = None
    wildfireType: Optional[str] = None
    geographicArea: Optional[str] = None

submissions: List[FormData] = []


@router.get("/")
async def root():
    return {'message': 'Hello From the Dummy router!'}


# POST METHODS
@router.post("/agency-containment-time-form")
async def submit_form(data: FormData):
    print("Current Submissions:", submissions)  # Debugging output
    return {"message": "Form received", "data": data}

@router.post("/changes-in-size-and-frequency-form-submission")
async def submit_form(data: FormData):
    submissions.append(data)
    print("Current Submissions:", submissions)  # Debugging output
    return {"message": "Form received", "data": data}

@router.post("/size-of-wildfire-types-form-submission")
async def submit_form(data: FormData):
    print("Current Submissions:", submissions)  # Debugging output
    return {"message": "Form received", "data": data}

@router.post("/type-of-wildfire-form-submission")
async def submit_form(data: FormData):
    print("Current Submissions:", submissions)  # Debugging output
    return {"message": "Form received", "data": data}

@router.post("/size-of-wildfire-based-on-geographic-area-form-submission")
async def submit_form(data: FormData):
    print("Current Submissions:", submissions)  # Debugging output
    return {"message": "Form received", "data": data}


# GET METHODS
@router.get("/changes-in-size-and-frequency-form-submission")
async def get_submissions():
    if not submissions:
        raise HTTPException(status_code=404, detail="No submissions found")
    return {"message": "Submissions retrieved", "data": submissions}

@router.get("/agency-containment-time-form")
async def get_submissions():
    if not submissions:
        raise HTTPException(status_code=404, detail="No submissions found")
    return {"message": "Submissions retrieved", "data": submissions}

@router.get("/size-of-wildfire-types-form-submission")
async def get_submissions():
    if not submissions:
        raise HTTPException(status_code=404, detail="No submissions found")
    return {"message": "Submissions retrieved", "data": submissions}

@router.get("/type-of-wildfire-form-submission")
async def get_submissions():
    if not submissions:
        raise HTTPException(status_code=404, detail="No submissions found")
    return {"message": "Submissions retrieved", "data": submissions}

@router.get("/size-of-wildfire-based-on-geographic-area-form-submission")
async def get_submissions():
    if not submissions:
        raise HTTPException(status_code=404, detail="No submissions found")
    return {"message": "Submissions retrieved", "data": submissions}
