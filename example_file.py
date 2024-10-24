
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
     

  
  
Free().insert(
     {'money': 19, 'level': 0.1}
)     

Item().insert(
     {
          'id': 123,
          'name': 'likee',
          'price': 5.55
     }
)

User().insert(
     {
          'id': 77,
          'username': 'My_penis'
     }
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