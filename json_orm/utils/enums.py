from enum import Enum, auto


__all__ = (
     "Mode",
)


class Mode(Enum):
     SELECT = auto()
     INSERT = auto()
     UPDATE = auto()
     DELETE = auto()