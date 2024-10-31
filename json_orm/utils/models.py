from pydantic import BaseModel


__all__ = (
     "MetaData",
)


class MetaData(BaseModel):
     path: str
     tablename: str | None
     primary: str | None
     free: bool
     columns: list[str]