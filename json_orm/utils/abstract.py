
import json_orm as orm

from abc import ABC, abstractmethod
from .checking import _attrs_data_class
from json_orm.utils.exception import TableColumnNotExists



__all__ = (
     "BaseClass",
     "MetaOrm"
)


class BaseClass(ABC):

     @abstractmethod
     def where(self):
          ...
          
          
     @abstractmethod
     def values(self):
          ...
          
          
           
          
class MetaOrm(type):
     __metadata__ = []
     
     def __new__(cls, name, bases, attrs):
          if not bases:
               return super().__new__(cls, name, bases, attrs)
          
          if not attrs.get('__annotations__'):
               raise TableColumnNotExists(f"class {name} dont have columns")
          
          metadata = _attrs_data_class(
               attrs.get('Data'),
               name
          )
          metadata['columns'] = []
          for key, value in attrs.get('__annotations__').items():
               if issubclass(value, orm.Column):
                    metadata['columns'].append(key)
               
          functions = {}
          for key, value in attrs.items():
               if callable(value) and not isinstance(value, type):
                    functions[key] = value
                    
          attrs = {
               key: key for key in metadata['columns']
          }
          attrs.update(functions)
          attrs.update({'metadata': metadata})
          cls.__metadata__.append(attrs)
          
          return super().__new__(cls, name, bases, attrs)