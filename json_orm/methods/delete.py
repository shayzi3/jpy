import json
import os


from typing_extensions import (
     Any,
     Generic,
     TypeVar,
     Self,
     Iterable
)
from json_orm.utils import (
     BaseClass, 
     MetaData,
     _valide_input_data,
     _save,
     _list_or_dict,
     _where_for_update_and_delete
)
from json_orm.utils.exception import (
     NotFoundMetadata,
     FileNotFound
)



__all__ = (
     "Delete",
)
ClassType = TypeVar("ClassType")



class Delete(BaseClass, Generic[ClassType]):
     __slots__ = (
          "__table",
          "__tablename",
          "__free",
          "__path",
          "__primary",
          "__columns",
          "__json_obj",
          "__where_values",
     )
     
     def __init__(self, table: ClassType) -> None:
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
          self.__where_values = []
          
          if not os.path.exists(self.__path):
               raise FileNotFound(f"Json file {self.__path} not exists")
          
          with open(self.__path, 'r', encoding='utf-8') as file:
               self.__json_obj = json.loads(file.read())
               
     def __valide(self, obj: Iterable) -> None:
          _valide_input_data(
               data=obj,
               json_file=self.__json_obj,
               table_name=self.__tablename,
               free=self.__free,
               primary=self.__primary,
               columns=self.__columns,
          )
          
          
     def where(self, **kwargs) -> Self:
          if self.__free:
               return self
          
          data = self.__json_obj[self.__tablename]['data']
          if not data:
               return self
          
          if not kwargs:
               self.__where_values = _list_or_dict(data)
               return self
          
          self.__valide(kwargs)
          self.__where_values = _where_for_update_and_delete(
               self=self,
               kwargs=kwargs,
               primary_key=self.__primary
          )
          return self