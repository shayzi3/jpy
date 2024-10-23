
from jpy import JsonPy




class Base(JsonPy):
     __path__ = 'other.json'
     
    
     
class User(Base):
     __tablename__ = 'user'
     
     id: int
     username: str
     
     
     
class Item(Base):
     __tablename__ = 'item'
     
     id: int
     name: str
     price: float
     


class Free(Base):
     __tablename__ = 'item'
     __free__ = True
     
     money: int
     level: float
     
     
     
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
     
     
if __name__ == '__main__':
     Base().create()