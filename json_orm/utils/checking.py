
from typing import Any, Iterable
from json_orm.utils.enums import Mode
from json_orm.utils.exception import (
     TableNotExists,
     TableColumnNotExists,
     RequiredArgument,
     PrimaryNotExists,
     JsonFileEmpty
)



__all__ = (
     "_valide_input_data",
     "_attrs_data_class",
)


def _valide_input_data(
     data: Iterable,
     json_file: dict[str, Any],
     table_name: str,
     free: bool,
     primary: str,
     columns: list[str],
     mode: Mode | None = None
     
) -> bool:
     if not json_file:
          raise JsonFileEmpty(f"Json file empty. Create a tables.")
     
     # Table not exists
     if table_name not in json_file.keys():   
          raise TableNotExists(f"Table {table_name} not exists.")
        
     if free:
          types = []
          for type_ in json_file[table_name].keys():
               if type_ not in ['columns', 'data']:
                    types.append(type_)
     else:
          types = columns
        
     if not free:
          if primary and primary not in types:
               raise PrimaryNotExists(f"Primary key {primary} in table {table_name} not exists.")

          if mode == Mode.INSERT:
               for key in types: 
                    if key not in data.keys(): # Missed argument for insert method
                         raise RequiredArgument(f"Missed column {key} for table {table_name}.")
               
     for key in data:
          if key not in types:  # Argument not exists
               raise TableColumnNotExists(f"Table {table_name} dont have column {key}.")
     return True




def _attrs_data_class(
     data_class: type | None,
     name_class: str
     
) -> dict[str, Any]:
     default_values = {
          'path': 'base.json',
          'primary': None,
          'free': False
     }
     
     metadata = {}
     if not data_class:
          metadata['path'] = default_values.get('path')
          metadata['tablename'] = name_class
          metadata['primary'] = default_values.get('primary')
          metadata['free'] = default_values.get('free')
          
     else:
          data = data_class.__dict__
          for keyword in ['path', 'tablename', 'free', 'primary']:
               if data.get(keyword):
                    metadata[keyword] = data.get(keyword)
                    
               else:
                    if keyword == 'tablename':
                         metadata['tablename'] = name_class
                    
                    else:
                         metadata[keyword] = default_values.get(keyword)
     return metadata