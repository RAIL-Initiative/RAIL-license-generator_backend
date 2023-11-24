from typing import Optional

from app.db.session import Session
from .base import CRUDBase
from app.models import License, LicenseCreate
    
license = CRUDBase[License, LicenseCreate, LicenseCreate](License)

