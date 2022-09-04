# menu
menu OMERLO

# menu_auto.py

menu_auto.py est un programme qui produit le fichier excel demandé par OMERLO automatiquement.
Il prend en entrée le fichier excel envoyé par le CSA et retourne le fichier excel
qui va ensuite devoir etre mis dans OMERLO par la personne à la réception.


## Installation ( NO ADMIN ) 

Il faut installer python3 sur l'ordinateur, disponible sur le Microsoft Store.
Pour vérifier l'installation dans powershell : 

```bash
python3 --version
```

Il faut installer le module googletrans version 3.1.0a0 pour python3, le
module openpyxl, et le module datetime
Utilisez le package manager dans powershell : 

```bash
pip install googletrans==3.1.0a0
```

```bash
pip install openpyxl
```

```bash
pip install datetime
```


## Usage ( NO ADMIN )

Les instructions si jointes dans `INSTRUCTIONS_menu_automatique.docx` sont absolument cruciales
et doivent être suivies à la lettre

S'assurer d'avoir dans le répertoire:

	1. menu_auto.py

	2. entrée.xlsx

	3. menu_template.xlsx

( *** LES DOCUMENTS DOIVENT AVOIR LES NOMS EXACTS *** )


Dans la console powershell : 

```bash
python3 menu_auto.py
```

Le menu de la semaine apparaitra dans le répertoire actif.


## Installation ( ADMIN )

Si c'est possible d'etre admin, on peut run menu_auto.exe ! Le programme est
compilé avec PyInstaller et contient tous les modules necessaires.

## Usage ( ADMIN )

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