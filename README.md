# menu_auto.py

menu_auto.py est un programme qui produit le fichier excel demandé par OMERLO automatiquement.
Il prend en entrée le fichier excel envoyé par le CSA et retourne le fichier excel
qui va ensuite devoir etre mis dans OMERLO par la personne à la réception.


## Installation 

Il faut installer python3 sur l'ordinateur, disponible sur le Microsoft Store.
Pour vérifier l'installation dans powershell : 

```bash
python3 --version
```

Il faut installer le module googletrans version 3.1.0a0 pour python3, le
module openpyxl, et le module datetime
Utilisez le package manager dans powershell : 

Sert à interragir avec les fichiers EXCEL (.xlsx)

```bash
pip install openpyxl
```

Sert à traduire tous les items du menu en anglais. *** VERSION 3.1.0a0 ***

```bash
pip install googletrans==3.1.0a0
```

Sert à introduire la date dans template.xlsx - La cellule qui contient la date
dans entrée.xlsx doit être formatée comme "TEXTE" pour que la fonction strptime() fonctionne. 
https://www.programiz.com/python-programming/datetime/strptime

```bash
pip install datetime
```

Pour construire l'application, nous aurons besoin de pyinstaller:

```bash
pip install pyinstaller
```

On 'build' le .exe avec la commande suivante:

```bash
python -m PyInstaller --onefile menu_auto.py
```

Le fichier `dist` produit par cette commande devient le repertoire actif pour le programme
On peut le renommer à `MENU_AUTO`
Y placer entrée.xlsx et menu_template.xlsx, puis éxécuter MENU_AUTO.exe

## Usage

Les instructions si jointes dans `INSTRUCTIONS_menu_automatique.docx` sont absolument cruciales
et doivent être suivies à la lettre

S'assurer d'avoir dans le répertoire:

	1. menu_auto.exe

	2. entrée.xlsx

	3. menu_template.xlsx

( *** LES DOCUMENTS DOIVENT AVOIR LES NOMS EXACTS *** )
 

Double-cliquer le programme menu_auto.exe

( *** IL FAUT ÉXÉCUTER CE PROGRAMME EN TANT QU'ADMINISTRATEUR *** )

Le menu de la semaine apparaitra dans le répertoire actif.


## Erreurs

1. `ERREUR ! Il y a un problème dans {src_excel_doc} ! REVOIR LE FORMATAGE!`

Il faut s'assurer que le document excel soit conforme au formatage nécéssaire pour le programme.

2. `ERREUR ! Il y a des cases vides dans {src_excel_doc}`

Le document entrée.xlsx ne peut pas contenir de cellules vides.

3. `ERREUR ! Le fichier {src_excel_doc/dest_excel_doc} n'est pas dans le répertoire!`

Les documents ne sont pas nommés de la bonne manière. S'assurer que les noms soient exacts!

4. `ERREUR ! La date est incorrecte dans {src_excel_doc}!`

La cellule excel 'A2' dans le fichier excel source 'entrée.xlsx' doit 
être ***formattée*** comme *** TEXTE *** pour que datetime.strptime() fonctionne