from datetime import datetime
from http.client import HTTPException
from typing import List, Optional

from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlmodel import Session, select

from models.db_models import FireIncident, ReportingAgency, NWCGUnit
from models.dto_models import FireIncidentFilters, WildFireChangesInSizeAndFrequency, AgencyContaintmentTime, \
    WildfireSizeBasedOnGeoFilters, WildFireSizesBasedOnGeo, WildfireTypesBasedOnGeo, \
    WildFireChangesInSizeAndFrequencyFilters, WildfireTypesBasedOnGeoFilters, AgencyContaintmentTimeFilters, \
    SizeOfWildfireTypesFilters, SizeOfWildfireTypesData, UnitInformation
from services.api_utility_service import get_session

router = APIRouter()


@router.get("/")
async def root():
    return {'message': 'Hello From the Trends router!'}


@router.get('/unit_information', response_model=List[UnitInformation], response_model_by_alias=False)
async def get_unit_information(db: Session = Depends(get_session)):
    query_statement = "SELECT DISTINCT unit_name, geographic_area_code FROM \"NWCGUnit\""
    print(query_statement)
    return_obj = db.execute(text(query_statement)).fetchall()
    return return_obj


@router.get('/cause_descriptions', response_model=List[str], response_model_by_alias=False)
async def get_cause_descriptions(db: Session = Depends(get_session)):
    query_statement = "SELECT DISTINCT cause_description FROM \"FireIncident\""
    print(query_statement)
    exec_obj = db.execute(text(query_statement)).fetchall()
    return_obj = []
    for obj in exec_obj:
        return_obj.append(obj._mapping['cause_description'])
    return return_obj

## Wildfire Changes In Size And Frequency Query
@router.post('/changes-in-size-and-frequency', response_model=List[WildFireChangesInSizeAndFrequency], response_model_by_alias=False)
async def wildfire_changes_in_size_and_freq_query(filters: WildFireChangesInSizeAndFrequencyFilters, db: Session = Depends(get_session)):
    query_statement = "SELECT year_of_fire, AVG(size_acres) AS avg_fire_size, COUNT(id) AS total_number_of_fires, SUM(size_acres) AS total_fires_size FROM \"FireIncident\""

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
        if filters.start_date:
            query_statement += f" year_of_fire >= {filters.start_date}"
        if filters.end_date:
            query_statement += " AND" if filters.end_date else ''
            query_statement += f" year_of_fire <= {filters.end_date}"


    # Complete the query with grouping and ordering
    query_statement += " GROUP BY year_of_fire ORDER BY year_of_fire"

    print(query_statement)
    return_obj = db.execute(text(query_statement)).fetchall()
    return return_obj


@router.post('/type-of-wildfire-geo', response_model=List[WildfireTypesBasedOnGeo], response_model_by_alias=False)
async def wildfires_based_on_geo(filters: WildfireTypesBasedOnGeoFilters, db: Session = Depends(get_session)):

    # Constructing the base query
    query_statement = ("SELECT year_of_fire, cause_description, geographic_area_code, AVG(size_acres) AS avg_fire_size, COUNT(id) AS total_number_of_fires," +
                       " SUM(size_acres) AS total_fires_size, COUNT(cause_description) AS cause_description_count" +
                       " FROM \"FireIncident\"" +
                       " JOIN \"ReportingAgency\" ON \"FireIncident\".AGENCY_CODE_ID = \"ReportingAgency\".AGENCY_CODE" +
                       " JOIN \"NWCGUnit\" ON \"ReportingAgency\".REPORTING_UNIT_ID = \"NWCGUnit\".UNIT_ID")

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
        if filters.start_date:
            query_statement += f" year_of_fire >= {filters.start_date}"
        if filters.end_date:
            query_statement += " AND" if filters.end_date else ''
            query_statement += f" year_of_fire <= {filters.end_date}"
        if filters.geographic_area:
            query_statement += " AND" if filters.start_date or filters.end_date else ''
            query_statement += ' ('
            for item in filters.geographic_area:
                query_statement += f"geographic_area_code = '{item}' OR "
            query_statement = query_statement[:-4]
            query_statement += ')'
        if filters.cause_description:
            query_statement += " AND" if filters.start_date or filters.end_date or filters.geographic_area else ''
            query_statement += ' ('
            for item in filters.cause_description:
                query_statement += f"cause_description = '{item}' OR "
            query_statement = query_statement[:-4]
            query_statement += ')'

    # Completing the query with grouping and ordering
    query_statement += " GROUP BY year_of_fire, cause_description, geographic_area_code ORDER BY year_of_fire, total_number_of_fires DESC"

    print(query_statement)
    return_obj = db.execute(text(query_statement)).fetchall()
    return return_obj
    

