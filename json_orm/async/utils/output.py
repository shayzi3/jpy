from typing_extensions import Any, TypeVar, Generic



ClassType = TypeVar("T")


class Output(Generic[ClassType]):
     __slots__ = (
          "__table",
          "__data",
     )
     
     def __init__(self, table: ClassType, data: list[dict[str, Any]]) -> None:
          self.__table = table
          
          if not data:
               column = table.__dict__.get('metadata').get('columns')
               data = [{key: None for key in column}]
          self.__data = data
          
     def all(self) -> list[ClassType]:
          return [self.__table(**kwargs) for kwargs in self.__data]
     
     def one(self) -> ClassType:
          return self.__table(**self.__data[0])