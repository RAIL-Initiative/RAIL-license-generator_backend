import datetime
from typing import TYPE_CHECKING, Literal, Optional
import uuid as uuid_pkg
from sqlalchemy import String
from pydantic import root_validator, validator
from sqlmodel import Field, Relationship, SQLModel
import sqlmodel
from dulwich.repo import Repo

from .link_tables import License_LicenseRestriction_Link
if TYPE_CHECKING:
    from .license_restriction import LicenseRestriction, License_LicenseRestriction_Link


class LicenseBase(SQLModel):
    timestamp: datetime.datetime = sqlmodel.Field(nullable=False, sa_type=sqlmodel.DateTime(timezone=True))
    name: str = Field(nullable=False)
    license: Literal["OpenRAIL", "ResearchRAIL", "RAIL"] = Field(nullable=False, sa_type=String)
    application: bool = Field(default=False)
    model: bool = Field(default=False)
    sourcecode: bool = Field(default=False)
    data: bool = Field(default=False)

    @root_validator
    def check_passwords_match(cls, values):
        if not (values.get('application') or values.get('model') or values.get('sourcecode') or values.get('data')):
            raise ValueError('At least one artifact must be selected.')
        return values

class LicenseCreate(LicenseBase):
    # insert minimum list size
    restriction_ids: list[int] = Field(min_items=1)
    
class License(LicenseBase, table=True):
    id: uuid_pkg.UUID = Field(
        default_factory=uuid_pkg.uuid4,
        primary_key=True,
        index=True,
        nullable=False,
    )
    git_commit_hash: str = Field(
        nullable=False,
        default=Repo.discover().head().decode("ascii")
    )
    restrictions: list["LicenseRestriction"] = Relationship(back_populates='licenses_with_restrictions', link_model=License_LicenseRestriction_Link)

class LicenseRead(LicenseBase):
    id: uuid_pkg.UUID
    restrictions: list["LicenseRestriction"]
    git_commit_hash: str