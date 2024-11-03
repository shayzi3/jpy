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
          self.__where_values = ('none-kwargs-where',)
          
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
          
     @staticmethod
     def __list_or_dict(obj: Iterable) -> list[dict[str, Any]]:
          if isinstance(obj, dict):
               return list(obj.values())
          return obj
          
               
     def where(self, **kwargs: dict[str, Any]) -> Self:
          # Обозначения в self.__where_values
          # пустой tuple - таблица free или в значении ключа data пусто
          # пустой list - данные, которые искал пользователь не нашлись
          if self.__free:
               return self
          
          data = self.__json_obj[self.__tablename]['data']
          if not data:
               self.__where_values = ('empty',)
               return self

          if not kwargs:
               self.__where_values = self.__list_or_dict(data)
               return self

          self.__validate(kwargs)
          if isinstance(data, dict):
               if self.__primary in kwargs.keys():
                    if isinstance(kwargs[self.__primary], int):
                         kwargs[self.__primary] = str(kwargs[self.__primary])
                         
                    data = {self.__primary: data.get(kwargs[self.__primary])}
                    if data[self.__primary] is None:
                         self.__where_values = []
                         return self
                    del kwargs[self.__primary]
                    
               if kwargs:
                    sorting = []
                    for key, value in data.items():
                         count = 0
                         for kw_key in kwargs.keys():
                              if value[kw_key] == kwargs[kw_key]:
                                   count += 1
                         
                         if count == len(kwargs):
                              sorting.append(data[key])
                    data = sorting

               if isinstance(data, dict):
                    self.__where_values = [i for i in data.values()]  
               else:
                    self.__where_values = data
               return self
          
          elif isinstance(data, list):
               sorting = []
               for dicts in data:
                    count = 0
                    for kw_key in kwargs.keys():
                         if dicts[kw_key] == kwargs[kw_key]:
                              count += 1
                    
                    if count == len(kwargs):
                         sorting.append(dicts)
                         
               self.__where_values = sorting
               return self

          
     def values(self, *args: str) -> ClassType | list[ClassType]:
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
          
          if 'empty' in self.__where_values:
               return None
          
          if 'none-kwargs-where' in self.__where_values:
               get = self.__json_obj[self.__tablename]['data']
               self.__where_values = self.__list_or_dict(get)

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