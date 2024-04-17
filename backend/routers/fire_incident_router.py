from typing import List, Optional

from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlmodel import Session, select

from models.db_models import FireIncident
from models.dto_models import FireIncidentFilters
from services.api_utility_service import get_session

router = APIRouter()


@router.post('/search', response_model=List[FireIncident], response_model_by_alias=False)
async def search_fire_incidents(filters: FireIncidentFilters, db: Session = Depends(get_session)):
    query_statement = "SELECT * FROM \"FireIncident\""

    if len(filters.model_dump().keys()) != 0:
        query_statement += ' WHERE'
        if filters.size_category:
            query_statement += f" size_category = '{filters.size_category}'"
        if filters.year_of_fire_min:
            query_statement += ' AND' if filters.size_category else ''
            query_statement += f" year_of_fire <= {filters.year_of_fire_min}"
        if filters.year_of_fire_max:
            query_statement += ' AND' if filters.size_category or filters.year_of_fire_min else ''
            query_statement += f" year_of_fire >= {filters.year_of_fire_max}"

    print(query_statement)
    query_statement = select(FireIncident).from_statement(text(query_statement))
    return_obj = db.execute(query_statement).first()
    return return_obj
