from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models
from app.api import deps

router = APIRouter()


@router.get("/", response_model=List[models.LicenseRestriction])
def read_restrictions(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve license restrictions.
    """
    all_license_restrictions = crud.license_restriction.get_multi(db, skip=skip, limit=limit, filter={'approved': True})
    return all_license_restrictions


@router.post("/", response_model=models.LicenseRestriction)
def create_restriction(
    *,
    db: Session = Depends(deps.get_db),
    item_in: models.LicenseRestrictionBase,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Create new license restriction.
    """
    new_license_restriction = crud.license_restriction.create(db=db, obj_in=item_in)
    return new_license_restriction


@router.put("/{id}", response_model=models.LicenseRestrictionBase)
def update_restriction(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    item_in: models.LicenseRestrictionBase,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Update a license restriction.
    """
    license_restriction = crud.license_restriction.get(db=db, id=id)
    if not license_restriction:
        raise HTTPException(status_code=404, detail="License Restriction not found")
    if not crud.user.is_superuser(current_user):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    updated_license_restriction = crud.license_restriction.update(db=db, db_obj=license_restriction, obj_in=item_in)
    return updated_license_restriction


@router.delete("/{id}", response_model=models.LicenseRestriction)
def delete_restriction(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Delete a license restriction.
    """
    license_restriction = crud.license_restriction.get(db=db, id=id)
    if not license_restriction:
        raise HTTPException(status_code=404, detail="License Restriction not found")
    if not crud.user.is_superuser(current_user):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    deleted_license_restriction = crud.license_restriction.remove(db=db, id=id)
    return deleted_license_restriction
