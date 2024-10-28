

from typing import Any, Self
from jpy.utils import valide_input_data, BaseClass



class Select(BaseClass):
     __slots__ = (
          "_table",
          "_json_obj",
          "_free",
          "_path",
          "_primary",
          "__where_values"
     )
     
     
     def __init__(
          self,
          table: str,
          json_obj: dict[str, Any],
          free: bool,
          path: str,
          primary: str
     ) -> None:
          
          self._table = table
          self._json_obj = json_obj
          self._free = free
          self._path = path
          self._primary = primary
          self.__where_values = ()
          
          if isinstance(self._primary, int):
               self._primary = str(self._primary)
          
          
     def validate(self, obj: dict[str, Any]) -> None:
          valide_input_data(
               data=obj,
               json_file=self._json_obj,
               table_name=self._table,
               free=self._free,
               primary=self._primary
          )
          
               
     def where(self, **kwargs: dict[str, Any]) -> Self:
          # Обозначения в self.__where_values
          # пустой tuple - таблица free или в значении ключа data пусто
          # пустой list - данные, которые искал пользователь не нашлись
          if self._free:
               return self
          
          data = self._json_obj[self._table]['data']
          if not data:
               return self

          if not kwargs:
               if isinstance(data, dict):
                    self.__where_values = [i for i in data.values()]
               
               elif isinstance(data, list):
                    self.__where_values = [i for i in data]
               return self

          self.validate(kwargs)
          if isinstance(data, dict):
               if self._primary in kwargs.keys():
                    if isinstance(kwargs[self._primary], int):
                         kwargs[self._primary] = str(kwargs[self._primary])
                         
                    data = {self._primary: data.get(kwargs[self._primary])}
                    if data[self._primary] is None:
                         self.__where_values = []
                         return self
                    
                    del kwargs[self._primary]
                    
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

          
     def values(
          self, 
          value_list: list[str] | tuple[str]
     ) -> list[dict[str, Any]] | dict[str, Any] | None:
          self.validate(value_list)
          if self._free:
               result = {}
               if not value_list:
                    res = self._json_obj[self._table]
                    
                    for key in res.keys():
                         if key not in ['__types', 'data']:
                              result[key] = res[key]
               else:
                    for free_key in value_list:
                         result.update({free_key: self._json_obj[self._table][free_key]})
               return result
          
          if not self.__where_values:
               return None
          
          result = self.__where_values
          if value_list:
               result = []
               for data in self.__where_values:
                    beetween = {}
                    for key in value_list:
                         beetween[key] = data[key]
                    result.append(beetween)      
                      
          if len(result) == 1:
               return result[0]
          return result
         