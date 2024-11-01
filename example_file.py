
from json_orm import (
     JsonOrm, 
     Column, 
     DataArgs,
     Insert,
     Select
)




class User(JsonOrm):
     id: Column
     name: Column
     
     class Data(DataArgs):
          tablename = 'user'
          primary = 'id'
          
     # or
     # class Data:
     #      tablename = 'user'
     #      primary = 'id'
          
          
          
class Item(JsonOrm):
     id: Column
     name: Column
     price: Column
     quality: Column
     
     
     
class Free(JsonOrm):
     status: Column
     
     class Data(DataArgs):
          tablename = 'free_keys'
          free = True
          
          
        
if __name__ == '__main__':
     JsonOrm.create_tables() # or JsonOrm.create_tables(User, Item)
     # user = Insert(User).values(
     #      id=555,
     #      name='my'
     # )
     # print(user.name, user.id)

     # item = Insert(Item).values(
     #      id=123,
     #      name='MY',
     #      price=100.0,
     #      quality=10
     # )
     # or
     print(Free.__dict__)
     # user = User() + {'id': 677, 'name': 'Kirill'}
     # print(user.id, user.name)
     
     # item = Select(Item).where(quality=10).values()
     # if isinstance(item, list):
     #      print(item)
     # else:
     #      print(item.name, item.id)
          
     # user = Select(User).values()
     # print(user)
     
     # print(item.id, item.name, item.price, item.quality)
     # print(User.__dict__)
     # print(Item.__dict__)
     
     #User - {
          # 'id': None, 
          # 'name': None, 
          # 'metadata': {
               # 'path': 'base.json', 
               # 'tablename': 'user', 
               # 'free': None, 
               # 'primary': 'id', 
               # 'columns': ['id', 'name']
               #}, 
               # '__module__': 'json_orm.utils.abstract', 
               # '__doc__': None
     # }
     
     
     # Item - {
          # 'id': None, 
          # 'name': None, 
          # 'price': None, 
          # 'quality': None, 
          # 'metadata': {
               # 'path': '.json', 
               # 'tablename': 'Item', 
               # 'free': None, 
               # 'primary': None, 
               # 'columns': ['id', 'name', 'price', 'quality']
          # }, 
          # '__module__': 'json_orm.utils.abstract', 
          # '__doc__': None
     # }
     
     # user = User(id=5, name='Vlad')
     # print(user.id, user.name) - 5 Vlad

     
     
# How look insert, delete, update, select methods
# Insert(Table).values(kwargs)
# Delete(Table).where(kwargs)
# Select(Table).where(kwargs).values(args: str)
# Update(Table).where(kwargs).values(args: str)