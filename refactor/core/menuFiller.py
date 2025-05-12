from core.interfaces import *
from core.date_utils import get_output_filename
from openpyxl import Workbook


class MenuFiller:
    def __init__(self, template: IMenuTemplate,
                 translator: ITranslator,
                 progress_bar: IProgressBar):
        self.template = template
        self.translator = translator
        self.progress_bar = progress_bar
        
    def run(self, src_wb: Workbook, dest_wb: Workbook) -> str:
        # we populate the date cell first
        date_obj = self.template.read_date_cell(src_wb)
        self.template.write_date_cell(dest_wb, date_obj)

        # we then populate the main menu area
        items = self.template.read_items(src_wb)
        translated = []
        # heuristique
        for i, item in enumerate(items, 1):
            translated.append(item)
            translated.append(self.translator.translate(item))
            self.progress_bar.update(i, len(items))
        self.template.write_items(dest_wb, translated)

        # return the formatted name 
        return get_output_filename(date_obj)
