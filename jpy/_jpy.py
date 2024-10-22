
import json

from utils import valide_input_data
from typing import Any  
          
          

class JsonPy:
     __tablename__: str | None = None
     __path__: str  = 'baser.json'
     __free__: bool = False
     
     __metadata = {}
     
     
     def __init__(
          self, 
          data: dict[str, Any] | None = None
     ) -> None:
          
          if data:
               self + data
     
     
     @classmethod
     def create(cls) -> None:
          classes = cls.__subclasses__()
          
          if not classes:
               return None
          
          for class_ in classes:
               attributes_class = class_.__annotations__
               
               if not attributes_class:
                    raise TypeError(f"Class {class_.__qualname__} dont have attributes")
               
               name = class_.__qualname__
               if class_.__tablename__:
                    name = class_.__tablename__
                    
               if class_.__free__:
                    cls.__metadata['__free'] = {
                         key: None for key in attributes_class.keys()
                    }
                    continue
                    
               cls.__metadata[name] = {
                    '__types': [key for key in attributes_class.keys()],
                    'data': []
               }
          return cls.__save(cls.__metadata)               
               
         
     @classmethod  
     def __tablename_or_class(cls) -> str:
          name = cls.__name__
          if cls.__tablename__:
               name = cls.__tablename__
               
          if cls.__free__:
               name = '__free'
               
          return name
     
     
     @classmethod
     def __save(cls, data: dict[str, Any]) -> None:
          with open(cls.__path__, 'w') as file:
               json.dump(data, file, indent=4)
     
     
     @classmethod
     def __len__(cls) -> int:
          """Get len your data

          Returns:
             int
          """
          name = cls.__tablename_or_class()
          with open(cls.__path__, 'r') as file:
               data = json.loads(file.read())[name]['data']
          return len(data)
          
       
     @classmethod   
     def __add__(cls, obj: dict[str, Any]) -> None:
          """Add new data in json moodel

          Args:
              obj (dict[str, Any]): Arguments from user. Class() + {'id': 1, 'name': 'John'}

          Raises:
              ValueError: Table ... not exists
              ValueError: Required argument ... for table ...
              ValueError: Argument ... not exists
          """
          if not isinstance(obj, dict):
               raise TypeError("If you wnt add new data, you must use dict")

          name = cls.__tablename_or_class()
          with open(cls.__path__, 'r') as file:
               data: dict = json.loads(file.read())
               
          valide_input_data(
               data=obj,
               json_file=data,
               table_name=name
          )  
          if name != '__free':
               data[name]['data'].append(obj)
          
          else:
               for key, value in obj.items():
                    data['__free'][key] = value
                    
          return cls.__save(data)
          
          
     def __repr__(self) -> str:
          if self.__class__.__name__ in self.__cache:
               return f'jpy_model <class={self.__class__.__name__} path={self.__cache[self.__class__.__name__]}>'
          else:
               return f'class <{self.__class__.__name__}>'