
from jpy import JsonPy


# Create tables
class User:
     __tablename__ = 'users' # Its not required attribute. If dont wrote __tablename__ that your table take name a class
     
     id: int
     username: str
     password: str
     
     
     
class Car:     
     id: int
     name: str
     owner_id: int
     

# If you want create just {key: value}. U can make class like this ↓
class FreeArguments:
     money: int
     level: int
     docs: str
     
     
# Also if you dont wanna create class, you can make this 
# JsonPy(free_arguments = ['money', 'level', 'docs'])
     
     
json_py = JsonPy(
     User,
     Car,
     free_arguments=FreeArguments,
     # free_arguments = ['money', 'level', 'docs']
)
json_py.create()


# After this code in json file will ↓
# {
#     "users": {
#         "__types": [
#             "id",
#             "username",
#             "password"
#         ],
#         "data": []
#     },
#     "Car": {
#         "__types": [
#             "id",
#             "name",
#             "owner_id"
#         ],
#         "data": []
#     },
#     "__free": {
#         "money": null,
#         "level": null,
#         "docs": null
#     }
# }

# '__types' its key for jpy