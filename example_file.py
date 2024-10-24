
from jpy import JsonPy




class Base(JsonPy):
     __path__ = 'example.json'
     
    
     
class User(Base):
     __tablename__ = 'user'
     __primary__ = 'id'
     
     id: int
     username: str
     
     
     
class Item(Base):
     __tablename__ = 'item'
     __primary__ = 'name'
     
     id: int
     name: str
     price: float
     


class Free(Base):
     __free__ = True
     
     money: int
     level: float
     

user, free = User(), Free()
     
user.update(
     values = {
          'id': 500,
          'username': 'Vlad'
     }
)
free.update(
     values = {'money': 10}
)

     
     
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