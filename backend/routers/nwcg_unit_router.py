from typing import List, Optional

from fastapi import APIRouter, Depends
from sqlalchemy import text, func
from sqlmodel import Session, select

from models.db_models import NWCGUnit
from models.dto_models import NWCGUnitSearch, NWCGUnitFilters
from services.api_utility_service import get_session

router = APIRouter()


@router.post('/search', response_model=NWCGUnitSearch, response_model_by_alias=False)
async def search_nwcg_units(filters: NWCGUnitFilters, db: Session = Depends(get_session)):
    query_statement = (
        'SELECT * FROM "NWCGUnit"'
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

    cleaned_key_list = []
    for key in key_list:
        if filters.model_dump()[key] is not None:
            cleaned_key_list.append(key)
    key_list = cleaned_key_list

    if len(key_list) != 0:
        query_statement += ' WHERE'
        if filters.agency_name:
            query_statement += f" agency_name like '%{filters.agency_name}%'"
        if filters.wildland_role:
            query_statement += ' AND' if filters.agency_name else ''
            query_statement += f" wildland_role like '%{filters.wildland_role}%'"
        if filters.geographic_area_code:
            query_statement += ' AND' if filters.agency_name or filters.wildland_role else ''
            query_statement += f" geographic_area_code like '%{filters.geographic_area_code}%'"

    query_statement += f" OFFSET {filters.skip if filters.skip else '0'} ROWS FETCH NEXT {filters.take if filters.take else '100'} ROWS ONLY"

    exec_stmt = select(NWCGUnit).from_statement(text(query_statement))
    res = db.execute(exec_stmt).all()
    return_units = []
    for obj in res:
        return_units.append(obj._mapping['NWCGUnit'])

    count_query = query_statement.replace('SELECT *', 'SELECT COUNT(*)').split(' OFFSET')[0]
    total_count = db.execute(text(count_query)).scalar_one()
    return_obj = {
        'nwcg_units': return_units,
        'total_count': total_count,
    }

    print(query_statement)
    return return_obj
