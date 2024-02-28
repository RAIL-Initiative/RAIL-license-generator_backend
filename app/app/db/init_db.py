from sqlalchemy.orm import Session

from app import crud, models
from app.core.config import settings

import json

# make sure all SQL Alchemy models are imported (app.db.base) before initializing DB
# otherwise, SQL Alchemy might fail to initialize relationships properly
# for more details: https://github.com/tiangolo/full-stack-fastapi-postgresql/issues/28


def init_db(db: Session) -> None:
    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create
    # the tables un-commenting the next line
    # Base.metadata.create_all(bind=engine)

    user = crud.user.get_by_email(db, email=settings.FIRST_SUPERUSER)
    if not user:
        user_in = models.UserCreate(
            full_name="Admin",
            email=settings.FIRST_SUPERUSER,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            is_superuser=True,
        )
        user = crud.user.create(db, obj_in=user_in)  # noqa: F841
    
    # read initial data from json file
    with open('app/data/initial_data.json') as f:
        data = json.load(f)
    
    for source in set(data['Source'].values()):
        crud.license_source.create(db, obj_in=models.LicenseSourceBase(name=source, approved=True))

    for domain in set(data['Domain'].values()):
        crud.license_domain.create(db, obj_in=models.LicenseDomainBase(name=domain))

    # flush so we can oberserve changes in the database
    db.flush()

    for i, restriction in data['Restriction'].items():
        source_id = crud.license_source.get_by_name(db, name=data['Source'][str(i)]).id
        domain_id = crud.license_domain.get_by_name(db, name=data['Domain'][str(i)]).id
        crud.license_restriction.create(db, obj_in=models.LicenseRestriction(
            text=restriction,
            approved=True,
            source_id=source_id,
            domain_id=domain_id
        ))

