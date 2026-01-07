from core.interfaces import *
from core.date_utils import get_output_filename
from openpyxl import Workbook
from core.date_utils import extract_date
from core.extractor import ExtractedItem
from typing import Iterable, Any
from core.extractor import Key

SEPARATOR = '+'
LANG_INDEX = 3

class MenuFiller(IMenuFiller):
    def __init__(self,
                 src_wb : Workbook,
                 dest_wb : Workbook,
                 extractor: IExtractor,
                 translator: ITranslator,
                 progress_bar: IProgressBar):
        self.src_wb = src_wb
        self.dest_wb = dest_wb
        self.extractor = extractor
        self.translator = translator
        self.progress_bar = progress_bar
        self.src_sheet = self.src_wb.active
        self.dest_sheet = self.dest_wb.active
        self.source = self.extractor.extract_data('source')
        self.template = self.extractor.extract_data('template')


    def items_to_value_map(self, items: Iterable[ExtractedItem]) -> dict[Key, Any]:
        out: dict[Key, Any] = {}
        for it in items:
            out[it.key] = it.menu_item
        return out
    

    def value_map_to_items(self, value_map: dict[Key, Any], template_items: Iterable[ExtractedItem],) -> list[ExtractedItem]:
        out: list[ExtractedItem] = []

        for it in template_items:
            val = value_map.get(it.key)
            out.append(
                ExtractedItem(
                    day=it.day,
                    meal=it.meal,
                    path=it.path,
                    cell=it.cell,
                    lang=it.lang,
                    menu_item=val,
                )
            )

        return out


    def read_date_cell(self) -> datetime: 
        return extract_date(self.src_wb, self.extractor.get_date_cell('source'))


    def write_date_cell(self, date_obj : datetime) -> None:
        sheet = self.dest_sheet
        sheet[self.extractor.dest_date_cell].value = date_obj


    def read_items(self) -> dict:
        ex_items: list[ExtractedItem] = self.source 
        sheet = self.src_sheet

        for i in ex_items:
            i.menu_item = sheet[i.cell].value

        return self.items_to_value_map(ex_items)


    # src_data needs to be extracted items from template, and the dest_cells should all be empty (=None)
    def write_items(self, src_data: dict):
        sheet = self.dest_sheet

        # if 2 extracted items have the same destination cell, we want to concat with SEPARATOR, not overwrite.
        # So if contents of excel cell isnt empty, add on to it
        for i in src_data:
            cell = sheet[i.cell].value
            if cell != None:
                sheet[i.cell].value = str(sheet[i.cell].value) + f' {SEPARATOR} {i.menu_item}'
            else:
                sheet[i.cell].value = i.menu_item


    def populate_template_items(self, src_data: dict[Key, Any]) -> dict[Key, Any]:
        # template map: all keys that exist in the destination schema
        dest_map: dict[Key, Any] = self.items_to_value_map(self.template)

        items = list(dest_map.keys())
        for i, k in enumerate(items, 1):
            day, meal, path, lang = k

            if lang == "fr":
                dest_map[k] = src_data.get(k)

            elif lang == "eng":
                fr_day = self.extractor.eng_to_french_day(day)  # monday -> lundi
                fr_key: Key = (fr_day, meal, path, "fr")

                fr_val = src_data.get(fr_key)
                # THIS IS THE STEP THAT TAKES TIME 
                dest_map[k] = self.translator.translate(fr_val)
                self.progress_bar.update(i, len(items))
                #dest_map[k] = f"translate this : {fr_val} <--" if fr_val else None

            else:
                raise ValueError(f"Unexpected lang: {lang}")

        return dest_map


    def run(self) -> str:
        # we populate the date cell first
        date_obj = self.read_date_cell()
        self.write_date_cell(date_obj)

        # we then populate the main menu area
        source_items: dict = self.read_items()
        dest_items = self.populate_template_items(source_items)

        l = self.value_map_to_items(dest_items, self.template)
        self.write_items(l)

        return get_output_filename(date_obj)