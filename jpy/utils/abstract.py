
from abc import ABC, abstractmethod



class BaseClass(ABC):

     @property
     @abstractmethod
     def where(self):
          ...
          
          
     @abstractmethod
     def values(self):
          ...