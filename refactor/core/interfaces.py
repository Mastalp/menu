from abc import ABC, abstractmethod
from openpyxl import Workbook
from datetime import datetime


# IMenuTemplate, ITranslator, IProgressBar, IExtractor

    
class IExtractor(ABC):
    @abstractmethod
    def extract_data(self, mode: str) -> list:
        pass

     
class IMenuFiller(ABC):
    @abstractmethod 
    def write_date_cell(self, wb: Workbook, date_obj: datetime) -> None:
        pass

    @abstractmethod
    def read_items(self):
        pass
        
    @abstractmethod
    def write_items(self, src_wb: Workbook, dest_wb: Workbook, src_data: list, dest_data = list):
        pass
        
   
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