# INTRODUCTION À LA FOUILLE DE TEXTE AVEC PYTHON (École normale supérieure ULM, 20 février 2023)

Ce cours fait partie du cours d'[*Introduction générale aux humanités numériques*](https://odhn.ens.psl.eu/article/introduction-generale-aux-humanites-numeriques) (ENS ULM, 2022-2023, responsable pédagogique Léa Saint-Raymond). 
Il vise à introduire aux possibilités d'extraction d'informations et d'analyse statistique depuis
un corpus de texte brut, en Python. 

--- 

## PRÉSENTATION

### Question de recherche
Quelle est la représentation de cinq genres littéraires du XVIIIe siècle
(poésie, théâtre, roman, littérature d'idées) dans un corpus datant du XIXe siècle de catalogues de 
vente de manuscrits ?

### Prérequis techniques

Aucun (c'est pratique!)

### Compétences vues pendant ce cours

- manipulation de fichiers: lecture, écriture
- analyse de texte: structuration et détection de motifs dans du texte brut
- manipulation des formats de base de Python: chaînes de caractères (`string`),
  nombres (entiers `int`, décimaux `float`), listes (`list`), dictionnaires (`dict`).
- expressions régulières (`regex`, pour les intimes) utilisées pour la détection de 
  motifs dans le texte (introduction)
- visualisation de données avec [Plotly](https://plotly.com/python/)
- *bonus*: utilisation d'APIs pour la récupération de données brutes sur le Web, 
  introduction aux principes de fonctionnement des API (introduction)

---

## UTILISATION

### En local

Si on ne veut pas / peut pas utiliser `Google Colab`, c'est tout aussi simple dans
un terminal. 

#### Installation de Git

On aura besoin de Git pour télécharger le code. Git doit peut-être installé.

```bash
brew install git      # si on a MacOS
sudo apt install git  # si on a linux (distribution Debian / Ubuntu)
winget install --id Git.Git -e --source winget  # si on a windows.
```

**Si vous utilisez Windows** mais que vous n'avez pas winget, vous pouvez soit
passer par un gestionnaire de fichiers/d'applications plutôt que par un terminal,
sinon on installe Winget via (ce lien)[https://docs.microsoft.com/en-us/windows/package-manager/winget].

#### Installation en local

```bash
git clone https://github.com/paulhectork/cours_ens2023_fouille_de_texte.git  # cloner le dépôt git
cd cours_ens2023_fouille_de_texte.git  # se déplacer dans le dossier.

# créer un environnement virtuel 
python3 -m venv env # sur macOS/linux
c:\>python3 -m venv .\env # sur windows

# sourcer l'environnement
source env/bin/activate  # linux/macOS
env\Scripts\activate.bat # sur Windows. si ca ne marche pas, essayer: `env\Scripts\Activate.ps1` 

# installer les dépendances
pip install -r requirements.txt
```

#### Utilisation

**Si on veut lancer le code directement**, sans passer par un notebook, en étant à la racine
du dossier `cours_ens2023_fouille_de_texte`:

``bash
# sourcer l'environnement virtuel
source env/bin/activate   # linux/macOS
env\Scripts\activate.bat  # windows. commande alternative: `env\Scripts\Activate.ps1`

# créer le corpus initial en requêtant une API (optionnel)
python src/creation_corpus.py  # linux/macOS
python src\creation_corpus.py  # windows

# analyser le texte et produire des visualisations
python src/fouille_texte.py    # linux/macOS
python src\fouille_texte.py    # linux/macOS
```

**Si on veut utiliser les notebooks jupyter**

```bash
# sourcer l'environnement virtuel
source env/bin/activate   # linux/macOS
env\Scripts\activate.bat  # windows. commande alternative: `env\Scripts\Activate.ps1`

jupyter notebook
```

---

## CRÉDITS

Code et notebooks: Paul, Hector Kervegan. Licence ouverte [GNU GPL 3.0](./LICENSE)

Données: [Katabase](https://katabase.huma-num.fr/). Données produites par Alexandre Bartz, 
Simon Gabay, Matthias Gille Levenson, Paul Kervegan, Ljudmila Petkovic et Lucie Rondeau du Noyer
et disponibles sous licence ouverte [Creative Commons Attribution 2.0](./LICENSE_DONNEES).


