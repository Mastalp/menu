from core.interfaces import IExtractor

from dataclasses import dataclass
from typing import Any, Iterable, Literal
from datetime import datetime
from openpyxl import Workbook
import json

MEALS = ['lunch', 'dinner']
LANG = ['fr', 'eng']
FR_TO_ENG_DAYS = {
    "lundi" : "monday",
    "mardi" : "tuesday",
    "mercredi" : "wednesday",
    "jeudi" : "thursday",
    "vendredi" : "friday",
    "samedi" : "saturday",
    "dimanche" : "sunday"
}
ENG_TO_FR_DAYS = {en: fr for fr, en in FR_TO_ENG_DAYS.items()}
FRENCH_DAYS = set(FR_TO_ENG_DAYS.keys())
ENGLISH_DAYS = set(ENG_TO_FR_DAYS.keys())
SOURCE = 'source'
TEMPLATE = 'template'
META_DATA = 'meta_data'
DATE_CELL = 'date_cell'
ENCODING = 'utf-8'

Key = tuple[str, str, tuple[str, ...], str]  # (day, meal, path, lang)

@dataclass
class ExtractedItem:
    day: str
    meal: str
    path: tuple[str, ...]
    cell: str
    lang: str
    menu_item: Any = None

    @property
    def key(self) -> Key:
        return (self.day, self.meal, self.path, self.lang)

# THIS EXTRACTS INFORMATION FROM templates.json FILE STRUCTURE
class Extractor(IExtractor):
    def __init__(self, config: dict):
        self.cfg = config
        self.source = config[SOURCE]
        self.dest = config[TEMPLATE]
        self.src_date_cell = self.source[META_DATA][DATE_CELL]
        self.dest_date_cell = self.dest[META_DATA][DATE_CELL]
    
    def eng_to_french_day(self, day: str):
        return ENG_TO_FR_DAYS[day]
    
    def french_to_eng_day(self, day: str):
        return FR_TO_ENG_DAYS[day]
    
    def get_date_cell(self, mode: str) -> str:
        if mode == SOURCE:
            return self.src_date_cell
        elif mode == TEMPLATE:
            return self.dest_date_cell
        else:
            raise ValueError(f'unknown mode {mode}')
        
    def iter_leaves(self, root: dict, path: tuple[str, ...] = ()) -> Iterable[tuple[tuple[str, ...], Any]]:
        for k, v in root.items():
            if isinstance(v, dict):
                yield from self.iter_leaves(v, path + (k,))
            else:
                yield (path + (k,), v)

    # Extract source data from json file with specific template
    def extract_data(self, mode:str) -> list[ExtractedItem]:
        if mode == SOURCE:
            section = self.source
        elif mode in (TEMPLATE, 'destination', 'dest'):
            section = self.dest
        else:
            raise ValueError(f'Unknown mode: {mode}')

        # json needs columns_eng even if its empty 
        cols: list[str] = [section[META_DATA][f'columns_{lang}'] for lang in LANG]
        extracted_items: list[ExtractedItem] = []
        
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
                            raise ValueError(f"Language not supported (or spelling mistake)")

        return extracted_items


class ExtractorFactory:
    def __init__(self, config_path: str):
        self.configs = json.load(open(config_path, encoding=ENCODING) )

    def get(self, key: str) -> Extractor:
        cfg = self.configs.get(key)
        if not cfg:
            raise ValueError(f"No template named '{key}'")
        
        return Extractor(cfg)