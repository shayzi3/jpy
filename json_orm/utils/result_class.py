from typing_extensions import Any, TypeVar, Generic



__all__ = (
     "Output",
)
T = TypeVar("T")


class Output(Generic[T]):
     __slots__ = (
          "__table",
          "__data",
     )
     
     def __init__(
          self, 
          table: T, 
          data: list[dict[str, Any]],
     ) -> None:
          self.__table = table
          
          if not data:
               column = table.__dict__.get('metadata').get('columns')
               data = [{key: None for key in column}]
          self.__data = data
          
     def all(self) -> list[T]:
          return [self.__table(**kwargs) for kwargs in self.__data]
     
     def one(self) -> T:
          return self.__table(**self.__data[0])