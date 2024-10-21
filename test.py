import random

from typing import Any


class Main:
     def __init__(self) -> None:
          self.num = random.randint(1, 100)
     
     
     def __add__(self, obj: int):
          return self.num + obj
          
     
     
     
print(Main() + 5)