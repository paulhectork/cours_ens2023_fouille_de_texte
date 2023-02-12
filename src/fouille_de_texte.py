from statistics import median  # fonction pour calculer une valeur médiane
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
    à traiter de façon automatique) en un format structuré: une liste
    de dictionnaires python.
    
    
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
    
    structure d'une entrée en entrée
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    ROUSSEAU
    Écrit en 1721-02-11. Vendu en 1878.
    Dimensions: 3.0 pages.  
    L. a. s. à M. d'Argental; Vienne, 11 févr. 1721, 3 p. pl. in-4. Légère déchirure.
    Prix: 30.0 FRF (en francs constants 1900: 30.6).
    
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
    
    structure du corpus en sortie
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    [
        {
            "auteur": "",
            "date_creation": "1763",
            "date_vente": "1879",
            "prix": "",
            "prix_constant": "",
            "monnaie": "",
            "description": " L. s., écrite par Wagnière; Ferney, 15 sept. 1763, 1 p. 1/2 in-4. "
        },
        # entrées suivantes
    ]
    
    :corpus: le contenu du fichier traité, en chaîne de caractères.
    :returns: le corpus structuré sous forme de liste de dictionnaires
    """
    corpus_structure = []  # le résultat de sortie
    
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
    # print(corpus[1])
    
    
    # on traite toutes les entrées du corpus
    for entree in corpus:
        # on initie les variables pour lesquelles on recherchera des informations
        # on ne retient pas les dimensions, qui ne seront pas utilisées plus tard
        auteur = ""
        date_creation = ""
        date_vente = ""
        prix = ""
        monnaie = ""
        prix_constant = ""
        description = ""
        
        
        # on extrait la première ligne: l'auteur.
        auteur = entree.split("\n")[0]
        
        # ensuite, la date de vente
        if re.search("Écrit en (\d{4})", entree):
            # - `\d{4}` permet de cibler une date au format `AAAA`: `\d{4}` permet de cibler 
            #   4 chiffres à la suite, soit l'année
            # - on récupère l'élément à l'index 1 renvoyé par `re.search()`: `re.search()[1]`:
            #   - le premier élément que renvoie cette fonction (récupéré avec `re.search()[0]`) 
            #     est l'intégralité du motif détecté ( "Écrit en AAAA")
            #   - le second élément correspond au premier sous-groupe du motif. les expressions
            #     régulières permettent de définir des sous-groupes, c'est-à-dire des sous-motifs
            #     à l'intérieur de l'expression régulière. un sous motif est indiqué par la 
            #     présence de "()". il permet de détecter et d'extraire une partie seulement 
            #     d'un motif dans une chaînes de caractères. ici, on repère "Écrit en AAAA",
            #     mais on extrait seulement "\d{4}", soit le premier sous-groupe de l'expression.
            # `int()` permet de convertir une chaîne de caractères en nombre entier
            date_creation = int(re.search("Écrit en (\d{4})", entree)[1])
        
        # de même pour la date de vente: on recupère le première série de 4 chiffres.
        if re.search("Vendu en (\d{4})", entree):
            date_vente = int(re.search("Vendu en (\d{4})", entree)[1])
        
        # on récupère ensuite la description, soit la 3e ligne de chaque entrée
        description = entree.split("\n")[3]
        
        # ensuite, on s'occupe du prix et de la monnaie
        if re.search("Prix: (\d+\.?\d*) ([A-Z]+)", entree):
            # décomposons cette expression régulière:
            # - elle permet de cibler: "Prix: 30 FRF", "Prix: 30.05 FRF"...
            # - ici, il y a deux sous-groupes qui correspondent au prix 
            #   et à la monnaie dans laquelle ce prix est exprimé:
            #   - `\d+\.?\d*`: permet de cibler un nombre entier ou à virgule.
            #     - `\d+`: un ou plusieurs chiffres
            #     - `\.?`: "\." permet de cibler un point ("."); "?" indique qu'il 
            #       faut cibler ce point 0 ou 1 fois.
            #     - `\d*`: entre 0 et plusieurs chiffres
            #   - `[A-Z]+`: permet de cibler une ou plusieurs fois une lettre capitale.
            #     - `[A-Z]`: les crochets "[]" permettent d'indiquer qu'il faut cibler un 
            #       caractère parmi une liste de caractères fournie entre crochets. séparer 
            #       2 caractères par un "-" indique que ces deux caractères sont des bornes 
            #       et qu'il faut cibler tous les caractères entre ces bornes: 
            #       [A-Z] cible donc tous les caractères en majuscules
            #     - `+` indique qu'il faut cibler le caractère précédent une ou plusieurs fois.
            prix = float(re.search("Prix: (\d+\.?\d*) ([A-Z]+)", entree)[1])  # le prix correspond au le 1er sous-groupe. on le convertit en nombre à virgule avec `float()`
            monnaie = re.search("Prix: (\d+\.?\d*) ([A-Z]+)", entree)[2]      # la monnaie correspond au 2nd sous-groupe
            
        # enfin, on cible le prix constant, exprimé en francs 1900.
        if re.search("en francs constants 1900: (\d+\.?\d*)", entree):
            # ici, la logique est la même qu'au dessus: on cible un nombre entier
            # ou un nombre à virgule (`\d+\.?\d*`) dans un sous-groupe et on l'extrait. 
            # on convertit le prix en nombre à virgule.
            prix_constant = float(re.search("en francs constants 1900: (\d+\.?\d*)", entree)[1])
            
        # pour finir, on exprime l'entrée sous la forme d'un dicitonnaire et on ajoute
        # cette entrée à notre variable `out`, qui stocke le corpus structuré.
        entree = {
            "auteur": auteur,
            "date_creation": date_creation,
            "date_vente": date_vente,
            "prix": prix,
            "prix_constant": prix_constant,
            "monnaie": monnaie,
            "description": description
        }
        corpus_structure.append(entree)
        
    return corpus_structure
    

def analyze():
    """
    ici, on analyse le dictionnaire produit à l'étape précédente
    (à supprimer / remplacer par visualise??)
    """


def axes(corpus):
    """
    à partir d'un corpus, générer des données pour les absisses et ordonnées
    de nos graphiques.
    
    quelles données sont récupérées?
    - en absisse (variable `y`, les années de vente).
    - en ordonnées, 
      - `y_count`: le nombre d'items vendus pour ce corpus et pour cette 
        années
      - `y_prix`: le prix médian d'une entrée pour ce corpus, sur un an.
        on commence par créer une liste de tous les prix de vente pour 
        ce corpus et cette année dans `y_prix`. à partir de cette liste,
        on calculera le prix médian de vente.
    
    on commence par exprimer les ordonnées en dictionnaires qui
    associent à chaque année les données pertinentes, pour pouvoir
    garder le lien entre données en abscisse et données en ordonnée

    :param corpus: le corpus traité
    :returns: 
              - `x`: l'axe des abscisses, sous la forme d'une liste de dates
              - `y_prix`: un dictionnaire associant à chaque année un prix médian 
                de vente, en francs 1900
              - `y_count`: le nombre d'items mis en vente par an pour ce corpus
    """
    x = []        # années de vente
    y_prix = {}   # prix  par an
    y_count = {}  # nombre d'items vendus par an
    
    annees = [ entree["date_vente"] for entree in corpus ]  # liste d'années.
    # on crée x: une liste avec toutes les années entre la vente la plus ancienne 
    # et la plus récente.
    for i in range(min(annees), max(annees) + 1):
        x.append(i)
    
    # ensuite, on crée les bases pour `y_prix` et `y_count`: on crée dans
    # chaque dictionnaire une entrée pour chaque année
    y_prix = { annee: [] for annee in x }  # on associe à chaque année une liste vide: on y ajoutera tous les prix de vente
    y_count = { annee: 0 for annee in x }  # on associe à chaque année un 0. on comptera toutes les ventes pour cette année
    
    
    # on itère sur chaque entrée
    for entree in corpus:
        date = entree["date_vente"]
        
        # on ajoute le prix constant à `y_prix`
        if entree["prix_constant"] != "":
            y_prix[date].append(entree["prix_constant"])
        
        # on augmente le compteur de ventes par an de 1 dans `y_count`
        y_count[date] += 1
    
    # enfin, on calcule le prix de vente médian pour une année dans `y_prix`:
    for key, value in y_prix.items():
        if len(value) > 0:
            y_prix[key] = median(value)  # si il y a des prix pour cette année, remplacer la liste de prix par le prix médian
    
    return x, y_prix, y_count



def visualize(corpus_idees, corpus_poeme, corpus_roman, corpus_theatre):
    """
    ici, on visualise notre corpus afin de voir comment sont représentés
    les 4 genres littéraires dans notre corpus.
    
    plotly et les graphiques en python
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    les visualisations de graphiques sont faites avec la librairie Plotly,
    concurrente de Matplotlib. Matplotlib est surtout orientée pour générer
    des images, alors que Plotly est pensée pour les navigateurs: elle permet
    de faire des graphiques interactifs. le principe d'un graphique 
    bidimensionnel avec plotly est relativement simple:
    - un graphique est créé par une fonction
    - cette fonction prend au moins 2 arguments: des données pour l'axe des
      abscisses (x), et des données pour l'axe des ordonnées (y). il faut
      donc donner à plotly 2 listes de données.
    - ensuite, il y a énormément de possibilités de personnalisation
    
    :param: en paramètre, tous les corpus exprimés en formats structurés.
    :returns: rien.
    """
    # on prépare les données: 
    # en `x`, on utilisera les années de vente
    # en `y`, 
    # - le nombre d'items mis en vente par corpus
    # - le prix médian de chaque item mis en vente par corpus
    x_idees, y_prix_idees, y_count_idees = axes(corpus_idees)
    x_poeme, y_prix_poeme, y_count_poeme = axes(corpus_poeme)
    x_roman, y_prix_roman, y_count_roman = axes(corpus_roman)
    x_theatre, y_prix_theatre, y_count_theatre = axes(corpus_theatre)
    
    # on crée un `x` pour tous les corpus à partir des `x` calculés ci-dessus:
    # différents corpus peuvent avoir des dates de ventes différentes. pour représenter
    # tous les corpus sur un même graphique, il faut avoir une seule abscisse.
    # ce `x` global correspond à une liste de toutes les années entre la date de vente
    # la plus ancienne et la plus récente, pour tous les corpus.
    x = []  # axe des abscisses fini.
    annees_total = x_idees
    for annee in x_poeme:
        annees_total.append(annee)
    for annee in x_roman:
        annees_total.append(annee)
    for annee in x_theatre:
        annees_total.append(annee)
    
    for i in range(min(annees_total), max(annees_total) + 1):
        x.append(i)
    
    
def pipeline():
    """
    fonction décrivant le processus global de traitement
    et analyse du texte.
    """
    # lire les fichiers et stocker leur contenu dans une variable
    corpus_idees = read_text("idees")
    corpus_poeme = read_text("poeme")
    corpus_roman = read_text("roman")
    corpus_theatre = read_text("theatre")
    
    # transformer les fichiers en documents structurés
    corpus_idees = structure(corpus_idees)
    corpus_poeme = structure(corpus_poeme)
    corpus_roman = structure(corpus_roman)
    corpus_theatre = structure(corpus_theatre)
    
    # créer des visualisations
    visualize(corpus_idees, corpus_poeme, corpus_roman, corpus_theatre)

if __name__ == "__main__":
    pipeline()
    
    
