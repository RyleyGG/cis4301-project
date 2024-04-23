from datetime import datetime
from http.client import HTTPException
from typing import List, Optional

from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlmodel import Session, select

from models.db_models import FireIncident, ReportingAgency, NWCGUnit
from models.dto_models import FireIncidentFilters, WildFireChangesInSizeAndFrequency,AgencyContaintmentTime, WildfireSizeBasedOnGeoFilters, WildFireSizesBasedOnGeo, WildfireTypesBasedOnGeo, WildFireChangesInSizeAndFrequencyFilters, WildfireTypesBasedOnGeoFilters, AgencyContaintmentTimeFilters, SizeOfWildfireTypesFilters, SizeOfWildfireTypesData
from services.api_utility_service import get_session

router = APIRouter()


@router.get("/")
async def root():
    return {'message': 'Hello From the Trends router!'}


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


@router.post('/type-of-wildfire-form-submission', response_model=List[WildfireTypesBasedOnGeo], response_model_by_alias=False)
async def size_of_types_of_wildfires(filters: WildfireTypesBasedOnGeoFilters, db: Session = Depends(get_session)):
    # Convert strings to datetime objects if needed
    if isinstance(filters.start_date, str):
        filters.start_date = datetime.fromisoformat(filters.start_date)
    if isinstance(filters.end_date, str):
        filters.end_date = datetime.fromisoformat(filters.end_date)

    # Constructing the base query
    query_parts = [
        "SELECT YEAR_OF_FIRE, CAUSE_DESCRIPTION, AVG(SIZE_ACRES) AS Avg_Fire_Size, COUNT(ID) AS Total_Number_of_Fires,",
        "SUM(SIZE_ACRES) AS TOTAL_FIRES_SIZE, COUNT(CAUSE_DESCRIPTION) AS FIRE_TYPE",
        "FROM \"FireIncident\"",
        "JOIN \"ReportingAgency\" ON \"FireIncident\".AGENCY_CODE_ID = \"ReportingAgency\".AGENCY_CODE",
        "JOIN \"NWCGUnit\" ON \"ReportingAgency\".REPORTING_UNIT_ID = \"NWCGUnit\".UNIT_ID"
    ]

    # Building the conditions for the WHERE clause
    conditions = [
        f"YEAR_OF_FIRE >= {filters.start_date.year}",
        f"YEAR_OF_FIRE <= {filters.end_date.year}",
        f"GEOGRAPHIC_AREA_CODE = '{filters.geographic_area}'",
        f"CAUSE_DESCRIPTION = '{filters.wildfire_type}'"
    ]

    # Adding the WHERE clause if there are conditions
    if conditions:
        query_parts.append("WHERE " + " AND ".join(conditions))

    # Completing the query with grouping and ordering
    query_parts.append(
        "GROUP BY YEAR_OF_FIRE, CAUSE_DESCRIPTION, GEOGRAPHIC_AREA_CODE ORDER BY YEAR_OF_FIRE, Total_Number_of_Fires DESC"
    )

    # Combining all parts of the query into a single string
    query_statement = " ".join(query_parts)
    

    # Executing the query
    print("QUERY: ", query_statement)
    return_obj = db.execute(text(query_statement)).fetchall()
    print(return_obj)
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
