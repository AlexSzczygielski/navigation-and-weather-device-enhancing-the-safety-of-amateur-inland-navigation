#cv_state.py
#This class serves as a state for cv_service
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from cv.cv_service import CvService

class CvState(ABC):
    @property
    def context(self) -> "CvService":
        return self._context
    
    @context.setter
    def context(self, context: "CvService") -> None:
        self._context = context

    @abstractmethod
    def get_vid_source(self) -> str:
        pass
    
    @abstractmethod
    def setup_vid_stream(self) -> None:
        pass
    
    @abstractmethod
    def fetch_image(self) -> None:
        pass
        
    @abstractmethod
    def fetch_frame(self) -> None:
        pass