
from typing_extensions import Callable, Any
from functools import wraps

from orm_json.utils.exception import (
     NotFoundMetadata,
     TableColumnNotExists,
     ReturnError
)



def custom_option(model: type, return_success_type: Any = True) -> Callable[[], dict]:
     def decorator(func: Callable) -> Callable[[], dict]:
          
          @wraps(func)
          def wrapper() -> dict:
               nonlocal model, return_success_type
               
               metadata = model.__dict__.get('metadata')
               if not metadata:
                    raise NotFoundMetadata(f"Metadata for class {model.__class__.__name__} not found.")
               
               if metadata.get('free') is True:
                    return {}
               
               for key in func.__code__.co_varnames:
                    if key not in metadata.get('columns'):
                         raise TableColumnNotExists(f"Column {key} for table {metadata.get('tablename')} not exists.")
               return {
                    metadata.get('tablename'): {
                         'args': func.__code__.co_varnames,
                         'function': func,
                         'return_type': return_success_type
                    }
               }
          return wrapper
     return decorator