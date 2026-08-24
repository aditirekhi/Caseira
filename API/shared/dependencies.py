from typing import Annotated
from fastapi import Depends

from shared.constants import ConstantsClass


def get_constants_dependency():
    return ConstantsClass()

ConstantsDependency=Annotated[ConstantsClass,Depends(get_constants_dependency)]