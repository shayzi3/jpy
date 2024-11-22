
### Update method


```python
from json_orm import Update

Update(User).where(id=909).values(name='shayzi3')
Update(User).where(name='shayzi3').values(money=1000)
```

# class: Update
The class accepts a model as input.

## method: `where(**kwargs)`
returns: `self`

Here the pillars are indicated along which the search will be performed.

## method: `custom_options(option: Callable)`
returns: `self`

It works exactly the same as where, but only the function is passed with your verification.

## method: `values(**kwargs)`
returns: `None`

And this class is columns with their new values.


`Important! Model where Free is True dont have method 'where'`

With use custom option
```python
from json_orm import custom_option

@custom_option(model=User)
def validate(id):
     return id % 2 == 0

Update(User).custom_options(validate).values(name="even")
```


