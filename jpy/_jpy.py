import json
import os


from typing import Any
from jpy.methods import Insert, Select
from jpy.utils.exception import (
     FileNotValide,
     ClassWithoutColumns,
     CannotCreateTable
)


          
class JsonPy:
     __tablename__: str | None = None
     __path_to_json__: str  = 'baser.json'
     __free__: bool = False
     __primary__: str | None = None
     
     __json = {}
     
     
     def __init__(self) -> None:
          if self.__path_to_json__.split('.')[-1] != 'json':
               raise FileNotValide('Path to json file must end with .json')
                    
          if not os.path.exists(self.__path_to_json__):
               open(self.__path_to_json__, 'w').close()
          
          with open(self.__path_to_json__, 'r') as file:
               read_file = file.read()
               if read_file:
                    self.__class__.__json = json.loads(read_file)     
     
     
     @classmethod
     def create(cls) -> None:
          classes = cls.__subclasses__()
          if not classes:
               return None
          
          if cls.__base__ != JsonPy:
               raise CannotCreateTable(f"Class {cls.__name__} is not a subclass of JsonPy")

          metadata = {}
          for class_ in classes:
               attributes_class = class_.__annotations__
               
               if not attributes_class:
                    raise ClassWithoutColumns(f"Class {class_.__qualname__} dont have columns.")
               
               name = class_.__qualname__
               if class_.__tablename__:
                    name = class_.__tablename__
                    
               if class_.__free__:
                    if not metadata.get(name):
                         metadata[name] = {}
                         
                    metadata[name].update(
                         {
                              key: None for key in attributes_class.keys()
                         }
                    )
                    continue
                    
               metadata[name] = {
                    '__types': [key for key in attributes_class.keys()],
                    'data': {} if class_.__primary__ else []
               }
          return cls.__save(metadata)    
     
     
     @classmethod
     def insert(cls, values: dict[str, Any]) -> type:
          if not values:
               return None
          
          if not cls.__json: 
               cls()
          
          name = cls.__tablename_or_class()
          Insert(
               table=name,
               json_obj=cls.__json,
               path=cls.__path_to_json__,
               free=cls.__free__,
               primary=cls.__primary__
          ).values(**values)  
          return type(cls.__name__, (), values)
          
          
     @classmethod
     def select(
          cls,
          where: dict[str, Any] = {},
          values: list[str] | tuple[str] = []
     ) -> type | None | list[dict[str, Any]]:
          name = cls.__tablename_or_class()
          
          if not cls.__json: 
               cls()
               
          select_data = Select(
               table=name,
               json_obj=cls.__json,
               primary=cls.__primary__,
               path=cls.__path_to_json__,
               free=cls.__free__
          ).where(**where).values(values)
          
          if isinstance(select_data, dict):
               return type(cls.__name__, (), select_data)
          return select_data
          
          
          
     @classmethod
     def update(cls) -> None:
          ...
          
          
          
     @classmethod
     def delete(cls) -> None:
          ...   
               
         
     @classmethod  
     def __tablename_or_class(cls) -> str:
          name = cls.__name__
          if cls.__tablename__:
               name = cls.__tablename__
          return name
     
     
     @classmethod
     def __save(cls, data: dict[str, Any]) -> None:
          with open(cls.__path_to_json__, 'w') as file:
               file.write(json.dumps(data, indent=4))
     
     
     @classmethod
     def __len__(cls) -> int:
          """Get len your data

          Returns:
             int
          """
          name = cls.__tablename_or_class()
          with open(cls.__path_to_json__, 'r') as file:
               data = json.loads(file.read())[name]['data']
          return len(data)
          
       
     @classmethod   
     def __add__(cls, obj: dict[str, Any]) -> None:
          return cls.insert(values=obj)
          
         
     @classmethod 
     def __repr__(cls) -> str:
          name = cls.__tablename_or_class()
          
          if name in cls.__json:
               return f'json model <class={cls.__name__} tablename={name} path={cls.__path_to_json__}>'
          return f'class @{cls.__name__}'
          
          