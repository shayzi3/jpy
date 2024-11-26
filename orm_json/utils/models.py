from pydantic import BaseModel



class MetaData(BaseModel):
     """
          Metadata for a classes Insert, Select, Update, Delete\n
          Its class check valide data saved in attribute metadata
     """
     primary: str | None
     path: str
     tablename: str
     free: bool
     columns: list[str]