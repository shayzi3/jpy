
import json
import os


from typing import Any  
from jpy.utils import valide_input_data


          

class JsonPy:
     __tablename__: str | None = None
     __path__: str  = 'baser.json'
     __free__: bool = False
     
     __json = {}
     
     
     def __init__(
          self, 
          data: dict[str, Any] | None = None
     ) -> None:
          if not os.path.exists(self.__path__):
               open(self.__path__, 'w').close()
          
          with open(self.__path__, 'r') as file:
               read_file = file.read()
               if read_file:
                    self.__class__.__json = json.loads(file.read())
               
          if data: self + data
     
     
     @classmethod
     def create(cls) -> None:
          classes = cls.__subclasses__()
          
          if not classes:
               return None
          
          metadata = {}
          for class_ in classes:
               attributes_class = class_.__annotations__
               
               if not attributes_class:
                    raise TypeError(f"Class {class_.__qualname__} dont have attributes")
               
               name = class_.__qualname__
               if class_.__tablename__:
                    name = class_.__tablename__
                    
               if class_.__free__:
                    if not cls.__json.get(name):
                         metadata[name] = {}
                         
                    metadata[name].update(
                         {
                              key: None for key in attributes_class.keys()
                         }
                    )
                    continue
                    
               metadata[name] = {
                    '__types': [key for key in attributes_class.keys()],
                    'data': []
               }
          return cls.__save(metadata)               
               
         
     @classmethod  
     def __tablename_or_class(cls) -> str:
          name = cls.__name__
          if cls.__tablename__:
               name = cls.__tablename__
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
               raise TypeError("If you want add new data, you must use dict")

          name = cls.__tablename_or_class()
               
          valide_input_data(
               data=obj,
               json_file=cls.__json,
               table_name=name,
               free=cls.__free__
          )  
          if not cls.__free__:
               cls.__json[name]['data'].append(obj)
          
          else:
               for key, value in obj.items():
                    cls.__json[name][key] = value
          return cls.__save(cls.__json)
          
          
     @classmethod
     def __repr__(cls) -> str:
          name = cls.__tablename_or_class()
          
          if name in cls.__json.keys():
               return f'jpy_model <class={cls.__name__} table={name} path={cls.__path__}>'
          return cls.__name__