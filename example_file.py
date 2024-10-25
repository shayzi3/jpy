
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
     
     id: int
     name: str
     price: float
     


class Free(Base):
     __free__ = True
     __tablename__ = 'user'
     
     money: int
     level: float
     


  
# Free().insert(
#      {'money': 1}
# )     

# Item().insert(
#      {
#           'id': 12,
#           'name': 'apple',
#           'price': 3.2
#      }
# )
# User().insert(
#      {
#           'id': 13,
#           'username': 'micro'
#      }
# )
print(Free().select())
# result = User().select(
#      values = ('id',)
# )
# print(result)


     
 
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