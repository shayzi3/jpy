
import json_orm as orm

from abc import ABC, abstractmethod
from .checking import _attrs_data_class



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
               raise ValueError("Not column")
          
          metadata = _attrs_data_class(
               attrs.get('Data'),
               name
          )
          metadata['columns'] = []
          for key, value in attrs.get('__annotations__').items():
               if issubclass(value, orm.Column):
                    metadata['columns'].append(key)
               
          attrs = {
               key: None for key in metadata['columns']
          }
          attrs.update({'metadata': metadata})
          cls.__metadata__.append(attrs)
          
          return super().__new__(cls, name, bases, attrs)