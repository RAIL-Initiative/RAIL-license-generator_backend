from .user import *  # noqa
from .license import *  # noqa
from .license_domain import *  # noqa
from .license_restriction import *  # noqa
from .license_source import *  # noqa
from .link_tables import *  # noqa
from .token import *  # noqa
from .msg import *  # noqa

def get_subclasses(cls):
    for subclass in cls.__subclasses__():
        yield from get_subclasses(subclass)
        yield subclass

models_dict = {cls.__name__: cls for cls in get_subclasses(SQLModel)}   

for cls in models_dict.values():
    cls.update_forward_refs(**models_dict)
