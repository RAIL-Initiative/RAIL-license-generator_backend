from typing import TYPE_CHECKING, Literal, Optional

from sqlmodel import Field, Relationship, SQLModel
import uuid as uuid_pkg

class License_LicenseRestriction_Link(SQLModel, table=True):
    license_id: Optional[uuid_pkg.UUID] = Field(default=None, foreign_key="license.id", primary_key=True)
    source_id: Optional[int] = Field(default=None, foreign_key="licenserestriction.id", primary_key=True)

class License_LicenseDomain_Link(SQLModel, table=True):
    license_id: Optional[uuid_pkg.UUID] = Field(default=None, foreign_key="license.id", primary_key=True)
    domain_id: Optional[int] = Field(default=None, foreign_key="licensedomain.id", primary_key=True)