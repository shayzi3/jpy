import json
import os


from typing_extensions import (
     Self, 
     Generic, 
     TypeVar,
     Iterable,
     Any
)
from json_orm.utils import (
     _valide_input_data, 
     _list_or_dict,
     BaseClass, 
     MetaData
)
from json_orm.utils.exception import (
     NotFoundMetadata, 
     FileNotFound
)


__all__ = (
     "Select",
)
ClassType = TypeVar("ClassType")



class Select(BaseClass, Generic[ClassType]):
     __slots__ = (
          "__table",
          "__free",
          "__path",
          "__primary",
          "__where_values",
          "__tablename",
          "__json_obj",
          "__columns",
     )
     
     
     def __init__(self, table: ClassType) -> None:
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
          self.__where_values = []
          
          if isinstance(self.__primary, int):
               self.__primary = str(self._primary)
               
          if not os.path.exists(self.__path):
               raise FileNotFound(f"Json file {self.__path} not exists")
          
          with open(self.__path, 'r', encoding='utf-8') as file:
               self.__json_obj = json.loads(file.read())
               
          
     def __validate(self, obj: Iterable) -> None:
          _valide_input_data(
               data=obj,
               json_file=self.__json_obj,
               table_name=self.__tablename,
               free=self.__free,
               columns=self.__columns,
               primary=self.__primary
          )
               
     def where(self, **kwargs: dict[str, Any]) -> Self:
          # Обозначения в self.__where_values
          # пустой tuple - таблица free или в значении ключа data пусто
          # пустой list - данные, которые искал пользователь не нашлись
          if self.__free:
               return self
          
          data = self.__json_obj[self.__tablename]['data']
          if not data:
               return self

          if not kwargs:
               self.__where_values = _list_or_dict(data)
               return self

          self.__validate(kwargs)
          result = []
          if isinstance(data, dict):
               if self.__primary in kwargs.keys():
                    primary = kwargs[self.__primary]
                    if isinstance(primary, int):
                         primary = str(primary)
                         
                    if not data.get(primary):
                         return self
                    result.append(data.get(primary))
                    del kwargs[self.__primary]
                    
               if kwargs:
                    if result:
                         for value in result:
                              for kw_key in kwargs.keys():
                                   if value[kw_key] != kwargs[kw_key]:
                                        del result[0]
                    else:
                         data = list(data.values())
          
          if isinstance(data, list):
               for dicts in data:
                    count = 0
                    for kw_key in kwargs.keys():
                         if dicts[kw_key] == kwargs[kw_key]:
                              count += 1
                    
                    if count == len(kwargs):
                         result.append(dicts)
                         
          self.__where_values = result
          return self

          
     def values(self, *args: str) -> ClassType | list[ClassType] | None:
          self.__validate(args)
          if self.__free:
               result = {}
               if not args:
                    res = self.__json_obj[self.__tablename]
                    
                    for key in res.keys():
                         if key not in ['columns', 'data']:
                              result[key] = res[key]
               else:
                    for free_key in args:
                         result.update({free_key: self.__json_obj[self.__tablename][free_key]})
               return self.__table(**result)
          
          if not self.__where_values:
               return None

          result = self.__where_values
          if args:
               result = []
               for data in self.__where_values:
                    beetween = {}
                    for key in args:
                         beetween[key] = data[key]
                    result.append(beetween)   

          if len(result) == 1:
               return self.__table(**result[0])
          return [self.__table(**value) for value in result]