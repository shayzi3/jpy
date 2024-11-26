import json
import os


from typing_extensions import TypeVar, Generic
from orm_json.utils import (
     _valide_input_data, 
     _save,
     Mode, 
     MetaData
)
from orm_json.utils.exception import (
     FileNotFound,
     NotFoundMetadata
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
               raise NotFoundMetadata(f"Metadata about class {table.__class__.__name__} not found.")
          
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
                    primary = kwargs[self.__primary]
                    if isinstance(primary, int):
                         primary = str(primary)
                         
                    self.__json_obj[self.__tablename]['data'].update({
                         primary: {key: value for key, value in kwargs.items()}
                    })
               else:
                    self.__json_obj[self.__tablename]['data'].append({
                              key: value for key, value in kwargs.items()
                         }
                    )
          else:
               for key, value in kwargs.items():
                    self.__json_obj[self.__tablename][key] = value
          _save(
               obj=self.__json_obj,
               path=self.__path
          )
          return self.__table(**kwargs)