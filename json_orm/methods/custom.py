
from typing import Callable
from typing_extensions import TypeVar
from functools import wraps

from json_orm.utils.exception import (
     NotFoundMetadata,
     TableColumnNotExists,
     ReturnError
)


__all__ = (
     "custom_option",
)
T = TypeVar("T")


def custom_option(model: T) -> Callable[[], dict]:
     def decorator(func: Callable) -> Callable[[], dict]:
          
          @wraps(func)
          def wrapper() -> dict:
               nonlocal model
               
               if func.__annotations__.get('return'):
                    if not issubclass(func.__annotations__.get('return'), bool):
                         raise ReturnError(f"Function {func.__name__} must return bool type")
               
               metadata = model.__dict__.get('metadata')
               if not metadata:
                    raise NotFoundMetadata(f"Metadata for class {model.__class__.__name__} not found.")
               
               if metadata.get('free') is True:
                    return {}
               
               for key in func.__code__.co_varnames:
                    if key not in metadata.get('columns'):
                         raise TableColumnNotExists(f"Column {key} for table {metadata.get('tablename')} not exists.")
               return {
                    'args': func.__code__.co_varnames,
                    'model': model,
                    'function': func
               }
          return wrapper
     return decorator