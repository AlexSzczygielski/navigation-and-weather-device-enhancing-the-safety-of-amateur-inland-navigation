#cv_pipe_status.py
from enum import Enum

class CvPipeStatus(Enum):
    Running = 1
    END = 2
    ERROR = 3