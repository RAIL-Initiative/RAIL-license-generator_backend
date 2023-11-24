from typing import Optional

from app.db.session import Session
from .base import CRUDBase
from app.models import LicenseDomain, LicenseDomainBase

class CRUDLicenseDomain(CRUDBase[LicenseDomain, LicenseDomainBase, LicenseDomainBase]):
    def get_by_name(self, db: Session, *, name: str) -> Optional[LicenseDomain]:
        return db.query(LicenseDomain).filter(LicenseDomain.name == name).first()
    
license_domain = CRUDLicenseDomain(LicenseDomain)

