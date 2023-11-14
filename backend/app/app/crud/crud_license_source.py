from typing import Optional

from app.db.session import Session
from .base import CRUDBase
from app.models import LicenseSource, LicenseSourceBase

class CRUDLicenseSource(CRUDBase[LicenseSource, LicenseSourceBase, LicenseSourceBase]):
    def get_by_name(self, db: Session, *, name: str) -> Optional[LicenseSource]:
        return db.query(LicenseSource).filter(LicenseSource.name == name).first()
    
license_source = CRUDLicenseSource(LicenseSource)

