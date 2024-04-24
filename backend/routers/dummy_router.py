from fastapi import APIRouter, HTTPException
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


router = APIRouter()


@router.get("/")
async def root():
    return {'message': 'Hello From the Dummy router!'}


