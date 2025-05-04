import json
from core.interfaces import IMenuTemplate


# ConfiguredMenuTemplate, TemplateFactory

class ConfiguredMenuTemplate(IMenuTemplate):
    def __init__(self, config: dict):
        #self.src_sheet   = config["src_sheet"]
        # allow either one range or many
        self.src_ranges  = ([config["src_range"]]
                             if "src_range" in config
                             else config["src_ranges"])
        #self.dest_sheet  = config["dest_sheet"]
        self.dest_ranges = ([config["dest_range"]]
                             if "dest_range" in config
                             else config["dest_ranges"])

    def read_items(self, wb):
        # WE TAKE THE ACTIVE SHEET
        sheet = wb.active
        items = []
        for row in sheet[self.src_ranges]:
            for cell in row:
                if cell.value and len(str(cell.value)) > 2:
                    items.append(str(cell.value).strip())
        return items

    def write_items(self, wb, items):
        # WE TAKE THE ACTIVE SHEET
        sheet = wb.active

        '''
        print(self.dest_ranges)
        for row in sheet[self.dest_ranges]:
            for cell in row:
                cell.value = items.pop(0)
        '''

        cells = [
            cell 
            for row in sheet[self.dest_ranges]
            for cell in row
        ]

        # sanity check
        # we have X menu items per week, we should have 2X menuItems after translation
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
