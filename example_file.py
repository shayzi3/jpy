
from json_orm import (
     JsonOrm, 
     Column, 
     DataArgs,
     Insert,
     Select,
     Update
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
          free = True
          
          
        
if __name__ == '__main__':
     # JsonOrm.create_tables() # or JsonOrm.create_tables(User, Item)
     # user = Insert(Item).values(
     #      id=172,
     #      name='Colum',
     #      price=9.3,
     #      quality=10.1
     # )
     # print(user.name, user.id)
     # Update(Item).where(id=172).values(name='jji')
     Update(Free).values(status=False)

     # item = Insert(Item).values(
     #      id=123,
     #      name='MY',
     #      price=100.0,
     #      quality=10
     # )
     # or
     # print(user.id, user.name)
     # insert = Insert(Free).values(status=True)
     select = Select(Item).where(id=172).values()
     free = Select(Free).values()
     print(select.name, free.status)
     
     
     
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