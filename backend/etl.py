import sqlite3
from sqlite3 import Cursor

from sqlalchemy import delete
from sqlmodel import SQLModel, Session, select, func
import os

from models.db_models import FireIncident, ReportingAgency, NWCGUnit
from services.api_utility_service import engine


def load_nwcg_unit_data(cursor: Cursor, db: Session):
    cursor.execute('SELECT '
                   'UnitId,'
                   'Parent,'
                   'Agency,'
                   'Department,'
                   'State,'
                   'WildlandRole,'
                   'Gacc,'
                   'Name,'
                   'UnitType,'
                   'Code,'
                   'State,'
                   'Country'
                   ' FROM NWCG_UNITIDActive_20170109')
    rows = cursor.fetchall()
    for row in rows:
        new_unit_obj = NWCGUnit(
            unit_id=row[0],
            parent_agency=row[1],
            agency_name=row[2],
            department_or_state=row[3] if row[3] else row[4],
            wildland_role=row[5],
            geographic_area_code=row[6],
            unit_name=row[7],
            unit_type=row[8],
            unit_code=row[9],
            state_affiliation=row[10],
            country=row[11]
        )
        db.add(new_unit_obj)
    db.commit()


def load_reporting_agency_data(cursor: Cursor, db: Session):
    cursor.execute('SELECT DISTINCT '
                   'NWCG_REPORTING_AGENCY,'
                   'NWCG_REPORTING_UNIT_ID,'
                   'NWCG_REPORTING_UNIT_NAME'
                   ' FROM Fires ')
    rows = cursor.fetchall()
    for row in rows:
        new_reporting_agency_obj = ReportingAgency(
            agency_code=row[0],
            reporting_unit_id=row[1],
            reporting_unit_name=row[2]
        )
        db.add(new_reporting_agency_obj)
    db.commit()


def load_fire_data(cursor: Cursor, db: Session):
    cursor.execute('SELECT '
                   'FOD_ID,'
                   'STAT_CAUSE_CODE,'
                   'STAT_CAUSE_DESCR,'
                   'DISCOVERY_DATE,'
                   'DISCOVERY_TIME,'
                   'CONT_DATE,'
                   'CONT_TIME,'
                   'FIRE_SIZE,'
                   'FIRE_SIZE_CLASS,'
                   'FIRE_YEAR,'
                   'FIPS_NAME,'
                   'FIPS_CODE,'
                   'LONGITUDE,'
                   'LATITUDE,'
                   'FIRE_NAME,'
                   'FIRE_CODE,'
                   'NWCG_REPORTING_AGENCY'
                   ' FROM Fires')

    rows = cursor.fetchall()
    for row in rows:
        # TODO: add datetimes
        new_fire_obj = FireIncident(
            id=row[0],
            cause_code=row[1],
            cause_description=row[2],
            discovery_datetime=None,
            containment_datetime=None,
            size_acres=row[7],
            size_category=row[8],
            year_of_fire=row[9],
            fips_name=row[10],
            fips_code=row[11],
            longitude=row[12],
            latitude=row[13],
            fire_name=row[14],
            fire_code=row[15],
            agency_code_id=row[16]
        )
        db.add(new_fire_obj)
    db.commit()


def main():
    if not os.path.exists(f'{os.getcwd()}\kaggle_db.sqlite'):
        raise Exception('Local database file not found')

    SQLModel.metadata.create_all(engine)
    oracle_connection = engine.connect()

    # Prep session
    session = Session(bind=oracle_connection)
    session.exec(delete(FireIncident))
    session.exec(delete(ReportingAgency))
    session.exec(delete(NWCGUnit))

    # Create SQLite connection
    sqlite_connection = sqlite3.connect(f'{os.getcwd()}\kaggle_db.sqlite', detect_types=sqlite3.PARSE_DECLTYPES)
    cursor = sqlite_connection.cursor()

    # Perform ETL tasks
    print('Starting database migration... this may take a while\n', flush=True)
    print('Loading NWCG Unit data...', flush=True)
    load_nwcg_unit_data(cursor, session)
    print('Loading Reporting Agency data...', flush=True)
    load_reporting_agency_data(cursor, session)
    print('Loading Fire data...', flush=True)
    load_fire_data(cursor, session)
    fire_count = select(func.count()).select_from(FireIncident)
    nwcg_count = select(func.count()).select_from(NWCGUnit)
    reporting_agency_count = select(func.count()).select_from(ReportingAgency)
    total = session.exec(fire_count).one() + session.exec(nwcg_count).one() + session.exec(reporting_agency_count).one()
    print(f'\nETL complete! The total number of rows in the database is: {total}', flush=True)


if __name__ == '__main__':
    main()
