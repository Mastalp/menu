import json
from core.interfaces import IMenuTemplate
from core.date_utils import extract_date
from datetime import datetime
from openpyxl import Workbook

# ConfiguredMenuTemplate, TemplateFactory

class ConfiguredMenuTemplate(IMenuTemplate):
    def __init__(self, config: dict):
        self.src_range  = config["src_range"]
        self.dest_range = config["dest_range"]
        self.src_date_cell = config["src_date_cell"]
        self.dest_date_cell = config["dest_date_cell"]    

    def read_date_cell(self, src_wb: Workbook) -> datetime: 
        return extract_date(src_wb, self.src_date_cell)
    
    def write_date_cell(self, dest_wb: Workbook, date_obj : datetime) -> None:
        sheet = dest_wb.active
        sheet[self.dest_date_cell].value = date_obj

    def read_items(self, wb: Workbook) -> list[str]:
        # WE TAKE THE ACTIVE SHEET
        sheet = wb.active
        items = []
        for row in sheet[self.src_range]:
            for cell in row:
                if cell.value and len(str(cell.value)) > 2:
                    items.append(str(cell.value).strip())
        return items

    def write_items(self, wb: Workbook, items: list[str]) -> None:
        # WE TAKE THE ACTIVE SHEET
        sheet = wb.active

        cells = [
            cell 
            for row in sheet[self.dest_range]
            for cell in row
        ]

        # sanity check
        if (len(items) != len(cells)): 
            raise ValueError(
                f"Template expects {len(cells)} values, ", 
                f"but got {len(items)} items to write"
            )
        
        for cell, value in zip(cells, items): 
            cell.value = value


class TemplateFactory:
    def __init__(self, config_path: str):
        self.configs = json.load(open(config_path))

    def get(self, key: str) -> IMenuTemplate:
        cfg = self.configs.get(key)
        if not cfg:
            raise ValueError(f"No template named '{key}'")
        return ConfiguredMenuTemplate(cfg)
