from enum import Enum


class SourceType(Enum):
    Tail = "tail"
    DockerLogs = "dockerlogs"
