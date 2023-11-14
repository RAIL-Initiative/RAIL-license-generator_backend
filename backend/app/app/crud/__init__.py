from .crud_user import user
from .crud_license import license
from .crud_license_source import license_source
from .crud_license_domain import license_domain
from .crud_license_restriction import license_restriction

# For a new basic set of CRUD operations you could just do

# from .base import CRUDBase
# from app.models.item import Item
# from app.schemas.item import ItemCreate, ItemUpdate

# item = CRUDBase[Item, ItemCreate, ItemUpdate](Item)
