from googletrans import Translator as GT
from core.interfaces import ITranslator

class GoogleTranslator(ITranslator):
    def __init__(self):
        self._svc = GT() 

    def translate(self, text: str) -> str:
        return self._svc.translate(text, dest="en").text