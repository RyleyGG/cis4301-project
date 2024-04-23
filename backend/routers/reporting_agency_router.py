from typing import List, Optional

from fastapi import APIRouter, Depends
from sqlalchemy import text, func
from sqlmodel import Session, select

from models.db_models import NWCGUnit, ReportingAgency
from models.dto_models import ReportingAgencyFilters, ReportingAgencySearch
from services.api_utility_service import get_session

router = APIRouter()


@router.post('/search', response_model=ReportingAgencySearch, response_model_by_alias=False)
async def search_reporting_agencies(filters: ReportingAgencyFilters, db: Session = Depends(get_session)):
    query_statement = (
        'SELECT * FROM "ReportingAgency"'
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
        if filters.agency_code:
            query_statement += f" agency_code like '%{filters.agency_code}%'"
        if filters.reporting_unit_id:
            query_statement += ' AND' if filters.agency_code else ''
            query_statement += f" reporting_unit_id like '%{filters.reporting_unit_id}%'"
        if filters.reporting_unit_name:
            query_statement += ' AND' if filters.agency_code or filters.reporting_unit_id else ''
            query_statement += f" reporting_unit_name like '%{filters.reporting_unit_name}%'"

    query_statement += f" OFFSET {filters.skip if filters.skip else '0'} ROWS FETCH NEXT {filters.take if filters.take else '100'} ROWS ONLY"

    exec_stmt = select(ReportingAgency).from_statement(text(query_statement))
    res = db.execute(exec_stmt).all()
    return_agencies = []
    for obj in res:
        return_agencies.append(obj._mapping['ReportingAgency'])

    count_query = query_statement.replace('SELECT *', 'SELECT COUNT(*)').split(' OFFSET')[0]
    total_count = db.execute(text(count_query)).scalar_one()
    return_obj = {
        'reporting_agencies': return_agencies,
        'total_count': total_count,
    }

    print(query_statement)
    return return_obj
