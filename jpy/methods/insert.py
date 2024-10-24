

import json
import os

from jpy.utils import valide_input_data
from typing import Any




class Insert:
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
          

     
     def __save(self, data: dict[str, Any]) -> bool:
          if not os.path.exists(self._path):
               raise FileNotFoundError(f"{self._path} not exists")
          
          with open(self._path, 'w') as file:
               json.dump(data, file, indent=4)
          return True
            
     
     def values(self, **kwargs) -> bool:
          valide_input_data(
               data=kwargs,
               json_file=self._json_obj,
               table_name=self._table,
               free=self._free,
               primary=self._primary
          )
          if not self._free:
               self._json_obj[self._table]['data'].update(
                    {
                         kwargs[self._primary]: {
                              key: value for key, value in kwargs.items()
                         }
                    }
               )
               
          else:
               for key, value in kwargs.items():
                    self._json_obj[self._table][key] = value
          return self.__save(self._json_obj)
          