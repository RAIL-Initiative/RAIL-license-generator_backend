import datetime
from typing import TYPE_CHECKING, Literal, Optional

from sqlmodel import Field, Relationship, SQLModel

from .link_tables import License_LicenseDomain_Link

if TYPE_CHECKING:
    from . import LicenseRestriction, License, License_LicenseDomain_Link

class LicenseDomainBase(SQLModel):
    name: str = Field(unique=True)

class LicenseDomain(LicenseDomainBase, table=True):
    id: int = Field(default=None, primary_key=True)
    restrictions: list["LicenseRestriction"] = Relationship(back_populates="domain")
    licenses: list["License"] = Relationship(back_populates='specifiedDomains', link_model=License_LicenseDomain_Link)

class LicenseDomainRead(LicenseDomainBase):
    id: int
    restrictions: list["LicenseRestriction"] = []