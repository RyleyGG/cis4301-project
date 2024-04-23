from datetime import datetime
from http.client import HTTPException
from typing import List, Optional

from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlmodel import Session, select

from models.db_models import FireIncident, ReportingAgency, NWCGUnit
from models.dto_models import FireIncidentFilters, WildFireChangesInSizeAndFrequency, wildfireSizeBasedOnGeoFilters, WildfireTypesBasedOnGeo, WildFireChangesInSizeAndFrequencyFilters, WildfireTypesBasedOnGeoFilters, SizeOfWildfireTypesFilters, AgencyContaintmentTimeFilters
from services.api_utility_service import get_session

router = APIRouter()


@router.get("/")
async def root():
    return {'message': 'Hello From the Trends router!'}


    return return_obj

## TODO: Fix Queries structure and 

## Wildfire Changes In Size And Frequency Query
@router.post('/changes-in-size-and-frequency-form-submission', response_model=List[WildFireChangesInSizeAndFrequency], response_model_by_alias=False)
async def wildfire_changes_in_size_and_freq_query(filters: WildFireChangesInSizeAndFrequencyFilters, db: Session = Depends(get_session)):
    # Ensure date strings are converted to datetime objects
    if isinstance(filters.start_date, str):
        filters.start_date = datetime.fromisoformat(filters.start_date)
    if isinstance(filters.end_date, str):
        filters.end_date = datetime.fromisoformat(filters.end_date)

    query_statement = ["SELECT YEAR_OF_FIRE, AVG(SIZE_ACRES) AS Avg_Fire_Size, COUNT(ID) AS Total_Number_of_Fires, SUM(SIZE_ACRES) AS TOTAL_FIRES_SIZE FROM \"FireIncident\""]
    conditions = [
        f"YEAR_OF_FIRE >= {filters.start_date.year}",
        f"YEAR_OF_FIRE <= {filters.end_date.year}",]



    # Combine conditions into a single WHERE clause if applicable
    if conditions:
        query_statement.append("WHERE " + " AND ".join(conditions))

    # Complete the query with grouping and ordering
    query_statement.append("GROUP BY YEAR_OF_FIRE ORDER BY YEAR_OF_FIRE")

    # Join all parts of the query into a single string
    query_statement = " ".join(query_statement)


    print("QUERY: ", query_statement)
    query_statement = select(FireIncident).from_statement(text(query_statement))
    print("QUERY AFTER: ", query_statement)
    return_obj = db.execute(query_statement).all()
    print("RETURN OBJ: ", return_obj)
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
    

@router.post("/agency-containment-time-form")
async def agency_containtment_time_vs_size_query(filters: AgencyContaintmentTimeFilters, db: Session = Depends(get_session)):
    # Construct the SQL query

    if isinstance(filters.start_date, str):
        filters.start_date = datetime.fromisoformat(filters.start_date)
    if isinstance(filters.end_date, str):
        filters.end_date = datetime.fromisoformat(filters.end_date)

    query_parts = [
        "SELECT DISTINCT YEAR_OF_FIRE, REPORTING_UNIT_NAME, COUNT(ID) AS Total_Fires",
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


    query_parts.append("GROUP BY YEAR_OF_FIRE, REPORTING_UNIT_NAME ORDER BY YEAR_OF_FIRE, REPORTING_UNIT_NAME")

     # Combining all parts of the query into a single string
    query_statement = " ".join(query_parts)
    print("QUERY: ", query_statement)  # Log the query for debugging

    
    # Executing the query
    try:
        result = db.execute(text(query_statement)).all()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/size-of-wildfire-types-form-submission")
async def size_of_wildfire_types_query(filters: SizeOfWildfireTypesFilters, db: Session = Depends(get_session)):
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


@router.post("/size-of-wildfire-based-on-geographic-area-form-submission")
async def wildfire_size_based_on_geo_query(filters: wildfireSizeBasedOnGeoFilters, db: Session = Depends(get_session)):
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
