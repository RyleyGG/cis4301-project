from sqlalchemy import delete
from sqlmodel import SQLModel, Session

from models.db_models import FireIncident, ReportingAgency, NWCGUnit
from services.api_utility_service import engine


def main():
    SQLModel.metadata.create_all(engine)
    connection = engine.connect()

    # Prep session
    session = Session(bind=connection)
    session.exec(delete(FireIncident))
    session.exec(delete(ReportingAgency))
    session.exec(delete(NWCGUnit))


if __name__ == '__main__':
    main()
