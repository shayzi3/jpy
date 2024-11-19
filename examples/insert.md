
### Insert method

```python
from json_orm import Insert

user = Insert(User).values(
     id=909,
     name='shayzi3',
     money=0,
     level=0
)
print(
     user.id,
     user.name,
     user.money,
     user.lvl
)
# 909 shayzi3 0 0
```
# class: Insert
This class accepts a model as input.

## method: values(**kwargs)
returns: `type[Model]`

`Important! The method values includes all columns of the model!`

```python
Insert(User).values(
     id=909,
     name='shayzi3',
     money=0
)
```
`class User have columns: id, name, money, lvl`
`In this example, there will be an error because not all columns were transferred. The first example is correct.`
