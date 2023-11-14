import datetime
from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel
import sqlmodel


class License_LicenseRestriction_Link(SQLModel, table=True):
    license_id: Optional[int] = Field(default=None, foreign_key="license.id", primary_key=True)
    source_id: Optional[int] = Field(default=None, foreign_key="licenserestriction.id", primary_key=True)

class License_LicenseDomain_Link(SQLModel, table=True):
    license_id: Optional[int] = Field(default=None, foreign_key="license.id", primary_key=True)
    domain_id: Optional[int] = Field(default=None, foreign_key="licensedomain.id", primary_key=True)

class LicenseSourceBase(SQLModel):
    name: str

class LicenseSource(LicenseSourceBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(unique=True)
    restrictions: Optional["LicenseRestriction"] = Relationship(back_populates="source")

class LicenseDomainBase(SQLModel):
    name: str 

class LicenseDomain(LicenseDomainBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(unique=True)
    restrictions: Optional["LicenseRestriction"] = Relationship(back_populates="domain")
    licenses: list['License'] = Relationship(back_populates='specifiedDomains', link_model=License_LicenseDomain_Link)

class LicenseRestrictionBase(SQLModel):
    text: str
    source_id: int
    domain_id: int

class LicenseRestriction(LicenseRestrictionBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    text: str = Field(nullable=False)
    approved: bool = Field(default=False)
    source_id: int = Field(default=1, foreign_key="licensesource.id")
    source: Optional[LicenseSource] = Relationship(back_populates="restrictions")
    domain_id: int = Field(default=1, foreign_key="licensedomain.id")
    domain: Optional[LicenseDomain] = Relationship(back_populates="restrictions")
    licenses_with_additionalRestrictions: list['License'] = Relationship(back_populates='additionalRestrictions', link_model=License_LicenseRestriction_Link)

class LicenseBase(SQLModel):
    timestamp: datetime.datetime = sqlmodel.Field(
      sa_column=sqlmodel.Column(
          sqlmodel.DateTime(timezone=True),
          nullable=False
      )
  )
    id: Optional[int] = Field(default=None, primary_key=True)
    artifact: str = Field(nullable=False)
    license: str = Field(nullable=False)
    data: bool = Field(default=False)
    application: bool = Field(default=False)
    model: bool = Field(default=False)
    sourcecode: bool = Field(default=False)
    derivatives: bool = Field(default=False)
    researchOnly: bool = Field(default=False)

class LicenseCreate(LicenseBase):
    specifiedDomain_ids: list[int]
    additionalRestriction_ids: list[int]

class License(LicenseBase, table=True):
    specifiedDomains: list[LicenseDomain] = Relationship(back_populates='licenses', link_model=License_LicenseDomain_Link)
    additionalRestrictions: list[LicenseRestriction] = Relationship(back_populates='licenses_with_additionalRestrictions', link_model=License_LicenseRestriction_Link)

class LicenseRead(LicenseBase):
    specifiedDomains: list[LicenseDomain] = []
    additionalRestrictions: list[LicenseRestriction] = []