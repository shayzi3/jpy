
from jpy import JsonPy




class Base(JsonPy):
     __path_to_json__ = 'example.json'
     
    
     
class User(Base):
     __tablename__ = 'user'
     __primary__ = 'id'
     
     id: int
     username: str
     money: int
     level: float 
     
     
class Item(Base):
     __tablename__ = 'item'
     
     id: int
     name: str
     price: float
     


class Free(Base):
     __free__ = True
     __tablename__ = 'user'
     
     money: int
     level: float
     

  
# Free().insert(
#      {'money': 1, 'level': 122}
# )     

# item = Item.insert(
#      {
#           'id': 1917,
#           'name': 'mikle',
#           'price': 31
#      }
# )
# print(item.id, item.name, item.price)
# User().insert(
#      {
#           'id': 3,
#           'username': 'ben',
#           'money': 555,
#           'level': 135
#      }
# )
# print(Free.select())


# f = Free.select(
#      values = ['level']
# )
# print(f.level)

result = Item.select(
)
print(result)

     
 
# User() + {
#      'id': 1,
#      'username': 'Vlad'
# }

# Item(
#      {
#           'id': 5, 
#           'name': 10, 
#           'price': 5.0
#      }
# )
# Free() + {
#      'level': 101
# }
# if __name__ == '__main__':
#      Base().create()