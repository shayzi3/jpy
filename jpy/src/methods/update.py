
import json
from typing import Any



class Update:
     def __init__(
          self,
          table: str,
          path: str,
     ) -> None:
          
          self.__table = table
          self.__path = path
          
          with open(self.__path, 'r') as file:
               self.__json = json.loads(file.read())
               
               
     def __save(
          self, 
          data: dict[str, Any]
     ) -> None:
          
          if self.__table != '__free':
               self.__json[self.__table]['data'].append(data)
               
          with open(self.__path, 'w', encoding='utf-8') as file:
               json.dump(self.__json, file, indent=4)
          
     
     def where(self, **kwargs: dict[str, Any]) -> None:
          if self.__table == '__free':
               raise ValueError("Dont use where with __free table")

          for key in kwargs:
               if key not in self.__json[self.__table]['__types']:
                    raise ValueError(f"Not found argument {key}")
               
               
     def values(self, **kwargs: dict[str, Any]) -> None:
          if self.__table == '__free':
               for key, value in kwargs.items():
                    if key not in self.__json['__free']:
                         raise ValueError(f'Key {key} not found in __free table')
                    self.__json['__free'][key] = value
                    
          else:
               # Проверка на то, что все аргументы укзаны
               for key in self.__json[self.__table]['__types']:
                    if key not in kwargs.keys():
                         raise ValueError(f"Not found argument {key} for table {self.__table}")
                    
               # Проверка на существование аргумента
               for key in kwargs.keys():
                    if key not in self.__json[self.__table]['__types']:
                         raise ValueError(f"Argument {key} not exists")
          self.__save(kwargs)
               