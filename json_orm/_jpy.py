import json


from typing import Any
from json_orm.utils import MetaOrm



__all__ = (
     "Column",
     "JsonOrm",
     "DataArgs"
)



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
               
               pathes[meta.get('path')].update({
                    meta.get('tablename'): {
                         'columns': meta.get('columns'),
                         'data': [] if not meta.get('primary') else {}
                         }
                    }
               )
          for key, value in pathes.items():
               with open(key, 'w', encoding='utf-8') as file:
                    json.dump(value, file, indent=4)
     
     
     @classmethod
     def __len__(cls) -> int:
          ...
          
       
     @classmethod   
     def __add__(
          cls, 
          obj: dict[str, Any]
     ) -> ...:
          
         ...
          
         
     @classmethod 
     def __repr__(cls) -> str:
          return f'cls <{cls.__name__}>'
          
          