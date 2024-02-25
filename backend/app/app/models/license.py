import datetime
from typing import TYPE_CHECKING, Literal, Optional
import uuid as uuid_pkg
from sqlalchemy import String
from pydantic import root_validator

from sqlmodel import Field, Relationship, SQLModel
import sqlmodel

from .link_tables import License_LicenseRestriction_Link, License_LicenseDomain_Link
if TYPE_CHECKING:
    from .license_restriction import LicenseRestriction, License_LicenseRestriction_Link
    from .license_domain import LicenseDomain, License_LicenseDomain_Link, LicenseDomainRead

class LicenseBase(SQLModel):
    timestamp: datetime.datetime = sqlmodel.Field(nullable=False, sa_type=sqlmodel.DateTime(timezone=True))
    name: str = Field(nullable=False)
    license: Literal["OpenRAIL", "ResearchRAIL", "RAIL"] = Field(nullable=False, sa_type=String)
    application: bool = Field(default=False)
    model: bool = Field(default=False)
    sourcecode: bool = Field(default=False)

class LicenseCreate(LicenseBase):
    restriction_ids: Optional[list[int]] = []
    
class License(LicenseBase, table=True):
    id: uuid_pkg.UUID = Field(
        default_factory=uuid_pkg.uuid4,
        primary_key=True,
        index=True,
        nullable=False,
    )
    restrictions: list["LicenseRestriction"] = Relationship(back_populates='licenses_with_restrictions', link_model=License_LicenseRestriction_Link)

class LicenseRead(LicenseBase):
    id: uuid_pkg.UUID
    restrictions: list["LicenseRestriction"]