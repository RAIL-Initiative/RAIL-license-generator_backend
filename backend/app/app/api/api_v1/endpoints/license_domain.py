from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models
from app.api import deps

router = APIRouter()


@router.get("/", response_model=List[models.LicenseDomain])
def read_domains(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve license domains.
    """
    all_license_domains = crud.license_domain.get_multi(db, skip=skip, limit=limit)
    return all_license_domains


@router.post("/", response_model=models.LicenseDomain)
def create_domain(
    *,
    db: Session = Depends(deps.get_db),
    item_in: models.LicenseDomainBase,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Create new license domain.
    """
    new_license_domain = crud.license_domain.create(db=db, obj_in=item_in)
    return new_license_domain


@router.put("/{id}", response_model=models.LicenseDomainBase)
def update_domain(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    item_in: models.LicenseDomainBase,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Update an item.
    """
    license_domain = crud.license_domain.get(db=db, id=id)
    if not license_domain:
        raise HTTPException(status_code=404, detail="License Domain not found")
    if not crud.user.is_superuser(current_user):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    updated_license_domain = crud.license_domain.update(db=db, db_obj=license_domain, obj_in=item_in)
    return updated_license_domain


@router.delete("/{id}", response_model=models.LicenseDomain)
def delete_domain(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Delete an item.
    """
    license_domain = crud.license_domain.get(db=db, id=id)
    if not license_domain:
        raise HTTPException(status_code=404, detail="License Domain not found")
    if not crud.user.is_superuser(current_user):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    deleted_license_domain = crud.license_domain.remove(db=db, id=id)
    return deleted_license_domain
