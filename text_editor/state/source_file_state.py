from enum import Enum


class SourceFileState(Enum):
    NEW = 0
    NEVER_SAVED = 1
    SAVED = 2
