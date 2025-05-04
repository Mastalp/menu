import threading
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
from openpyxl import load_workbook

from core import *

class TkProgressBar:
    """
    Adapts a ttk.Progressbar widget to the IProgressBar interface.
    """
    def __init__(self, progress_widget):
        self._progress = progress_widget

    def update(self, current, total):
        # Advance by one step; ttk.Progressbar handles the max internally
        self._progress.step(1)

class MenuAutoApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Menu Auto 3.0")
        self.geometry("600x250")

        # — Source file picker —
        tk.Label(self, text="Weekly menu source:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.src_path = tk.StringVar()
        tk.Entry(self, textvariable=self.src_path, width=40).grid(row=0, column=1, padx=5)
        tk.Button(self, text="Browse…", command=self.browse_src).grid(row=0, column=2)

        # — Template file picker —
        tk.Label(self, text="Template workbook:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.tpl_path = tk.StringVar()
        tk.Entry(self, textvariable=self.tpl_path, width=40).grid(row=1, column=1, padx=5)
        tk.Button(self, text="Browse…", command=self.browse_tpl).grid(row=1, column=2)

        # — Template selector —
        tk.Label(self, text="Mode:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.template_var = tk.StringVar(value="legacy")
        with open("templates.json") as f:
            choices = list(json.load(f).keys())
        tk.OptionMenu(self, self.template_var, *choices).grid(row=2, column=1, sticky="w")

        # — Progress bar —
        self.progress = ttk.Progressbar(self, orient='horizontal', length=500, mode='determinate')
        self.progress.grid(row=3, column=0, columnspan=3, pady=10)

        # — Generate button —
        self.generate_btn = tk.Button(self, text="Generate Menu", command=self.on_generate)
        self.generate_btn.grid(row=4, column=1, pady=10)

    def browse_src(self):
        path = filedialog.askopenfilename(filetypes=[("Excel","*.xlsx")])
        if path:
            self.src_path.set(path)

    def browse_tpl(self):
        path = filedialog.askopenfilename(filetypes=[("Excel","*.xlsx")])
        if path:
            self.tpl_path.set(path)

    def on_generate(self):
        # Disable button to prevent re-entry
        self.generate_btn.config(state='disabled')

        # Prepare template and determine total items
        factory = TemplateFactory("templates.json")
        template = factory.get(self.template_var.get())
        src_wb = load_workbook(self.src_path.get())
        total = len(template.read_items(src_wb))
        self.progress['value'] = 0
        self.progress['maximum'] = total

        # Start translation/write in background thread
        worker = threading.Thread(target=self._worker, args=(template,), daemon=True)
        worker.start()

    def _worker(self, template):
        try:
            src_wb = load_workbook(self.src_path.get())
            tpl_wb = load_workbook(self.tpl_path.get())

            filler = MenuFiller(
                template,
                GoogleTranslator(),
                TkProgressBar(self.progress)
            )

            # Execute the fill process
            filler.run(src_wb, tpl_wb)

            # Save result
            out_name = "output.xlsx" #tpl_wb.active['A1'].value or "output.xlsx"
            tpl_wb.save(out_name)

            self.after(0, lambda: messagebox.showinfo("✅ Success", f"Saved: {out_name}"))
        except Exception as e:
            self.after(0, lambda err=e: messagebox.showerror("❌ Error", str(err)))
        finally:
            # Re-enable the generate button
            self.after(0, lambda: self.generate_btn.config(state='normal'))

if __name__ == "__main__":
    app = MenuAutoApp()
    app.mainloop()
