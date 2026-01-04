from core.interfaces import IExtractor
from core.date_utils import extract_date
from dataclasses import dataclass
from typing import Any, Iterable
from datetime import datetime
from openpyxl import Workbook
import json


@dataclass(frozen=True)
class ExtractedItem:
    day: str
    meal: str
    path: tuple[str, ...]
    src_cell: str
    value: Any


class Extractor(IExtractor):
    def __init__(self, config: dict):
        self.src_date_cell = config["meta_data"]["date_cell"]
        self.columns = config["meta_data"]["columns"]
        self.lunch = config["lunch"]
        self.dinner = config["dinner"]

    def read_date_cell(self, src_wb: Workbook) -> datetime: 
        return extract_date(src_wb, self.src_date_cell)
     
    def iter_leaves(self, root: dict, path: tuple[str, ...] = ()) -> Iterable[tuple[tuple[str, ...], Any]]:
        for k, v in root.items():
            if isinstance(v, dict):
                yield from self.iter_leaves(v, path + (k,))
            else:
                yield (path + (k,), v)

    def extract_data(self, wb: Workbook) -> list[ExtractedItem]:
        l, d = self.lunch, self.dinner
        sheet = wb.active
        extracted_items = []

        for i in self.columns.keys():
            current_day = i
            current_column = self.columns[current_day]

            # LUNCH
            for path, row in self.iter_leaves(l):
                cell = f'{current_column}{row}'
                menu_item = sheet[cell].value
                data = ExtractedItem(current_day, "lunch", path, cell, menu_item) 
                extracted_items.append(data)

            # DINER
            for path, row in self.iter_leaves(d):
                cell = f'{current_column}{row}'
                menu_item = sheet[cell].value
                data = ExtractedItem(current_day, "dinner", path, cell, menu_item) 
                extracted_items.append(data)

        return extracted_items


class ExtractorFactory:
    def __init__(self, config_path: str):
        self.configs = json.load(open(config_path))

    def get(self, key: str) -> Extractor:
        cfg = self.configs.get(key)
        if not cfg:
            raise ValueError(f"No template named '{key}'")
        
        return Extractor(cfg)

