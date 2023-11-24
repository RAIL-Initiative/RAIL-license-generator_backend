import datetime
from typing import TYPE_CHECKING, Literal, Optional

from sqlmodel import Field, Relationship, SQLModel
import sqlmodel

from .link_tables import License_LicenseRestriction_Link

if TYPE_CHECKING:
    from .license_restriction import License_LicenseRestriction_Link
    from .license_source import LicenseSource
    from .license_domain import LicenseDomain
    from .license import License

class LicenseRestrictionBase(SQLModel):
    text: str
    source_id: int
    domain_id: int

class LicenseRestriction(LicenseRestrictionBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    text: str = Field(nullable=False)
    approved: bool = Field(default=False)
    source_id: int = Field(foreign_key="licensesource.id")
    source: Optional["LicenseSource"] = Relationship(back_populates="restrictions")
    domain_id: int = Field(foreign_key="licensedomain.id")
    domain: Optional["LicenseDomain"] = Relationship(back_populates="restrictions")
    licenses_with_additionalRestrictions: list["License"] = Relationship(back_populates='additionalRestrictions', link_model=License_LicenseRestriction_Link)