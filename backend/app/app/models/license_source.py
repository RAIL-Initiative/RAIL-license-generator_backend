import datetime
from typing import TYPE_CHECKING, Literal, Optional

from sqlmodel import Field, Relationship, SQLModel
import sqlmodel

if TYPE_CHECKING:
    from . import LicenseRestriction

class LicenseSourceBase(SQLModel):
    name: str = Field(unique=True)

class LicenseSource(LicenseSourceBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    restrictions: list["LicenseRestriction"] = Relationship(back_populates="source")