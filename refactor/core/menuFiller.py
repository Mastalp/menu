from core.interfaces import *


class MenuFiller:
    def __init__(self, template: IMenuTemplate,
                 translator: ITranslator,
                 progress_bar: IProgressBar):
        self.template = template
        self.translator = translator
        self.progress_bar = progress_bar

    def run(self, src_wb, dest_wb):
        items = self.template.read_items(src_wb)
        translated = []
        for i, item in enumerate(items, 1):
            translated.append(item)
            translated.append(self.translator.translate(item))
            self.progress_bar.update(i, len(items))
        self.template.write_items(dest_wb, translated)
