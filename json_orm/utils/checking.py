import json

from typing_extensions import Any, Iterable
from json_orm.utils.enums import Mode
from json_orm.utils.exception import (
     TableNotExists,
     TableColumnNotExists,
     RequiredArgument,
     PrimaryNotExists,
     JsonFileEmpty
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
          metadata['tablename'] = name_class
          metadata['path'] = default_values.get('path')
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
                    
                    else: metadata[keyword] = default_values.get(keyword)
     return metadata


def _where_for_update_and_delete(
     data: Iterable,
     kwargs: dict[str, Any],
     primary_key: str | None
) -> list[dict[str, dict]] | type:
     
     result = []
     if isinstance(data, dict):
          if primary_key in kwargs.keys():
               primary = kwargs[primary_key]
               if isinstance(primary, int):
                    primary = str(primary)
                         
               if not data.get(primary):
                    return None
               result.append({primary: data.get(primary)})
               del kwargs[primary_key]
                     
          if kwargs:
               if result:
                    for index in range(len(result)):
                         for items_value in result[index].values():
                              for kw_key in kwargs.keys():
                                   if items_value[kw_key] != kwargs[kw_key]:
                                        del result[index]
               else:
                    data = list(data.values())
                    
     if isinstance(data, list):
          for index in range(len(data)):
               count = 0
               for kw_key in kwargs.keys():
                    if data[index][kw_key] == kwargs[kw_key]:
                         count += 1
                    
               if count == len(kwargs):
                    result.append({index: data[index]})
     return result

def _save(obj: dict[str, Any], path: str) -> None:
     with open(path, 'w', encoding='utf-8') as file:
          json.dump(obj, file, indent=4, ensure_ascii=False)
     return None
          
          
def _list_or_dict(obj: Iterable) -> list[dict[str, Any]]:
     if isinstance(obj, dict):
          return list(obj.values())
     return obj