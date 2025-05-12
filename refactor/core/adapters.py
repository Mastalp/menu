from core.interfaces import ITranslator, IProgressBar
from googletrans import Translator as GT


# adapter for the google translator package
class GoogleTranslator(ITranslator):
    def __init__(self):
        self._svc = GT() 

    def translate(self, text: str) -> str:
        return self._svc.translate(text, dest="en").text


# We use this class to adapt a ttk.Progressbar widget to the IProgressBar interface in app.py 
class TkProgressBar(IProgressBar):
    def __init__(self, progress_widget):
        self._progress = progress_widget

    def update(self, current, total):
        # Advance by one step; ttk.Progressbar handles the max internally
        self._progress.step(1)