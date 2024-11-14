import json
import os


from typing_extensions import (
     Generic,
     TypeVar,
     Self,
     Iterable
)
from json_orm.utils import (
     MetaData,
     BaseClass,
     _save,
     _list_or_dict,
     _valide_input_data,
     _where_for_update_and_delete
)
from json_orm.utils.exception import (
     NotFoundMetadata,
     FileNotFound
)



ClassType = TypeVar("ClassType")



class Update(BaseClass, Generic[ClassType]):
     __slots__ = (
          "__table",
          "__tablename",
          "__free",
          "__path",
          "__primary",
          "__columns",
          "__json_obj",
          "__where_values",
     )
     
     def __init__(self, table: ClassType) -> None:
          dict_type = table.__dict__.get('metadata')
          if dict_type:
               type_ = MetaData(**dict_type)
          else:
               raise NotFoundMetadata(f"Metadata about class {table.__class__.__name__} not found.")
          
          self.__table = table
          self.__tablename = type_.tablename
          self.__free = type_.free
          self.__path = type_.path
          self.__primary = type_.primary
          self.__columns = type_.columns
          self.__where_values = []
          
          if not os.path.exists(self.__path):
               raise FileNotFound(f"Json file {self.__path} not exists")
          
          with open(self.__path, 'r', encoding='utf-8') as file:
               self.__json_obj = json.loads(file.read())
          
          
     def __valide(self, obj: Iterable) -> None:
          _valide_input_data(
               data=obj,
               json_file=self.__json_obj,
               table_name=self.__tablename,
               free=self.__free,
               primary=self.__primary,
               columns=self.__columns
          )
          
          
     def where(self, **kwargs) -> Self:
          if self.__free:
               return self
          
          data = self.__json_obj[self.__tablename]['data']
          if not data:
               return self
          
          if not kwargs:
               self.__where_values = _list_or_dict(data)
               return self
          
          self.__valide(kwargs)
          self.__where_values = _where_for_update_and_delete(
               data=data,
               kwargs=kwargs,
               primary_key=self.__primary
          )
          return self
          
          
     
     def values(self, **kwargs) -> ClassType | None:
          if not kwargs:
               return None
          
          self.__valide(kwargs)
          if self.__free:
               for kw_key in kwargs.keys():
                    self.__json_obj[self.__tablename][kw_key] = kwargs[kw_key]
               
          else:   
               if not self.__where_values:
                    return None
               
               for dicts in self.__where_values:
                    primary_key_changed = ''
                    
                    for key, value in dicts.items():
                         if isinstance(value, dict):
                              for kw_key in kwargs.keys():
                                   if kw_key == self.__primary:
                                        primary_key_changed = key
                                   value[kw_key] = kwargs[kw_key]
                         
                         else:
                              for kw_key in kwargs.keys():
                                   dicts[kw_key] = kwargs[kw_key]
                              break
                    
                    if isinstance(value, dict):
                         if isinstance(value.get(self.__primary), int):
                              key = str(value[self.__primary])
                         self.__json_obj[self.__tablename]['data'][key] = value
                         
                         if primary_key_changed:
                              del self.__json_obj[self.__tablename]['data'][primary_key_changed]
                         
                    elif isinstance(key, int):
                         self.__json_obj[self.__tablename]['data'][key] = value
          _save(
               obj=self.__json_obj,
               path=self.__path
          )
          return self.__table(**kwargs)
                         
                    
                    
     