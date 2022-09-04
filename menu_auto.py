# menu 2.0 using openpyxl instead of csv
from googletrans import Translator
from openpyxl import load_workbook
from datetime import datetime
import time
import sys

translator = Translator()

# FUNCTIONS

# returns translated menu_item with googletrans
def menu_translate(menu_item):
    global progress
    progress += 1
    return (translator.translate(menu_item, dest='en')).text
    
# prints a progress bar
def progress_bar(progress, total):
    percent = 100 * (progress / float(total))
    bar = '█' * int(percent) + '-' * (100 - int(percent))
    print(f"\r|{bar}| {percent:.2f}%", end="\r")

# returns doc name from date object
def save_as_name(date_object):
    months = ['Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin', 
    'Juillet', 'Août', 'Septembre', 'Octobre', 'Novembre', 'Décembre']
    name = 'Menu ' + str(date_object.day) + ' ' + \
    str(months[int(date_object.month) - 1]) + ' ' + \
        str(date_object.year) + '.xlsx'
    return name

# looping thru tuples, GETTING and SETTING values using menu list
def menu_auto(src_cells, dest_cells):
    menu = [] # will contain 140 items to be placed in template

    # READ, looping thru src cell tuples, getting and translating cell values
    for row in src_cells:
        for i in range(len(row)):
            if row[i].value != None and len(row[i].value) > 2: # != et, ou
                menu_item_f = (row[i].value).strip().capitalize()
                menu.append(menu_item_f)
                menu_item_f_t = menu_translate(menu_item_f)
                menu.append(menu_item_f_t)
                progress_bar(progress, total)

    # WRITE, looping thru dest cell tuples, setting values
    for row in dest_cells:
        for i in range(len(row)):
            row[i].value = menu[0] # item at index 0
            menu.pop(0) # popping the stack of delicious items

def error_handler():
    time.sleep(1)
    print("CETTE FENÊTRE SE FERMERA AUTOMATIQUEMENT")
    time.sleep(5)
    sys.exit(1)


# MAIN

# get input for src name ? *** TO DO ***
src_excel_doc = 'entrée.xlsx'

# src for save as
dest_excel_doc = 'menu_template.xlsx'

# loading excel docs with openpyxl w/ error handling
try:
    src_doc = load_workbook(src_excel_doc)
    src_feuille = src_doc.active
except:
    print("ERREUR ! Le fichier " + src_excel_doc + \
        " n'est pas dans le répertoire!")
    error_handler()
try:
    dest_doc = load_workbook(dest_excel_doc)
    dest_feuille = dest_doc.active
except:
    print("ERREUR ! Le fichier " + dest_excel_doc + \
        " n'est pas dans le répertoire!")
    error_handler()

# DATE using datetime w/ error handling
try:
    date_cell = dest_feuille['A1']
    date_object = datetime.strptime(src_feuille['A2'].value, "%d-%m-%Y")
    date_cell.value = date_object
except:
    print("ERREUR ! La date est incorrecte dans " + src_excel_doc + " !")
    error_handler()

# NAME using save_as_name func and date_object
document_name = save_as_name(date_object)

# SRC and DEST cell tuples from openpyxl ranges
src_cells = src_feuille['B4':'H20']
dest_cells = dest_feuille['F4':'S13']

print("MENU_AUTOMATIQUE POUR OMERLO V 2.0 par LPRL")
time.sleep(2)
print("LE PROGRAMME VA COMMENCER...")
time.sleep(1)

# vars for progress bar
progress, total = 0, 70 # items to be translated (10/j, 7j)

# CALLING MAIN FUNC ***
menu_auto(src_cells, dest_cells)

# SAVING DOC AS using save_as_name function
dest_doc.save(document_name)

print('\r') # print under progress bar
print("TRAVAIL TERMINÉ")
time.sleep(1)
print(f"LE MENU '{document_name}' EST MAINTENANT DANS LE RÉPERTOIRE ACTIF")
time.sleep(2)
print("CETTE FENÊTRE SE FERMERA AUTOMATIQUEMENT")
time.sleep(5)