
import orm_json as orm

from .checking import _attrs_data_class
from orm_json.utils.exception import TableColumnNotExists
           
          
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
          columns = set()
          for key, value in attrs.get('__annotations__').items():
               if issubclass(value, orm.Column):
                    columns.add(key)
          metadata['columns'] = list(columns)
               
          functions = {}
          for key, value in attrs.items():
               if callable(value) and not isinstance(value, type):
                    functions[key] = value
                    
          attrs = {
               key: f'__{key}__' for key in metadata['columns']
          }
          attrs.update(functions)
          attrs.update({'metadata': metadata})
          cls.__metadata__.append(attrs)
          
          return super().__new__(cls, name, bases, attrs)