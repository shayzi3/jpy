
import json
from typing import Any     
from .src.methods import Update     
          
          

class BaseJsonPy:
     __cache = {}
     __tablename__ = None
     
     
     def __new__(cls, path: str | None = None):
          if cls.__name__ not in cls.__cache:
               cls.__cache[cls.__name__] = path
               return f'class {cls.__name__} cached'
          return super().__new__(cls)

     
     def __init__(self) -> None:
         self.path = self.__cache[self.__class__.__name__]         
         
         
     def __tablename_or_class(self) -> str:
          name = self.__class__.__name__
          if self.__class__.__tablename__:
               name = self.__class__.__tablename__
               
          return name
     
     
     def __save(self, data: dict[str, Any]) -> bool:
          with open(self.path, 'w') as file:
               json.dump(data, file, indent=4)
          return True
     
     
     def __len__(self) -> int:
          """Get len your data

          Returns:
             int
          """
          name = self.__tablename_or_class()
          
          with open(self.path, 'r') as file:
               data = json.loads(file.read())[name]['data']
          return len(data)
          
          
     def __add__(self, obj: dict[str, Any]) -> None:
          name = self.__tablename_or_class()

          with open(self.path, 'r') as file:
               data: dict = json.loads(file.read())
            
          if name not in data.keys():   
               raise ValueError(f"Table {name} not exists")
          
          types = data[name]['__types']
          for key in types:
               if key not in obj.keys():
                    raise ValueError(f"Unexpected argument {key} for table {name}")
               
          for key in obj.keys():
               if key not in types:
                    raise ValueError(f"Argument {key} not exists")
               
          data[name]['data'].append(obj)
          self.__save(data)
          
          
     def __repr__(self) -> str:
          return f'jpy_model <class={self.__class__.__name__} path={self.__cache[self.__class__.__name__]}>'



class JsonPy:
     __slots__ = (
          "_metadata",
          "_path",
     )
     
     def __init__(
          self, 
          *args: type, 
          path: str = 'base.json',
          free_arguments: list[str] | type | None = None
     ) -> None:
          
          self._metadata = {}
          self._path = path
          
          for class_ in args:
               attributes_class = class_.__annotations__
               
               if not attributes_class:
                    raise TypeError(f"Class {class_.__qualname__} dont have any annotations")
               
               name = class_.__class__.__name__
               if class_.__tablename__:
                    name = class_.__tablename__
                    
               self._metadata[name] = {
                    '__types': [key for key in attributes_class.keys()],
                    'data': []
               }
               class_.__new__(class_, self._path)

               
          if free_arguments:
               if isinstance(free_arguments, list):
                    iter_ = free_arguments
                    
               elif isinstance(free_arguments, type):
                    iter_ = free_arguments.__annotations__.keys()
                    
               else:
                    raise ValueError("wrong type data in free_argument must be list[str] | type | None")
               self._metadata.update({'__free': {f: None for f in iter_}}) 
                    
               
     def create(self) -> None:
          with open(self._path, 'w') as file:
               json.dump(self._metadata, file, indent=4)
               
               
     def update(
          self,
          table: str | object | None = None
     ) -> Update:
          if not table or table == '__free':
               return Update(
                    table='__free',
                    path=self._path
               )
               
          if isinstance(table, type):
               name = table.__qualname__
               if '__tablename__' in table.__dict__:
                    name = table.__tablename__
               table = name
               
          if table not in self._metadata.keys():
               raise ValueError(f"Not found table {table}")
               
          return Update(
               table=table,
               path=self._path
          )
          
     
     def __repr__(self) -> str:
          return f"JsonPy <path=/{self.__path}>"