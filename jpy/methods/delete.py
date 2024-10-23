from __future__ import annotations


import json
from typing import Any
from .where_value import WhereValues



class Delete(WhereValues):
     def __init__(
          self,
          table: str,
          path: str,
          **kwargs
     ) -> None:
          
          self.__table = table
          self.__path = path
          self.__kwargs = kwargs
          
          with open(self.__path, 'r') as file:
               self.__json = json.loads(file.read())
               
               
     
               