from typing import Optional, List, Dict
import uuid
from sqlmodel import SQLModel, Field


class Dummy(SQLModel, table=True):
    __tablename__ = 'Dummy'
    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True, index=True)
    some_str: str
