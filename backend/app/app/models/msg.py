from typing import TYPE_CHECKING, Optional

from sqlmodel import SQLModel

class Msg(SQLModel):
    msg: str