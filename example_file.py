
from json_orm import (
     JsonOrm,
     Column,
     DataArgs,
     Insert,
     Select,
     Update,
     Delete,
     custom_option
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
     ...
     # create table
     # JsonOrm.create_tables() # or JsonOrm.create_tables(User, Item)
     
     # Insert
     # user = Insert(User).values(
     #      id=523,
     #      name='__name__'
     # )
     # print(user.name, user.id)
     
     # item = Insert(Item).values(
     #      id=123,
     #      name='Vlad',
     #      price=15,
     #      quality=1
     # )
     # insert = Insert(Free).values(status=False)
     
     
     # Delete
     # Delete(Table).drop_table()
     # Delete(Item).drop_one_data()
     # Delete(Item).drop_one_data(price=222)
     # Delete(Item).drop_one_data_option(check_price)
     
     
     # Update
     # print(Update(Item).where(id=123).values(name='Armen', price=222))
     # print(Update(Item).custom_options(check_price).values(name='Cooper'))
     # print(Update(Item).where().values(price=500))
     # print(Update(User).custom_options(check_id).values(name='Column', id=180))
     # print(Update(User).where(id=180).values(id=150, name='NEW_ID'))
     # print(Update(Free).values())
     
     # Select    
     # @custom_option(model=User)
     # def checker(id: int) -> bool:
     #      return id == 523
     
     # @custom_option(model=Item)
     # def checker(id: int, name: str) -> bool:
     #      return name == 'Vlad'
     
     # select = Select(User).where(name='Maks', id=552)
     # print(select.one())
     # select = Select(Item).where(name='Vlad').all()
     # print(select)
     # select = Select(User).custom_options(checker).one()
     # print(select)
     # select = Select(Item).custom_options(checker).one()
     # print(select.id)
     # print(len(Item()))
     # print(len(User()))
     
     # item = Select(Item).where(quality=10).values()
     # if isinstance(item, list):
     #      print(item)
     # else:
     #      print(item.name, item.id)
          
     # user = Select(User).values()
     # print(user)
     
     
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
          # 'id': 'id', 
          # 'name': 'name', 
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
     
     
# Select(User).custom_options(check_id)
# custom_options(*args: Callable)