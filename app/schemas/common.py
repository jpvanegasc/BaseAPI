import inspect
from typing import List

from pydantic import BaseModel


class PagedResponse(BaseModel):
    items: List[BaseModel]
    total: int


def optional(*fields):
    """
    Decorator function used to modify a pydantic model's fields to all be optional.
    Alternatively, you can  also pass the field names that should be made optional
    as arguments to the decorator.
    Taken from
        https://github.com/samuelcolvin/pydantic/issues/1223#issuecomment-775363074
    """

    def wrapper(_cls):
        for field in fields:
            _cls.__fields__[field].required = False

        dict_origin = _cls.dict

        def dict_excludes(*args, exclude_unset: bool = None, **kwargs):
            exclude_unset = True
            return dict_origin(*args, **kwargs, exclude_unset=exclude_unset)

        _cls.dict = dict_excludes

        return _cls

    if fields and inspect.isclass(fields[0]) and issubclass(fields[0], BaseModel):
        cls = fields[0]
        fields = cls.__fields__
        return wrapper(cls)

    return wrapper
