from typing import Optional

from app.db.session import Session
from .base import CRUDBase
from app.models import LicenseRestriction, LicenseRestrictionBase
    
license_restriction = CRUDBase[LicenseRestriction, LicenseRestrictionBase, LicenseRestrictionBase](LicenseRestriction)

