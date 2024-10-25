

from typing import Any, Self
from jpy.utils import valide_input_data, BaseClass, Mode



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
          
          self.__where_values = {}
          
               
     def where(self, **kwargs) -> Self:
          if not kwargs or self._free:
               return self
          
          self.__where_values = {...}
          return self
     
     
     
     def values(self, value_list: list[str]) -> list[dict[str, Any]]:
          valide_input_data(
               data=value_list,
               json_file=self._json_obj,
               table_name=self._table,
               free=self._free,
               primary=self._primary,
               mode=Mode.SELECT
          )
          if self._free:
               data = {}
               if not value_list:
                    res = self._json_obj[self._table]
                    
                    for key in res.keys():
                         if key not in ['__types', 'data']:
                              data[key] = res[key]
               else:
                    for j in value_list:
                         data.update({j: self._json_obj[self._table][j]})
               return data
               
               
          if not value_list:
               if not self.__where_values:
                    return [dicts for _, dicts in self._json_obj[self._table]['data'].items()]
                    
               else:
                    return [dicts for _, dicts in self.__where_values.items()]
          
          iterable = self._json_obj[self._table]['data']
          if self.__where_values:
               iterable = self.__where_values
               
          result = []
          for _, value in iterable.items():
               starter = {}
               for key in value_list:
                    starter.update({key: value.get(key)})
               result.append(starter)
          return result
          
         