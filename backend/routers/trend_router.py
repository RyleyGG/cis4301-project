from datetime import datetime
from http.client import HTTPException
from typing import List, Optional

from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlmodel import Session, select

from models.db_models import FireIncident, ReportingAgency, NWCGUnit
from models.dto_models import FireIncidentFilters, wildfireSizeBasedOnGeoFilters, WildFireChangesInSizeAndFrequencyFilters, WildfireTypesBasedOnGeoFilters, SizeOfWildfireTypesFilters, AgencyContaintmentTimeFilters
from services.api_utility_service import get_session

router = APIRouter()


@router.get("/")
async def root():
    return {'message': 'Hello From the Trends router!'}


    return return_obj


## Wildfire Changes In Size And Frequency Query
@router.post('/changes-in-size-and-frequency-form-submission')
async def search_fire_incidents(filters: WildFireChangesInSizeAndFrequencyFilters, db: Session = Depends(get_session)):
    # Ensure date strings are converted to datetime objects
    if isinstance(filters.start_date, str):
        filters.start_date = datetime.fromisoformat(filters.start_date)
    if isinstance(filters.end_date, str):
        filters.end_date = datetime.fromisoformat(filters.end_date)

    query_parts = ["SELECT YEAR_OF_FIRE, AVG(SIZE_ACRES) AS Avg_Fire_Size, COUNT(ID) AS Total_Number_of_Fires, SUM(SIZE_ACRES) AS TOTAL_FIRES_SIZE FROM \"FireIncident\""]
    conditions = []

    # Append conditions based on filters
    if filters.start_date:
        conditions.append(f"YEAR_OF_FIRE >= {filters.start_date.year}")
    if filters.end_date:
        conditions.append(f"YEAR_OF_FIRE <= {filters.end_date.year}")

    # Combine conditions into a single WHERE clause if applicable
    if conditions:
        query_parts.append("WHERE " + " AND ".join(conditions))

    # Complete the query with grouping and ordering
    query_parts.append("GROUP BY YEAR_OF_FIRE ORDER BY YEAR_OF_FIRE")

    # Join all parts of the query into a single string
    query_statement = " ".join(query_parts)


    print("QUERY: ", query_statement)
    query_statement = select(FireIncident).from_statement(text(query_statement))
    return_obj = db.execute(query_statement).all()
    return return_obj


@router.post('/type-of-wildfire-form-submission')
async def search_fire_incidents(filters: WildfireTypesBasedOnGeoFilters, db: Session = Depends(get_session)):
    # Convert strings to datetime objects if needed
    if isinstance(filters.start_date, str):
        filters.start_date = datetime.fromisoformat(filters.start_date)
    if isinstance(filters.end_date, str):
        filters.end_date = datetime.fromisoformat(filters.end_date)

    # Constructing the base query
    query_parts = [
        "SELECT YEAR_OF_FIRE, CAUSE_DESCRIPTION, AVG(SIZE_ACRES) AS Avg_Fire_Size, COUNT(ID) AS Total_Number_of_Fires,",
        "SUM(SIZE_ACRES) AS TOTAL_FIRES_SIZE, COUNT(CAUSE_DESCRIPTION) AS FIRE_TYPE, GEOGRAPHIC_AREA_CODE AS GEO_AREA",
        "FROM \"FireIncident\"",
        "JOIN \"ReportingAgency\" ON \"FireIncident\".AGENCY_CODE_ID = \"ReportingAgency\".AGENCY_CODE",
        "JOIN \"NWCGUnit\" ON \"ReportingAgency\".REPORTING_UNIT_ID = \"NWCGUnit\".UNIT_ID"
    ]

    # Building the conditions for the WHERE clause
    conditions = [
        f"YEAR_OF_FIRE >= {filters.start_date.year}",
        f"YEAR_OF_FIRE <= {filters.end_date.year}",
        f"GEOGRAPHIC_AREA_CODE = '{filters.geo_area_code}'",
        f"CAUSE_DESCRIPTION = '{filters.cause_description}'"
    ]

    # Adding the WHERE clause if there are conditions
    if conditions:
        query_parts.append("WHERE " + " AND ".join(conditions))

    # Completing the query with grouping and ordering
    query_parts.append(
        "GROUP BY YEAR_OF_FIRE, CAUSE_DESCRIPTION, GEOGRAPHIC_AREA_CODE",
        "ORDER BY YEAR_OF_FIRE, Total_Number_of_Fires DESC"
    )

    # Combining all parts of the query into a single string
    query_statement = " ".join(query_parts)
    print("QUERY: ", query_statement)  # Log the query for debugging

    # Executing the query
    try:
        result = db.execute(text(query_statement)).all()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@router.post("/agency-containment-time-form")
async def get_fire_reports(filters: AgencyContaintmentTimeFilters, db: Session = Depends(get_session)):
    # Construct the SQL query
    query = text("""
        SELECT DISTINCT
            YEAR_OF_FIRE,
            REPORTING_UNIT_NAME,
            COUNT(ID) AS Total_Fires
        FROM 
            "FireIncident"
        JOIN 
            "ReportingAgency" ON "FireIncident".AGENCY_CODE_ID = "ReportingAgency".AGENCY_CODE
        JOIN 
            "NWCGUnit" ON "ReportingAgency".REPORTING_UNIT_ID = "NWCGUnit".UNIT_ID
        WHERE
            YEAR_OF_FIRE BETWEEN :start_year AND :end_year
            AND REPORTING_UNIT_NAME = :reporting_unit_name
        GROUP BY 
            YEAR_OF_FIRE,
            REPORTING_UNIT_NAME
        ORDER BY 
            YEAR_OF_FIRE,
            REPORTING_UNIT_NAME
    """)
    
    # Execute the query with parameters
    try:
        result = db.execute(query, {
            'start_year': filters.start_year,
            'end_year': filters.end_year,
            'reporting_unit_name': filters.reporting_unit_name
        }).all()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/size-of-wildfire-based-on-geographic-area-form-submission")
async def get_fire_causes(filters: wildfireSizeBasedOnGeoFilters, db: Session = Depends(get_session)):
    # Construct the SQL query using safe parameter binding
    query = text("""
        SELECT 
            YEAR_OF_FIRE,
            CAUSE_DESCRIPTION,
            AVG(SIZE_ACRES) AS Avg_Fire_Size,
            STATE_AFFILIATION
        FROM 
            "FireIncident"
        JOIN 
            "ReportingAgency" ON "FireIncident".AGENCY_CODE_ID = "ReportingAgency".AGENCY_CODE
        JOIN 
            "NWCGUnit" ON "ReportingAgency".REPORTING_UNIT_ID = "NWCGUnit".UNIT_ID
        WHERE 
            YEAR_OF_FIRE BETWEEN :start_year AND :end_year
            AND STATE_AFFILIATION = :state_affiliation
            AND CAUSE_DESCRIPTION = :cause_description
        GROUP BY 
            YEAR_OF_FIRE,
            CAUSE_DESCRIPTION,
            STATE_AFFILIATION
        ORDER BY 
            YEAR_OF_FIRE,
            CAUSE_DESCRIPTION
    """)

    # Execute the query with parameters
    try:
        result = db.execute(query, {
            'start_year': filters.start_year,
            'end_year': filters.end_year,
            'state_affiliation': filters.state_affiliation,
            'cause_description': filters.cause_description
        }).fetchall()
        return result
    except Exception as e:
        print(f"Error executing query: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    # You can return raw results or map them to a response model
    return result




