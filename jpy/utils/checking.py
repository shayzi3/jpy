
from typing import Any
from jpy.utils.enums import Mode





def valide_input_data(
     data: dict[str, Any],
     json_file: dict[str, Any],
     table_name: str,
     free: bool,
     primary: str,
     mode: Mode
) -> bool:
     if table_name not in json_file.keys():   
          raise ValueError(f"Table {table_name} not exists")
        
     if free:
          types = json_file[table_name].keys()
          
     else:
          types = json_file[table_name]['__types']
        
     if not free:
          if primary and primary not in types:
               raise ValueError(f"key {primary} in __primary__ not exists")

          if mode == Mode.INSERT:
               for key in types: 
                    if key not in data.keys(): # Пропущенный аргумент
                         raise ValueError(f"Required argument {key} for table {table_name}")
               
     for key in data:
          if key not in types:  # Несуществующий аргумент
               raise ValueError(f"Argument {key} not exists")
     return True