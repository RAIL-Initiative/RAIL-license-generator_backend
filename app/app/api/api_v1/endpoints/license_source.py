from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models
from app.api import deps

router = APIRouter()


@router.get("/", response_model=List[models.LicenseSource])
def read_sources(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve license sources.
    """
    all_license_sources = crud.license_source.get_multi(db, skip=skip, limit=limit)
    return all_license_sources


@router.post("/", response_model=models.LicenseSource)
def create_source(
    *,
    db: Session = Depends(deps.get_db),
    item_in: models.LicenseSourceBase,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Create new license source.
    """
    new_license_source = crud.license_source.create(db=db, obj_in=item_in)
    return new_license_source


@router.put("/{id}", response_model=models.LicenseSourceBase)
def update_source(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    item_in: models.LicenseSourceBase,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Update a license source.
    """
    license_source = crud.license_source.get(db=db, id=id)
    if not license_source:
        raise HTTPException(status_code=404, detail="License Source not found")
    if not crud.user.is_superuser(current_user):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    updated_license_source = crud.license_source.update(db=db, db_obj=license_source, obj_in=item_in)
    return updated_license_source


@router.delete("/{id}", response_model=models.LicenseSource)
def delete_source(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Delete a license source.
    """
    license_source = crud.license_source.get(db=db, id=id)
    if not license_source:
        raise HTTPException(status_code=404, detail="License Source not found")
    if not crud.user.is_superuser(current_user):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    deleted_license_source = crud.license_source.remove(db=db, id=id)
    return deleted_license_source
