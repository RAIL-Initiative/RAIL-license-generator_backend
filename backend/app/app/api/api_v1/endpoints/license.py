import io
import os
import tempfile
from typing import Any, List, Union

from fastapi import APIRouter, Depends, HTTPException, Query, Request
from fastapi.responses import FileResponse
import pypandoc
from sqlalchemy.orm import Session
from sqlmodel import select

from app import crud, models
from app.api import deps
from app.utils import generate_license_text
import uuid as uuid_pkg
from fastapi.templating import Jinja2Templates
from pathlib import Path
from starlette.background import BackgroundTask

router = APIRouter()

templates = Jinja2Templates(directory="app/templates")

BASE_DIR = Path(__file__).resolve().parent


@router.get("/", response_model=List[models.LicenseRead])
def read_licenses(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve licenses.
    """
    all_licenses = crud.license.get_multi(db, skip=skip, limit=limit)
    return all_licenses

@router.get("/{id}/generate")
async def generate_license(
    request: Request,
    db: Session = Depends(deps.get_db),
    *,
    id: uuid_pkg.UUID,
    file_type: str = Query("file_type", enum=["txt", "pdf"]),
) -> Any:
    """
    Generate license text for license with id "id".
    """
    license = crud.license.get(db, id=id)

    # we use the python approach even though it is less efficient for clarity
    domain_restrictions = { 
        domain.name : 
        [
            restriction.text for restriction in  domain.restrictions
        ]
        for domain in license.specifiedDomains
    }

    for additional_restriction in license.additionalRestrictions:
        # put additional restriction in correct domain
        # create if not exists
        if additional_restriction.domain.name not in domain_restrictions:
            domain_restrictions[additional_restriction.domain.name] = []
        # append restriction
        domain_restrictions[additional_restriction.domain.name].append(additional_restriction.text)

    if license.license == "ResearchRAIL":
        template_file = "ResearchUseRail.jinja"
    elif license.license == "OpenRAIL":
        template_file = "OpenRAIL-AMS.jinja"
    elif license.license == "RAIL":
        template_file = "RAIL-AMS.jinja"
    else:
        raise ValueError("Unknown license type")
    
    print(license.artifact)
    
    templated_response = templates.TemplateResponse(name=template_file, context={
        "request": request,
        "ARTIFACT": license.artifact,
        "RESTRICTIONS":  domain_restrictions
        }
    )

    if file_type == "txt":
        return pypandoc.convert_text(templated_response.body, format='markdown+fancy_lists', to='plain+fancy_lists')
    if file_type == "pdf":
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as output_file:
            pypandoc.convert_text(templated_response.body, format='markdown+fancy_lists', outputfile=output_file.name, to='pdf')
            def cleanup():
                os.remove(output_file.name)
            return FileResponse(output_file.name, media_type="application/pdf", filename="license.pdf", background=BackgroundTask(cleanup))
            

@router.post("/", response_model=models.LicenseRead)
def create_license(
    *,
    db: Session = Depends(deps.get_db),
    license_in: models.LicenseCreate,
) -> Any:
    """
    Create new license .
    """
    # get all domains with license_in.specifiedDomains
    specified_domains = [crud.license_domain.get(db=db, id=domain_id) for domain_id in license_in.specifiedDomain_ids]
    # get all restrictions with license_in.additionalRestrictions
    additional_restrictions = [crud.license_restriction.get(db=db, id=restriction_id) for restriction_id in license_in.additionalRestriction_ids]
    # filter Nones
    specified_domains = [domain for domain in specified_domains if domain]
    additional_restrictions = [restriction for restriction in additional_restrictions if restriction]
    new_license = crud.license.create(db=db, obj_in=license_in)
    new_license.specifiedDomains = specified_domains
    new_license.additionalRestrictions = additional_restrictions
    db.add(new_license)
    db.commit()

    return new_license


@router.put("/{id}", response_model=models.LicenseRead)
def update_license(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    license_in: models.LicenseCreate,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Update an license.
    """
    license_ = crud.license_.get(db=db, id=id)
    if not license_:
        raise HTTPException(status_code=404, detail="License  not found")
    if not crud.user.is_superuser(current_user):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    updated_license = crud.license.update(db=db, db_obj=license_, obj_in=license_in)
    return updated_license


@router.delete("/{id}", response_model=models.LicenseRead)
def delete_license(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Delete an license.
    """
    license_ = crud.license_.get(db=db, id=id)
    if not license_:
        raise HTTPException(status_code=404, detail="License  not found")
    if not crud.user.is_superuser(current_user):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    deleted_license = crud.license.remove(db=db, id=id)
    return deleted_license
