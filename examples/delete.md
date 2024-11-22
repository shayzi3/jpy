
### Delete method


```python
from json_orm import Delete

Delete(User).drop_one_data(id=909)
Delete(User).drop_data()
Delete(User).drop_table()
```

# class: Delete

## method: `drop_table()`
returns: `None`

Delete the table from the database

## method: `drop_data()`
returns: `None`

This method resets the data

## method: `drop_one_data(**kwargs)`
returns: `None`

At the input, this method takes values that will be used to search for data to delete.


`Important! Free tables dont have methods drop_one_data, drop_data, drop_one_data_option`


## method: `drop_one_data_option(option: Callable)`
returns: `None`

You pass a function with your own validation to the method.

```python
from json_orm import custom_option

@custom_option(model=User)
def validate(id):
     return id % 2 != 0

Delete(User).drop_one_data_option(validate)
```