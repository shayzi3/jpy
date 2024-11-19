
### Select method


```python
from json_orm import Select


# Let's imagine, that User its a model
user = Select(User).where(id=15)

# where return Output[type[User]]
# 1. Excample
print(user.one()) # -> type[User]
print(user.all()) # -> list[type[User]]

# 2. Example
user_data_one = user.one()


# And in this case, you can access the attributes of the 'User' class and get the data that is returned.
print(
     user_data_one.id,
     user_data_one.name,
     user_data_one.money,
     user_data_one.lvl
)
# 15 shayzi3 1500 100

user_data_all = user.all()
print(user_data_all)
# [User(id=15 name=shayzi3 money=1500 lvl=100)]
```
If the data does not exist, then None is returned, will return User(id=None name=None money=None lvl=None)


```python

user = Select(User).where(id=909).one()

if user.id:
     return increment_money(user.id, 100)
return 'User not found.'
```


# class: Output
This class accepts a model and sorted data as input.

## method: one()
returns: ```type[Model]```

Returns the first element of the sorted data.

## method: all()
returns: ```list[type[Model]]```

Returns all elements of the sorted data.



# class: Select
This class accepts a model as input.

## method: where(**kwargs)
returns: ```Output[type[Model]]```

This method extracts melons from a json file.
`Important! This method only compares the data.`


## method: custom_options(option)
returns: ```Output[type[Model]]```

This method accepts a function in which you can specify your own validation.

```python
from json_orm import custom_option


@custom_option(model=User)
def validate_user(id, name) -> bool:
     return id > 100 and 'shayzi3' in name


user = Select(User).custom_options(validate_user).one()
print(
     user.id,
     user.name,
     user.money,
     user.lvl
)
```
`The function validate_user accepts columns as input, which are located in the model User.`
`Important! Function validate_user must return boolean type.`