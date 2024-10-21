
import json     

from .src.methods import Update     
          
          
          
          

class JsonPy:
     __slots__ = (
          "__metadata",
          "__path"
     )
     
     def __init__(
          self, 
          *args: type, 
          path: str = 'base.json',
          free_arguments: list[str] | type | None = None
     ) -> None:
          
          self.__metadata = {}
          self.__path = path
          
          for class_ in args:
               attributes_class = class_.__annotations__
               
               if not attributes_class:
                    raise TypeError(f"Class {class_.__qualname__} dont have any annotations")
               
               class_dict = class_.__dict__
               name = class_.__qualname__
               
               if '__tablename__' in class_dict:
                    name = class_.__tablename__
                    
                    
               self.__metadata[name] = {
                    '__types': [key for key in attributes_class.keys()],
                    'data': []
               }
               
          if free_arguments:
               iter_ = free_arguments
               if isinstance(free_arguments, type):
                    iter_ = free_arguments.__annotations__.keys()
               
               self.__metadata.update({'__free': {f: None for f in iter_}}) 
                    
               
     def create(self) -> None:
          with open(self.__path, 'w') as file:
               json.dump(self.__metadata, file, indent=4)
               
               
     def update(
          self,
          table: str | object | None = None
     ) -> Update:
          if not table or table == '__free':
               return Update(
                    table='__free',
                    path=self.__path
               )
               
          if isinstance(table, type):
               name = table.__qualname__
               if '__tablename__' in table.__dict__:
                    name = table.__tablename__
               table = name
               
          if table not in self.__metadata.keys():
               raise ValueError(f"Not found table {table}")
               
          return Update(
               table=table,
               path=self.__path
          )
          
     
     def __repr__(self) -> str:
          return f"JsonPy <path=/{self.__path}>"