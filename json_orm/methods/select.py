import json
import os


from typing_extensions import (
     Generic, 
     TypeVar,
     Iterable,
     Callable
)
from json_orm.utils import (
     _valide_input_data, 
     _list_or_dict,
     MetaData,
     Output
)
from json_orm.utils.exception import (
     NotFoundMetadata, 
     FileNotFound,
     CallableError
)


ClassType = TypeVar("ClassType")



class Select(Generic[ClassType]):
     __slots__ = (
          "__table",
          "__free",
          "__path",
          "__primary",
          "__tablename",
          "__json_obj",
          "__columns",
     )
     
     def __init__(self, table: ClassType) -> None:
          dict_type = table.__dict__.get('metadata')
          if dict_type:
               type_ = MetaData(**dict_type)
          else:
               raise NotFoundMetadata(f"Metadata about class {table.__qualname__} not found.")
          
          self.__table = table
          self.__tablename = type_.tablename
          self.__free = type_.free
          self.__path = type_.path
          self.__primary = type_.primary
          self.__columns = type_.columns
          
          if isinstance(self.__primary, int):
               self.__primary = str(self._primary)
               
          if not os.path.exists(self.__path):
               raise FileNotFound(f"Json file {self.__path} not exists")
          
          with open(self.__path, 'r', encoding='utf-8') as file:
               self.__json_obj = json.loads(file.read())
               
          
     def __validate(self, obj: Iterable) -> None:
          _valide_input_data(
               data=obj,
               json_file=self.__json_obj,
               table_name=self.__tablename,
               free=self.__free,
               columns=self.__columns,
               primary=self.__primary
          )
               
     def where(self, **kwargs) -> Output[ClassType]:
          if self.__free:
               column = self.__json_obj[self.__tablename]
               return Output(
                    table=self.__table,
                    data=[{key: column.get(key) for key in self.__columns}]
               )
          data = self.__json_obj[self.__tablename]['data']
          if not data:
               return Output(
                    table=self.__table,
                    data=[{key: None for key in self.__columns}]
               )
          if not kwargs:
               return Output(
                    table=self.__table,
                    data=_list_or_dict(data)
               )

          self.__validate(kwargs)
          result = []
          if isinstance(data, dict):
               if self.__primary in kwargs.keys():
                    primary = kwargs[self.__primary]
                    if isinstance(primary, int):
                         primary = str(primary)
                         
                    if not data.get(primary):
                         return Output(
                              table=self.__table,
                              data=[{key: None for key in self.__columns}]
                         )
                         
                    result.append(data.get(primary))
                    del kwargs[self.__primary]
                    
               if kwargs:
                    if result:
                         for value in result:
                              for kw_key in kwargs.keys():
                                   if value[kw_key] != kwargs[kw_key]:
                                        del result[0]
                    else:
                         data = list(data.values())
          
          if isinstance(data, list):
               for dicts in data:
                    count = 0
                    for kw_key in kwargs.keys():
                         if dicts[kw_key] == kwargs[kw_key]:
                              count += 1
                    
                    if count == len(kwargs):
                         result.append(dicts)
          return Output(
               table=self.__table,
               data=result
          )

     
     def custom_options(self, option: Callable) -> Output[ClassType]:
          json_data = self.__json_obj[self.__tablename]['data']
          if not json_data: 
               return Output(
                    table=self.__table,
                    data=[{key: None for key in self.__columns}]
               )
          
          if isinstance(json_data, dict):
               json_data = list(json_data.values())
          
          if not callable(option):
               raise CallableError(f"{option} its not callable object")
          meta_function = option()
               
          func = meta_function.get(self.__tablename).get('function')
          arguments = meta_function.get(self.__tablename).get('args')
          return_type = meta_function.get(self.__tablename).get('return_type')
             
          result = []
          for dict_ in json_data:
               kwargs = {key: dict_.get(key) for key in arguments}
                    
               if func(**kwargs) == return_type:
                    result.append(dict_)
          return Output(
               table=self.__table,
               data=result
          )