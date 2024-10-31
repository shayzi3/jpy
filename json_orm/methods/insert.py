import json
import os


from typing import Any, TypeVar, Generic
from json_orm.utils import (
     _valide_input_data, 
     Mode, 
     MetaData
)
from json_orm.utils.exception import (
     FileNotFound,
     NotFoundMetadata
)


__all__ = (
     "Insert",
)

ClassType = TypeVar('ClassType')


class Insert(Generic[ClassType]):
     __slots__ = (
          "__tablename",
          "__free",
          "__path",
          "__primary",
          "__columns",
          "__json_obj",
          "__table",
     )
     
     
     def __init__(self, table: ClassType):
          dict_type = table.__dict__.get('metadata')
          if dict_type:
               type_ = MetaData(**dict_type)
          else:
               raise NotFoundMetadata(f"Metadata about class {table.__qualname__} not found.")
          
          self.__table = table
          self.__tablename = type_.tablename
          self.__free = type_.free
          self.__path = type_.path
          self.__primary = type_.primary
          self.__columns = type_.columns
          
          if not os.path.exists(self.__path):
               raise FileNotFound(f"Json file {self.__path} not exists")
          
          with open(self.__path, 'r', encoding='utf-8') as file:
               self.__json_obj = json.loads(file.read())

     
     def __save(self, kwargs: dict[str, Any]) -> ClassType:
          with open(self.__path, 'w') as file:
               json.dump(self.__json_obj, file, indent=4)
          return self.__table(**kwargs)

     
     def values(self, **kwargs) -> ClassType:
          _valide_input_data(
               data=kwargs,
               json_file=self.__json_obj,
               table_name=self.__tablename,
               free=self.__free,
               primary=self.__primary,
               columns=self.__columns,
               mode=Mode.INSERT
          )
          if not self.__free:
               if self.__primary:
                    self.__json_obj[self.__tablename]['data'].update(
                         {
                              kwargs[self.__primary]: {
                                   key: value for key, value in kwargs.items()
                              }
                         }
                    )
               else:
                    self.__json_obj[self.__tablename]['data'].append(
                         {
                              key: value for key, value in kwargs.items()
                         }
                    )
          else:
               for key, value in kwargs.items():
                    self.__json_obj[self.__tablename][key] = value
          return self.__save(kwargs)   