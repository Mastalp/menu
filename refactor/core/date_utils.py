from datetime import datetime, date
from openpyxl.utils.datetime import from_excel

FRENCH_MONTHS = [
    "Janvier","Février","Mars","Avril","Mai","Juin",
    "Juillet","Août","Septembre","Octobre","Novembre","Décembre"
]

# failsafe in case the source excel date cell isnt formatted correctly
# handles str/datetime/serial
def parse_menu_date(raw, fmt: str = "%d-%mmmm-%Y") -> datetime:
    if isinstance(raw, datetime):
        return raw
    if isinstance(raw, date):
        # make date into datetime at midnight
        return datetime(raw.year, raw.month, raw.day)
    if isinstance(raw, str):
        return datetime.strptime(raw, fmt)
    # if it’s an Excel serial number
    try:
        return from_excel(raw)
    except Exception:
        raise ValueError(f"Cannot parse date from {raw!r}")

def extract_date(wb, cell: str) -> datetime:
    return wb.active[cell].value

def get_output_filename(date_obj: datetime) -> str:
    french_month = FRENCH_MONTHS[date_obj.month - 1]
    return f"Menu {date_obj.day} {french_month} {date_obj.year}.xlsx"
