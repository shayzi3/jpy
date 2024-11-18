

### Create table


```python
from json_orm import (
     Column,
     DataArgs,
     JsonOrm
)

class User(JsonOrm):
     id: Column
     name: Column
     money: Column
     lvl: Column

     class Data(DataArgs):
          tablename = 'users'
          primary = 'id'
          path = 'base.json'
          free = False

          # If you specify the "primary" setting, then the "data" will have a dict otherwise list

if __name__ == '__main__':
     JsonOrm.create_tables() # or JsonOrm.create_tables(User)
```

```json
{
     "users": {
          "columns": ["id", "name", "money", "lvl"],
          "data": {} 
     }
}
```

User is a model and every class that inherits from JsonOrm and has columns is a model

## class: Column
This is just an empty class that is needed to denote the columns of the table.

## class: DataArgs
This class can be inherited into the internal 'Data' class. However, it is not mandatory, 
it just serves as a hint about the settings of the table. 


## Settings in 'Data'

`Important! It is necessary that the class for specifying model settings be called 'Data'`


# Default values of settings:
```
tablename = name your model
primary = None
path = base.json
free = False
```

```python
tablename: str
# Name table. If you dont hint of name table, then the name of your table will be taken from the name of the model itself.

primary: str | None
# Its not mandorory setting, but with primary key, methods Delete/Update/Select will be work faster.

path: str
# Path to your json file. If you dont hint of path, that its will be 'base.json'.

free: bool
# If these argument 'True', that its not a model
```

Initially, 'Data' can be omitted

```python

class Item(JsonOrm):
     id: Column
     item_name: Column
     price: Column

if __name__ == '__main__':
     JsonOrm.create_tables()

```

Create free model
```python

class FreeTable(JsonOrm):
     status: Column
     players: Column

     class Data:
          tablename = 'free'
          free = True


if __name__ == '__main__':
     JsonOrm.create_tables(FreeTable)
```

And after start this code in file 'base.json' will ↓

```json
{
     "free": {
          "status": null,
          "players": null
     }
}

```

Also if you point tablename 'users', but its table exists that ↓

```json
{
     "users": {
          "columns": [],
          "data": [],
          "status": null,
          "players": null
     }
}
```