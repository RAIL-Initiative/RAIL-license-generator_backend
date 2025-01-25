from enum import Enum
import os
import tempfile
from typing import Any, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import FileResponse, StreamingResponse
from jinja2 import Template
import pypandoc
from sqlalchemy.orm import Session
import uuid as uuid_pkg
from pathlib import Path
from starlette.background import BackgroundTask
from pathvalidate import validate_filename, ValidationError

from dulwich.repo import Repo
from dulwich.object_store import tree_lookup_path

from app import crud, models
from app.api import deps
from app.core.rate_limiting import limiter



router = APIRouter()
repo = Repo.discover()

BASE_DIR = Path(__file__).resolve().parent

class MediaType(str, Enum):
    plain = "text/plain"
    latex = "text/latex"
    markdown = "text/markdown"
    rtf = "text/rtf"



@router.get("/", response_model=List[models.LicenseRead])
def read_licenses(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Retrieve licenses.
    """
    all_licenses = crud.license.get_multi(db, skip=skip, limit=limit)
    return all_licenses

@router.get("/{id}/generate")
@limiter.limit("5/minute")
async def generate_license(
    request: Request,
    db: Session = Depends(deps.get_db),
    *,
    id: uuid_pkg.UUID,
    media_type: MediaType = "text/markdown",
    git_sha: Optional[str] = None
) -> Any:
    """
    Generate license text for license with id "id".
    In order to select a specific version of the license, you can provide a git_sha or 'head' to get the latest version locally.
    """
    license = crud.license.get(db, id=id)

    restrictions = {}
    for restriction in license.restrictions:
        # put additional restriction in correct domain
        # create if not exists
        if restriction.domain.name not in restrictions:
            restrictions[restriction.domain.name] = []
        # append restriction
        restrictions[restriction.domain.name].append(restriction.text)
    
     # deduplicate restrictions
    for domain in restrictions:
        # create index for each restriction with letters
        restrictions[domain] = [[chr(97 + index), restriction] for index, restriction in enumerate(restrictions[domain])]

    # construct array of licensed artifacts
    artifacts = []
    if license.application:
        artifacts.append("Application")
    if license.model:
        artifacts.append("Model")
    if license.sourcecode:
        artifacts.append("Source Code")

    short_artifact_name = "".join([artifact[0] for artifact in artifacts])

    if license.license == "ResearchRAIL":
        template_file = "ResearchUseRAIL.jinja"
    elif license.license == "OpenRAIL":
        template_file = "OpenRAIL-AMS.jinja"
    elif license.license == "RAIL":
        template_file = "RAIL-AMS.jinja"
    else:
        raise ValueError("Unknown license type")
    
    if git_sha != "head":
        git_sha = git_sha or license.git_commit_hash
        commit = repo.get_object(git_sha.encode("ascii"))
        # dulwich expects bytes instead of str
        path = bytes("app/app/templates/" + template_file, "utf-8")
        mode, sha = tree_lookup_path(repo.get_object, commit.tree, path)
        file_object_at_creation_time = repo[sha].data.decode("utf-8")
    else:
        with open("/app/app/app/templates/" + template_file, "r") as template_file:
            file_object_at_creation_time =  template_file.read()

    
    template = Template(file_object_at_creation_time)
    rendered_text = template.render(
        request=request,
        ARTIFACTS=artifacts,
        SHORT_ARTIFACT_NAME=short_artifact_name,
        LICENSE_NAME=license.name,
        RESTRICTIONS=restrictions,
        LICENSE_TIMESTAMP=license.timestamp,
        LICENSE_ID=license.id,
        LICENSE_TEMPLATE_VERSION=license.git_commit_hash
    )

    try:
        filename = license.name + "-" + license.license
        # check if filename can be encodable and a proper filename for all platforms
        filename.encode("latin1")
        validate_filename(filename)
    except (UnicodeEncodeError, ValidationError):
        filename = license.license.encode("latin1")
    except Exception as e:
        print(e)
        raise HTTPException(status_code=422, detail="The license name could not be encoded correctly. Please check the license name for special characters and contact the maintainers.")

    if media_type == "text/markdown":
        return StreamingResponse(iter(rendered_text), media_type="application/octet-stream", headers={"Content-Disposition": f"attachment; filename={filename}.md"})
    if media_type == "text/plain":
        return StreamingResponse(iter(pypandoc.convert_text(rendered_text, format='markdown', to='plain')), media_type="application/octet-stream", headers={"Content-Disposition": f"attachment; filename={filename}.txt"})
    if  media_type == "text/rtf":
        return StreamingResponse(iter(pypandoc.convert_text(rendered_text, format='markdown', to='rtf')), media_type="application/octet-stream", headers={"Content-Disposition": f"attachment; filename={filename}.rtf"})
    if media_type == "text/latex":
        return StreamingResponse(iter(pypandoc.convert_text(rendered_text, format='markdown', to='latex')), media_type="application/octet-stream", headers={"Content-Disposition": f"attachment; filename={filename}.latex"})
    if media_type == "application/pdf":
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as output_file:
            pypandoc.convert_text(rendered_text, format='markdown', outputfile=output_file.name, to='pdf')
            def cleanup():
                os.remove(output_file.name)
            return FileResponse(output_file.name, media_type="application/pdf", filename="{filename}.pdf", background=BackgroundTask(cleanup))
            

@router.post("/", response_model=models.LicenseRead)
@limiter.limit("1/minute")
def create_license(
    request: Request,
    *,
    db: Session = Depends(deps.get_db),
    license_in: models.LicenseCreate,
) -> Any:
    """
    Create new license .
    """
    # get all restrictions with license_in.additionalRestrictions
    restrictions = [crud.license_restriction.get(db=db, id=restriction_id) for restriction_id in license_in.restriction_ids]
    if None in restrictions:
        raise HTTPException(status_code=404, detail="One or more restrictions not found. Please check that you have the correct restriction ids.")
    # filter Nones
    new_license = crud.license.create(db=db, obj_in=license_in)
    new_license.restrictions = restrictions
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
