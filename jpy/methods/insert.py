

import json
import os

from jpy.utils import valide_input_data, Mode
from typing import Any



class Insert:
     __slots__ = (
          "_table",
          "_json_obj",
          "_free",
          "_path",
          "_primary"
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
          

     
     def __save(self) -> None:
          if not os.path.exists(self._path):
               raise FileNotFoundError(f"{self._path} not exists")
          
          with open(self._path, 'w') as file:
               json.dump(self._json_obj, file, indent=4)

     
     def values(self, **kwargs) -> None:
          valide_input_data(
               data=kwargs,
               json_file=self._json_obj,
               table_name=self._table,
               free=self._free,
               primary=self._primary,
               mode=Mode.INSERT
          )
          if not self._free:
               if self._primary:
                    self._json_obj[self._table]['data'].update(
                         {
                              kwargs[self._primary]: {
                                   key: value for key, value in kwargs.items()
                              }
                         }
                    )
               else:
                    self._json_obj[self._table]['data'].append(
                         {
                              key: value for key, value in kwargs.items()
                         }
                    )
          else:
               for key, value in kwargs.items():
                    self._json_obj[self._table][key] = value
          return self.__save()   