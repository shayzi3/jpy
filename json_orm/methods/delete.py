import json
import os


from typing_extensions import (
     Iterable,
     Callable
)
from json_orm.utils import (
     MetaData,
     _valide_input_data,
     _save,
     _custom,
     _get_custom_args
)
from json_orm.utils.exception import (
     NotFoundMetadata,
     FileNotFound,
     TableNotExists
)




class Delete:
     __slots__ = (
          "__table",
          "__tablename",
          "__free",
          "__path",
          "__primary",
          "__columns",
          "__json_obj",
     )
     
     def __init__(self, table: type) -> None:
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
          
          if not os.path.exists(self.__path):
               raise FileNotFound(f"Json file {self.__path} not exists")
          
          with open(self.__path, 'r', encoding='utf-8') as file:
               self.__json_obj = json.loads(file.read())
               
          if self.__tablename not in self.__json_obj.keys():
               raise TableNotExists(f"Table {self.__tablename} not exists")
               
     def __valide(self, obj: Iterable) -> None:
          _valide_input_data(
               data=obj,
               json_file=self.__json_obj,
               table_name=self.__tablename,
               free=self.__free,
               primary=self.__primary,
               columns=self.__columns,
          )
          
          
     def drop_one_data(self, **kwargs) -> None:
          if self.__free: return None
          
          data = self.__json_obj[self.__tablename]['data']
          if not data or not kwargs:
               return None
                    
          self.__valide(kwargs)
          if isinstance(data, dict):
               if self.__primary not in kwargs.keys():
                    for key, value in data.items():
                         for kw_key in kwargs.keys():
                              if kwargs[kw_key] == value[kw_key]:
                                   del self.__json_obj[self.__tablename]['data'][key]
               else:
                    key = kwargs[self.__primary]
                    if isinstance(key, int):
                         key = str(key)
                         
                    if data.get(key):
                         del self.__json_obj[self.__tablename]['data'][key]
          
          iter_data = data.copy()  
          if isinstance(iter_data, list):
               for index in range(len(iter_data)):
                    for kw_key in kwargs.keys():
                         if kwargs[kw_key] == iter_data[index][kw_key]:
                              self.__json_obj[self.__tablename]['data'].pop(index)
          return _save(
               obj=self.__json_obj,
               path=self.__path
          )
          
     def drop_one_data_option(self, option: Callable) -> None:
          if self.__free: return None
          
          data = self.__json_obj[self.__tablename]['data']
          if not data:
               return None
     
          meta_function, data = _custom(data, option)
          args, func, return_type = _get_custom_args(
               data=meta_function,
               tablename=self.__tablename
          )
          
          iter_data = data.copy()
          for index in range(len(iter_data)):
               kwargs = {key: iter_data[index].get(key) for key in args}
                   
               if func(**kwargs) == return_type:
                    if self.__primary:
                         index = iter_data[index].get(self.__primary)
                         if isinstance(index, int):
                              index = str(index)
                         del self.__json_obj[self.__tablename]['data'][index]
                    else:
                         self.__json_obj[self.__tablename]['data'].pop(index)
                    
          return _save(
               obj=self.__json_obj,
               path=self.__path
          )
          
          
     def drop_table(self) -> None:
          del self.__json_obj[self.__tablename]
          
          return _save(
               obj=self.__json_obj,
               path=self.__path
          )
     
     def drop_data(self) -> None:
          if self.__free: return None
          
          type_data = self.__json_obj[self.__tablename]['data']
          if isinstance(type_data, dict):
               self.__json_obj[self.__tablename]['data'] = {}
          
          elif isinstance(type_data, list):
               self.__json_obj[self.__tablename]['data'] = []
               
          return _save(
               obj=self.__json_obj,
               path=self.__path
          )