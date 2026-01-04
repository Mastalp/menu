from core.interfaces import *
from core.date_utils import get_output_filename
from openpyxl import Workbook
import json 


class MenuFiller(IMenuFiller):
    def __init__(self,
                 src_wb : Workbook,
                 dest_wb : Workbook,
                 source: IExtractor,
                 destination: IExtractor,
                 translator: ITranslator,
                 progress_bar: IProgressBar):
        

        self.source : IExtractor = source
        self.destination : IExtractor = destination
        self.source_cells = self.source.extract_data(src_wb)
        self.dest_cells = self.destination.extract_data(dest_wb)

        self.translator = translator
        self.progress_bar = progress_bar




        
    def write_date_cell(self, dest_wb: Workbook, date_obj : datetime) -> None:
        sheet = dest_wb.active
        sheet[self.dest_date_cell].value = date_obj


        
    def run(self) -> str:
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

class MenuFillerFactory:
    def __init__(self, config_path: str):
        self.configs = json.load(open(config_path))

    def get(self, key: str):
        cfg = self.configs.get(key)
        if not cfg:
            raise ValueError(f"No template named '{key}'")
        
        return MenuFiller(cfg)