from typing import List, Optional

from fastapi import APIRouter, Depends
from sqlalchemy import text, func
from sqlmodel import Session, select

from models.db_models import FireIncident
from models.dto_models import FireIncidentFilters, FireIncidentSearch
from services.api_utility_service import get_session

router = APIRouter()


@router.post('/search', response_model=FireIncidentSearch, response_model_by_alias=False)
async def search_fire_incidents(filters: FireIncidentFilters, db: Session = Depends(get_session)):
    query_statement = (
        'SELECT * FROM "FireIncident"'
    )

    key_list = list(filters.model_dump().keys())
    try:
        key_list.pop(key_list.index('skip'))
    except ValueError:
        pass
    try:
        key_list.pop(key_list.index('take'))
    except ValueError:
        pass

    if len(key_list) != 0:
        query_statement += ' WHERE'
        if filters.size_category:
            query_statement += f" size_category = '{filters.size_category}'"
        if filters.year_of_fire_min:
            query_statement += ' AND' if filters.size_category else ''
            query_statement += f" year_of_fire >= {filters.year_of_fire_min}"
        if filters.year_of_fire_max:
            query_statement += ' AND' if filters.size_category or filters.year_of_fire_min else ''
            query_statement += f" year_of_fire <= {filters.year_of_fire_max}"

    query_statement += f" OFFSET {filters.skip if filters.skip else '0'} ROWS FETCH NEXT {filters.take if filters.take else '100'} ROWS ONLY"

    exec_stmt = select(FireIncident).from_statement(text(query_statement))
    res = db.execute(exec_stmt).all()
    return_fires = []
    for obj in res:
        return_fires.append(obj._mapping['FireIncident'])

    count_query = query_statement.replace('SELECT *', 'SELECT COUNT(*)').split(' OFFSET')[0]
    total_count = db.execute(text(count_query)).scalar_one()
    return_obj = {
        'fire_incidents': return_fires,
        'total_count': total_count,
    }

    print(query_statement)
    return return_obj
