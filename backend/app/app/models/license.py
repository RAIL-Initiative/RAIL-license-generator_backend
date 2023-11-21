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
    artifact: Literal["", "A", "M", "S", "AS", "AM", "MS", "AMS"] = Field(nullable=False, sa_type=String)
    license: Literal["OpenRAIL", "ResearchRAIL", "RAIL"] = Field(nullable=False, sa_type=String)
    data: bool = Field(default=False)
    application: bool = Field(default=False)
    model: bool = Field(default=False)
    sourcecode: bool = Field(default=False)
    derivatives: bool = Field(default=False)
    researchOnly: bool = Field(default=False)

class LicenseCreate(LicenseBase):
    specifiedDomain_ids: Optional[list[int]] = []
    additionalRestriction_ids: Optional[list[int]] = []

    @root_validator
    def check_license_options(cls, values) -> 'LicenseCreate':
        if values.get("license") == 'OpenRAIL' and not ( values.get("derivatives") and not values.get("researchOnly")):
            raise ValueError('OpenRAIL license requires derivatives to be true and researchOnly to be false')
        if values.get("license") == 'ResearchRAIL' and not ( not values.get("derivatives") and values.get("researchOnly")):
            raise ValueError('ResearchRAIL license requires derivatives to be false and researchOnly to be true')
        if values.get("license") == 'RAIL' and not (not values.get("derivatives") and not values.get("researchOnly")):
            raise ValueError('RAIL license requires derivatives to be false and researchOnly to be false')
        return values
    
class License(LicenseBase, table=True):
    id: uuid_pkg.UUID = Field(
        default_factory=uuid_pkg.uuid4,
        primary_key=True,
        index=True,
        nullable=False,
    )
    specifiedDomains: list["LicenseDomain"] = Relationship(back_populates='licenses', link_model=License_LicenseDomain_Link)
    additionalRestrictions: list["LicenseRestriction"] = Relationship(back_populates='licenses_with_additionalRestrictions', link_model=License_LicenseRestriction_Link)

class LicenseRead(LicenseBase):
    id: uuid_pkg.UUID
    specifiedDomains: list["LicenseDomainRead"]
    additionalRestrictions: list["LicenseRestriction"]