from abc import ABC, abstractmethod
from openpyxl import Workbook
from datetime import datetime


# IMenuTemplate, ITranslator, IProgressBar, IExtractor

    
class IExtractor(ABC):
    @abstractmethod
    def read_date_cell(self, wb: Workbook) -> datetime:
        pass

    @abstractmethod
    def extract_data(self, wb: Workbook) -> list:
        pass

     
class IMenuFiller(ABC):
    @abstractmethod 
    def write_date_cell(self, wb: Workbook, date_obj: datetime) -> None:
        pass

        """
         @abstractmethod
    def write_items(self, wb: Workbook, items: list[str]) -> None:
        pass
        """
   
class IMenuTemplate(ABC):
    pass

class ITranslator(ABC):
    @abstractmethod
    def translate(self, text: str) -> str:
        pass


class IProgressBar(ABC):
    @abstractmethod
    def update(self, current: int, total: int) -> None:
        pass