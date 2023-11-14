from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models
from app.api import deps

router = APIRouter()


@router.get("/", response_model=List[models.LicenseRead])
def read_items(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve licenses.
    """
    all_license_s = crud.license.get_multi(db, skip=skip, limit=limit)
    return all_license_s


@router.post("/", response_model=models.LicenseRead)
def create_item(
    *,
    db: Session = Depends(deps.get_db),
    item_in: models.LicenseCreate,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Create new license .
    """
    # get all domains with item_in.specifiedDomains
    specified_domains = [crud.license_domain.get(db=db, id=domain_id) for domain_id in item_in.specifiedDomain_ids]
    # get all restrictions with item_in.additionalRestrictions
    additional_restrictions = [crud.license_restriction.get(db=db, id=restriction_id) for restriction_id in item_in.additionalRestriction_ids]

    new_license = crud.license.create(db=db, obj_in=item_in)

    for domain in specified_domains:
        new_license.specifiedDomains.append(domain)
    for restriction in additional_restrictions:
        new_license.additionalRestrictions.append(restriction)
    db.add(new_license)
    db.commit()
    print(new_license.specifiedDomains)
    print(new_license.additionalRestrictions)

    return new_license


@router.put("/{id}", response_model=models.LicenseRead)
def update_item(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    item_in: models.LicenseCreate,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Update an item.
    """
    license_ = crud.license_.get(db=db, id=id)
    if not license_:
        raise HTTPException(status_code=404, detail="License  not found")
    if not crud.user.is_superuser(current_user):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    updated_license = crud.license.update(db=db, db_obj=license_, obj_in=item_in)
    return updated_license


@router.delete("/{id}", response_model=models.LicenseRead)
def delete_item(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Delete an item.
    """
    license_ = crud.license_.get(db=db, id=id)
    if not license_:
        raise HTTPException(status_code=404, detail="License  not found")
    if not crud.user.is_superuser(current_user):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    deleted_license = crud.license.remove(db=db, id=id)
    return deleted_license
