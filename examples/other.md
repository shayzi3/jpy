### You can get the length of the data.

```python
print(len(YourModel))
```

### Also you can insert data with help '+'

```python
User() + {
     "id": 909,
     "name": "shayzi3",
     "money": 0,
     "lvl": 0
}
```

### custom_option

argument: return_success_type: Any = True
`Now the function can return more than just a Boolean type. Now she will return what you need.`


```python
from json_orm import custom_option, Select


@custom_option(model=User, return_success_type=1)
def validate(id, name) -> int:
     if id > 100 and 'shayzi3' in name:
          return 1

user = Select(User).custom_options(validate).one()
print(user.name)
```
`In this case, if 1 is returned, it will be a successful sorting.`
