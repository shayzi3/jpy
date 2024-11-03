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
     Mode
)
from json_orm.utils.exception import (
     NotFoundMetadata,
     FileNotFound
)



__all__ = (
     "Update",
)
ClassType = TypeVar("ClassType")



class Update(BaseClass, Generic[ClassType]):
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
               
               
     def __save(self) -> None:
          with open(self.__path, 'w', encoding='utf-8') as file:
               json.dump(self.__json_obj, file, indent=4)
          
          
     def __validate(self, obj: Iterable) -> None:
          _valide_input_data(
               data=obj,
               json_file=self.__json_obj,
               table_name=self.__tablename,
               free=self.__free,
               primary=self.__primary,
               columns=self.__columns,
               mode=Mode.UPDATE
          )
          
     @staticmethod
     def __list_or_dict(obj: Iterable) -> list[dict[str, Any]]:
          if isinstance(obj, dict):
               return list(obj.values())
          return obj
               
               
     def where(self, **kwargs) -> Self:
          if self.__free:
               return self
          
          data = self.__json_obj[self.__tablename]['data']
          if not data:
               self.__where_values.append('empty')
               return self
          
          if not kwargs:
               self.__where_values = self.__list_or_dict(data)
               return self
          self.__validate(kwargs)
          
          
          result: list[dict[str, Any]] = []
          if isinstance(data, dict):
               if self.__primary in kwargs.keys():
                    primary = kwargs[self.__primary]
                    if isinstance(primary, int):
                         primary = str(primary)
                         
                    if not data.get(primary):
                         return self
                    result.append({primary: data.get(primary)})
                    del kwargs[self.__primary]
                    
               if kwargs:
                    if result:
                         for _, value in result[0].items():
                              for kw_key in kwargs.keys():
                                   if value[kw_key] != kwargs[kw_key]:
                                        del result[0]
                    else:
                         data = list(data.values())
                    
          if isinstance(data, list):
               for index in range(len(data)):
                    count = 0
                    for kw_key in kwargs.keys():
                         if data[index][kw_key] == kwargs[kw_key]:
                              count += 1
                    
                    if count == len(kwargs):
                         result.append({index: data[index]})           
          self.__where_values = result
          return self
          
          
     
     def values(self, **kwargs: dict[str, Any]) -> ClassType:
          self.__validate(kwargs)
          if self.__free:
               ...
                  
          if not self.__where_values:
               return None
          
          for dicts in self.__where_values:
               for key, value in dicts.items():
                    for kw_key in kwargs.keys():
                         value[kw_key] = kwargs[kw_key]
               
               if self.__primary in value:
                    key = value[self.__primary]
               self.__json_obj[self.__tablename]['data'][key] = value
                    
          self.__save()
          return self.__table(**kwargs)
                         
                    
                    
     