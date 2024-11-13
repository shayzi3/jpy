



class TableNotExists(Exception):
     def __init__(self, *args: object) -> None:
          super().__init__(*args)
          
          
          
class TableColumnNotExists(Exception):
     def __init__(self, *args: object) -> None:
          super().__init__(*args)
          
          
          
class RequiredArgument(Exception):
     def __init__(self, *args: object) -> None:
          super().__init__(*args)
          


class PrimaryNotExists(Exception):
     def __init__(self, *args: object) -> None:
          super().__init__(*args)
          
          
          
class FileNotValide(Exception):
     def __init__(self, *args: object) -> None:
          super().__init__(*args)
          
          
class TableDontHaveColumns(Exception):
     def __init__(self, *args: object) -> None:
          super().__init__(*args)
          
          
          
class CannotCreateTable(Exception):
     def __init__(self, *args: object) -> None:
          super().__init__(*args)
          
          
class JsonFileEmpty(Exception):
     def __init__(self, *args: object) -> None:
          super().__init__(*args)
          
          
class FileNotFound(Exception):
     def __init__(self, *args: object) -> None:
          super().__init__(*args)
          
          
class NotFoundMetadata(Exception):
     def __init__(self, *args: object) -> None:
          super().__init__(*args)
          
          
class ReturnError(Exception):
     def __init__(self, *args: object) -> None:
          super().__init__(*args)