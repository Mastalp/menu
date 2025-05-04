from abc import ABC, abstractmethod
from openpyxl import Workbook
import sys

# IMenuTemplate, ITranslator, IProgressBar

class IMenuTemplate(ABC):
    @abstractmethod
    def read_items(self, wb: Workbook) -> list[str]:
        """Extract raw menu strings from the source sheet."""
        pass

    @abstractmethod
    def write_items(self, wb: Workbook, items: list[str]) -> None:
        """Populate the target sheet(s) with translated/final items."""
        pass


class ITranslator(ABC):
    @abstractmethod
    def translate(self, text: str) -> str:
        """Translate a single string into the target language."""
        pass


class IProgressBar(ABC):
    @abstractmethod
    def update(self, current: int, total: int) -> None:
        """Update the progress indicator to current/total."""
        pass