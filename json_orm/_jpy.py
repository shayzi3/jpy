import json


from typing_extensions import Any, TypeVar
from json_orm.utils import MetaOrm
from json_orm.methods.insert import Insert



__all__ = (
     "Column",
     "JsonOrm",
     "DataArgs"
)

T = TypeVar("T")


class Column:
     pass



class DataArgs:
     tablename: str | None
     primary: str | None
     path: str
     free: bool
     
     
          
class JsonOrm(metaclass=MetaOrm):
     def __init__(self, **kwargs) -> None:
          if kwargs:
               columns: list[str] = self.metadata.get('columns')
               if columns:  
                    for kw_key, value in kwargs.items():
                         if kw_key in columns:
                              self.__dict__[kw_key] = value
                              
                              
     @classmethod
     def create_tables(cls, *args: type) -> None:
          if args:
               iterable = [dict_.__dict__ for dict_ in args]
          else:
               iterable = cls.__metadata__
               
          pathes = {key.get('metadata').get('path'): {} for key in iterable}
          for data in iterable:
               meta = data.get('metadata')                    
               
               tablename = meta.get('tablename')
               if meta.get('tablename') not in pathes[meta.get('path')]:
                    # Create with tablename
                    if meta.get('free') is True:
                         pathes[meta.get('path')].update({
                                   tablename: {key: None for key in meta.get('columns')}
                              }  
                         )
                    else:
                         pathes[meta.get('path')].update({
                              tablename: {
                                   'columns': meta.get('columns'),
                                   'data': [] if not meta.get('primary') else {}
                                   }
                              }
                         )
               else: 
                    # Create without tablename
                    if meta.get('free') is True:
                         pathes[meta.get('path')][tablename].update(
                              {key: None for key in meta.get('columns')}
                         )
                         
                    else:
                         pathes[meta.get('path')][tablename].update({
                              'columns': meta.get('columns'),
                              'data': [] if not meta.get('primary') else {}
                              }
                         )
          for key, value in pathes.items():
               with open(key, 'w', encoding='utf-8') as file:
                    json.dump(value, file, indent=4)
     
     
     def __len__(self) -> int:
          ...
          
          
     @classmethod
     def __add__(cls: T, obj: dict[str, Any]) -> T:
          return Insert(cls).values(**obj)
          
         
     def __repr__(self) -> str:
          meta = getattr(self, 'metadata')
          name = self.__class__.__name__

          if meta:
               string = ''
               for key in meta.get('columns'):
                    if key != getattr(self, key):
                         string += f'{key}={getattr(self, key)} '
                    
               return f'{name}({string.strip()})'
          return f'{name}()'

          
          