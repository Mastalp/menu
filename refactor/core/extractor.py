from core.interfaces import IExtractor
from core.date_utils import extract_date
from dataclasses import dataclass
from typing import Any, Iterable, Literal
from datetime import datetime
from openpyxl import Workbook
import json

MEALS = ["lunch", "dinner"]
LANG = ["fr", "eng"]
FRENCH_DAYS = ["lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi", "dimanche"]
ENGLISH_DAYS = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
SOURCE = "source"
TEMPLATE = "template"
META_DATA = "meta_data"
DATE_CELL = "date_cell"
ENCODING = 'utf-8'

Key = tuple[str, str, tuple[str, ...]]  # (day, meal, path)

@dataclass(frozen=True)
class ExtractedItem:
    day: str
    meal : str
    path: tuple[str, ...]
    cell: str
    lang: str
    menu_item: Any = None

    @property
    def key(self) -> Key:
        return (self.day, self.meal, self.path)

# THIS EXTRACTS INFORMATION FROM templates.json FILE STRUCTURE
class Extractor(IExtractor):
    def __init__(self, config: dict):
        self.cfg = config
        self.source = config[SOURCE]
        self.dest = config[TEMPLATE]
        self.src_date_cell = self.source[META_DATA][DATE_CELL]
        self.dest_date_cell = self.dest[META_DATA][DATE_CELL]

    # ---
    def get_source_data(self):
        return self.source

    def get_template_data(self):
        return self.dest
    
    def read_date_cell(self, src_wb: Workbook) -> datetime: 
        return extract_date(src_wb, self.src_date_cell)
    
    # ---
     
    def iter_leaves(self, root: dict, path: tuple[str, ...] = ()) -> Iterable[tuple[tuple[str, ...], Any]]:
        for k, v in root.items():
            if isinstance(v, dict):
                yield from self.iter_leaves(v, path + (k,))
            else:
                yield (path + (k,), v)

    # Extract source data from json file with specific template
    def extract_data(self, mode:str) -> list[ExtractedItem]:
        extracted_items = []

        if mode == SOURCE:
            section = self.source
        elif mode in (TEMPLATE, "destination", "dest"):
            section = self.dest
        else:
            raise ValueError(f"Unknown mode: {mode}")

        cols: list[str] = [section[META_DATA][f"columns_{lang}"] for lang in LANG]
        
        for c in cols:
            for current_day, current_column in c.items():
                for meal_name in MEALS:
                    for path, row in self.iter_leaves(section[meal_name]):
                        cell = f'{current_column}{row}'
                        if current_day in FRENCH_DAYS:
                            data = ExtractedItem(current_day, meal_name, path, cell, LANG[0]) 
                            extracted_items.append(data)
                        elif current_day in ENGLISH_DAYS:
                            data = ExtractedItem(current_day, meal_name, path, cell, LANG[1]) 
                            extracted_items.append(data)
                        else: 
                            raise ValueError(f"Language not supported (or writing mistake)")

        return extracted_items


class ExtractorFactory:
    def __init__(self, config_path: str):
        self.configs = json.load(open(config_path, encoding=ENCODING) )

    def get(self, key: str) -> Extractor:
        cfg = self.configs.get(key)
        if not cfg:
            raise ValueError(f"No template named '{key}'")
        
        return Extractor(cfg)

