import logging

from sqlmodel import SQLModel
from app.models import User

from app.db.init_db import init_db
from app.db.session import Session, engine

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def init() -> None:
    with Session() as db:
        init_db(db)



def main() -> None:
    logger.info("Creating initial data")
    try:
        with Session() as db:
            # check if atleast one user exists
            if not db.query(User).first():
                init()
    except Exception as e:
        logger.error(e)
    logger.info("Initial data created")


if __name__ == "__main__":
    main()