@router.post("/agency-containment-time-form", response_model=List[AgencyContaintmentTime], response_model_by_alias=False)
async def agency_containtment_time_vs_size_query(filters: AgencyContaintmentTimeFilters, db: Session = Depends(get_session)):
    # Construct the SQL query

    if isinstance(filters.start_date, str):
        filters.start_date = datetime.fromisoformat(filters.start_date)
    if isinstance(filters.end_date, str):
        filters.end_date = datetime.fromisoformat(filters.end_date)

    query_parts = [
        "SELECT DISTINCT YEAR_OF_FIRE, REPORTING_UNIT_NAME, (CONTAINMENT_DATETIME - DISCOVERY_DATETIME) AS Time_To_Contain, COUNT(ID) AS Total_Fires, AVG(SIZE_ACRES) AS AVG_SIZE_OF_FIRES",
        "FROM \"FireIncident\"",
        "JOIN \"ReportingAgency\" ON \"FireIncident\".AGENCY_CODE_ID = \"ReportingAgency\".AGENCY_CODE",
        "JOIN \"NWCGUnit\" ON \"ReportingAgency\".REPORTING_UNIT_ID = \"NWCGUnit\".UNIT_ID"
    ]

    conditions = [
        f"YEAR_OF_FIRE >= {filters.start_date.year}",
        f"YEAR_OF_FIRE <= {filters.end_date.year}",
        f"AGENCY_NAME = '{filters.reporting_agency}'",
    ]

    if conditions:
        query_parts.append("WHERE " + " AND ".join(conditions))


    query_parts.append("GROUP BY YEAR_OF_FIRE, REPORTING_UNIT_NAME, (CONTAINMENT_DATETIME - DISCOVERY_DATETIME) ORDER BY YEAR_OF_FIRE, REPORTING_UNIT_NAME")

     # Combining all parts of the query into a single string
    query_statement = " ".join(query_parts)
    print("QUERY: ", query_statement)  # Log the query for debugging

    
    # Executing the query
    try:
        result = db.execute(text(query_statement)).all()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/size-of-wildfire-types-form-submission", response_model=List[SizeOfWildfireTypesFilters], response_model_by_alias=False)
async def size_of_wildfire_types_query(filters: SizeOfWildfireTypesData, db: Session = Depends(get_session)):
    # Construct the SQL query using safe parameter binding

    if isinstance(filters.start_date, str):
        filters.start_date = datetime.fromisoformat(filters.start_date)
    if isinstance(filters.end_date, str):
        filters.end_date = datetime.fromisoformat(filters.end_date)


    query_parts = [
        "SELECT YEAR_OF_FIRE, AGENCY_NAME, COUNT(ID) as Fires, AVG(SIZE_ACRES) AS Avg_Fire_Size, MAX(SIZE_ACRES) AS Largest_Fire_Size",
        "FROM \"FireIncident\"",
        "JOIN \"ReportingAgency\" ON \"FireIncident\".AGENCY_CODE_ID = \"ReportingAgency\".AGENCY_CODE",
        "JOIN \"NWCGUnit\" ON \"ReportingAgency\".REPORTING_UNIT_ID = \"NWCGUnit\".UNIT_ID"
    ]
    
    conditions = [
        f"YEAR_OF_FIRE >= {filters.start_date.year}",
        f"YEAR_OF_FIRE <= {filters.end_date.year}",
        f"AGENCY_NAME = '{filters.reporting_agency}'"
        f"CAUSE_DESCRIPTION = '{filters.wildfire_type}'"
    ]

    if conditions:
        query_parts.append("WHERE " + " AND ".join(conditions))


    query_parts.append("GROUP BY YEAR_OF_FIRE, AGENCY_NAME ORDER BY YEAR_OF_FIRE, AGENCY_NAME")

     # Combining all parts of the query into a single string
    query_statement = " ".join(query_parts)
    print("QUERY: ", query_statement)  # Log the query for debugging

    
    # Executing the query
    try:
        result = db.execute(text(query_statement)).all()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/size-of-wildfire-based-on-geographic-area-form-submission", response_model=List[WildFireSizesBasedOnGeo], response_model_by_alias=False)
async def wildfire_size_based_on_geo_query(filters: WildfireSizeBasedOnGeoFilters, db: Session = Depends(get_session)):
    # Construct the SQL query using safe parameter binding

    if isinstance(filters.start_date, str):
        filters.start_date = datetime.fromisoformat(filters.start_date)
    if isinstance(filters.end_date, str):
        filters.end_date = datetime.fromisoformat(filters.end_date)


    query_parts = [
        "SELECT YEAR_OF_FIRE, STATE_AFFILIATION, COUNT(ID) AS Fires, AVG(SIZE_ACRES) AS Avg_Fire_Size, MAX(SIZE_ACRES) AS Largest_Fire_Size",
        "FROM \"FireIncident\"",
        "JOIN \"ReportingAgency\" ON \"FireIncident\".AGENCY_CODE_ID = \"ReportingAgency\".AGENCY_CODE",
        "JOIN \"NWCGUnit\" ON \"ReportingAgency\".REPORTING_UNIT_ID = \"NWCGUnit\".UNIT_ID"
    ]
    
    conditions = [
        f"YEAR_OF_FIRE >= {filters.start_date.year}",
        f"YEAR_OF_FIRE <= {filters.end_date.year}",
        f"STATE_AFFILIATION = '{filters.geographic_area}'"
    ]

    if conditions:
        query_parts.append("WHERE " + " AND ".join(conditions))


    query_parts.append("GROUP BY YEAR_OF_FIRE, STATE_AFFILIATION ORDER BY YEAR_OF_FIRE, STATE_AFFILIATION")

     # Combining all parts of the query into a single string
    query_statement = " ".join(query_parts)
    print("QUERY: ", query_statement)  # Log the query for debugging

    
    # Executing the query
    try:
        result = db.execute(text(query_statement)).all()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
