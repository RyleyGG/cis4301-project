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
@router.post('/changes-in-size-and-frequency-form-submission', response_model=List[FireIncident], response_model_by_alias=False)
async def search_fire_incidents(filters: WildFireChangesInSizeAndFrequencyFilters, db: Session = Depends(get_session)):
    query_statement = """
    SELECT YEAR_OF_FIRE, AVG(SIZE_ACRES) AS Avg_Fire_Size, COUNT(ID) AS Total_Number_of_Fires, SUM(SIZE_ACRES) AS TOTAL_FIRES_SIZE
    FROM \"FireIncident\"
    """

    # Check if both min and max year filters are provided
    if filters.startDate is not None and filters.endDate is not None:
        query_statement += f"WHERE YEAR_OF_FIRE BETWEEN {filters.startDate} AND {filters.endDate}"
    
    query_statement += """
    GROUP BY YEAR_OF_FIRE
    ORDER BY YEAR_OF_FIRE
    """

    print(query_statement)
    query_statement = select(FireIncident).from_statement(text(query_statement))
    return_obj = db.execute(query_statement).all()
    return return_obj

## Wildfire Types Based on Geography Query
@router.post('/type-of-wildfire-form-submission', response_model=List[FireIncident], response_model_by_alias=False)
async def search_fire_incidents(filters: WildfireTypesBasedOnGeoFilters, db: Session = Depends(get_session)):
    query_statement = """
    SELECT 
        YEAR_OF_FIRE,
        CAUSE_DESCRIPTION,
        AVG(SIZE_ACRES) AS Avg_Fire_Size,
        COUNT(ID) AS Total_Number_of_Fires,
        SUM(SIZE_ACRES) AS TOTAL_FIRES_SIZE,
        COUNT(CAUSE_DESCRIPTION) AS FIRE_TYPE,
        GEOGRAPHIC_AREA_CODE AS GEO_AREA
    FROM 
        \"FireIncident\"
    JOIN 
        \"ReportingAgency\" ON \"FireIncident\".AGENCY_CODE_ID = \"ReportingAgency\".AGENCY_CODE
    JOIN 
        \"NWCGUnit\" ON \"ReportingAgency\".REPORTING_UNIT_ID = \"NWCGUnit\".UNIT_ID
    """
    if len(filters.model_dump().keys()) != 0:
        query_statement += ' WHERE'
        if filters.startDate:
            query_statement += f" YEAR_OF_FIRE BETWEEN {filters.startDate} AND {filters.endDate}"
    
    
    query_statement += """
    GROUP BY 
        YEAR_OF_FIRE,
        CAUSE_DESCRIPTION,
        GEOGRAPHIC_AREA_CODE
    ORDER BY 
        YEAR_OF_FIRE,
        Total_Number_of_Fires DESC
    """

    print(query_statement)
    result = db.execute(text(query_statement), {'GeoAreaCode': geographic_area_code}).fetchall()
    return result

