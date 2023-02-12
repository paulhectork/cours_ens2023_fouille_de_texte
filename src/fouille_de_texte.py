import plotly  # librairie pour générer des graphiques
import os  # la librairie pour gérer les chemins de fichiers
import re  # librairie pour les expressions régulières (détection de motifs dans le texte)


# *************************************************************
# dans ce script, on analyse les corpus de texte produits 
# avec `api_creation_dataset.py`
#
# crédits: 
# - code: Paul Kervegan, 2023. code sous licence `GNU GPLv3.0`
# - données: Katabase (Alexandre Bartz, Simon Gabay, Matthias 
#   Gille Levenson, Paul Kervegan, Ljudmila Petkovic et Lucie 
#   Rondeau du Noyer). licence `Creative Commons Attribution 
#   4.0 International License`
# *************************************************************


def read_text(genre):
    """
    ici, on ouvre les fichiers en lecture et on en sauvegarde
    le contenu dans une variable, afin de pouvoir traiter et
    manipuler les corpus
    
    :param genre: le genre du corpus, pour ouvrir le bon fichier
    :returns: le corpus associé à ce genre, sous la forme d'une
              chaîne de caractères 
    """
    current_directory = os.path.abspath(os.path.dirname(__file__))  # le chemin du dossier où se trouve le fichier actuel
    in_file = os.path.join(current_directory, os.pardir, "in", f"catalogue_{genre}.txt")  # le chemin du fichier d'entrée

    # `with open() as fh` permet d'ouvrir un fichier. 
    # `mode="r+"` indique ce que l'on veut faire avec ce fichier: 
    # - `r` = read (lire le contenu),
    # - `w` = write (écrire du contenu).
    # - `fh.read()` permet de lire le contenu du fichier `fh` et d'assigner ce contenu à une variable 
    with open(in_file, mode="r+") as fh:
        corpus = fh.read()

    # return permet de retourner une variable: quand une fonction se termine, 
    # toutes les variables créées à l'intérieur de cette fonction sont supprimées,
    # sauf celles qui sont retournées. retourner une variable permet donc d'utiliser
    # cette variable à l'extérieur de la fonction: on prend le resultat de la fonction
    # pour l'utiliser ailleurs.
    return corpus



def structure(corpus):
    """
    ici, on traduit le texte brut (non structuré, donc impossible
    à traiter de façon automatique) en un format structuré: le 
    dictionnaire python (équivalent au `json`).
    
    
    un dictionnaire, c'est quoi?
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    un dictionnaire est un type de données structuré en python
    qui associe une clé à une valeur. il fonctionne de la même
    manière qu'un document papier: la clé est le mot, la valeur 
    sa définition.
    dico = {"clé": "valeur"}.
    
    on accède à une valeur à partir de sa clé: 
    dico["clé"] permet d'accéder à la valeur associée à la clé "clé".
    
    dans un dictionnaire, la clé doit être une chaîne de caractères 
    ou un nombre. la valeur peut prendre n'importe quel type de données:
    liste, dictionnaire, nombre, chaîne de caractères, ce qui permet de
    créer des structures imbriquées et de représenter des objets complexes
    en python.
    
    structure du fichier en entrée
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    ROUSSEAU
    Écrit en 1721-02-11. Vendu en 1878.
    Dimensions: 3.0 pages.  
    L. a. s. à M. d'Argental; Vienne, 11 févr. 1721, 3 p. pl. in-4. Légère déchirure.
    Prix:30.0 FRF (en francs constants 1900: 30.6).
    
    en bref, une entrée a la structure ci-dessous. on a se servir de détection
    de motifs pour extraire les éléments importants de cette structure et les intégrer
    à un json.
    * nom de l'auteur.ice (texte libre)
    * dates d'écriture et de vente au format: "Écrit en {date}. Vendu en {date}". 
    * dimensions au format: "Dimension: {nombre} pages."
    * description en texte libre
    * prix au format: "Prix: {nombre} {monnaie}. (En francs constants 1900: {nombre}).)"
    * ligne vide
    * ligne vide
    
    structure du fichier en sortie
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    :corpus: le contenu du fichier traité, en chaîne de caractères.
    :returns:
    """
    # toutes les entrées du corpus sont séparées par 2 lignes vides, 
    # soit 3 retours à la ligne. 
    # on sépare donc toutes les entrées pour traduire le corpus en une liste
    # d'entrées de catalogue.
    # en python, une ligne vide s'écrit "\n".
    # `.split()` permet de transformer une chaîne de caractères en une liste
    # en indiquant un séparateur (c'est-à-dire, un ou plusieurs caractères qui
    # séparent deux éléments de la liste. le séparateur par défaut est l'espace: " ".
    corpus = corpus.split("\n\n\n")
    
    # à l'aide d'expressions régulières,
    # on filtre la liste pour enlever les entrées vides.
    # pour ce faire, on utilise `re.search("chaîne à rechercher", "chaîne sur laquelle la recherche est faite)` 
    # une entrée vide est une entrée qui ne contient:
    # - soit rien, 
    # - soit des espaces horizontaux (`\s`) une ou plusieurs fois (`*`)
    # - soit des espaces verticaux (`\n`) une ou plusieurs fois (`*`)
    # - entre le début (`^`) et la fin de l'entrée (`$`). 
    # - `(a|b)` est une expression qui correspond à "soit a, soit b".
    corpus = [ entree for entree in corpus if not re.search("^(\n|\s)*$", entree, flags=re.MULTILINE) ]
    
    # à quoi ressemble une entrée, maintenant?
    print(corpus[1])
    
    
    # on traite toutes les entrées du corpus
    for entree in corpus:
        author = re.search("^.+\n", entree, flags=re.MULTILINE)[0]
        
        
    return corpus
    

def analyze():
    """
    ici, on analyse le dictionnaire produit à l'étape précédente
    (à supprimer / remplacer par visualise??)
    """


def visualize():
    """
    ici, on visualise notre corpus afin de voir comment sont représentés
    les 4 genres littéraires dans notre corpus.
    """


def pipeline():
    """
    fonction décrivant le processus global de traitement
    et analyse du texte.
    """
    # lire les fichiers et stocker leur contenu dans une variable
    corpus_idees = read_text("idees")
    corpus_poems = read_text("poeme")
    corpus_roman = read_text("roman")
    corpus_theatre = read_text("theatre")
    
    # transformer les fichiers en documents structurés
    corpus_idees = structure(corpus_idees)
    


if __name__ == "__main__":
    pipeline()
    
    
