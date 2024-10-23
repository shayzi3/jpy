
from typing import Any





def valide_input_data(
     data: dict[str, Any],
     json_file: dict[str, Any],
     table_name: str,
     free: bool
) -> bool:
     if table_name not in json_file.keys():   
          raise ValueError(f"Table {table_name} not exists")
        
     if free:
          types = json_file[table_name].keys()
          
     else:
          types = json_file[table_name]['__types']
        
     if not free:
          for key in types: 
               if key not in data.keys(): # Пропущенный аргумент
                    raise ValueError(f"Required argument {key} for table {table_name}")
               
     for key in data.keys():
          if key not in types:  # Несуществующий аргумент
               raise ValueError(f"Argument {key} not exists")
     return True