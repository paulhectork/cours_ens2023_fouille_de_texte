import requests  # le paquet pour faire des requêtes HTTP et récupérer des données de sources distantes
import json  # le paquet pour parser des `json`, format analogue au dictionnaire Python
import os  # le paquet pour construire des chemins de fichiers
import re
import sys



# -------------------------------------------------------------
# script pour produire le texte utilisé lors de ce cours.
# processus:
# - récupérer les données en `json` depuis l'API Katabase
# - filtrer les résultats pour ne garder que les items ayant
#   un prix de vente
# - transformer ce `json` en un texte brut
# - enregristrer ce texte dans un fichier
# 
# crédits: 
# - code: Paul Kervegan, 2023. code sous licence `GNU GPLv3.0`
# - données: Katabase (Alexandre Bartz, Simon Gabay, Matthias 
#   Gille Levenson, Paul Kervegan, Ljudmila Petkovic et Lucie 
#   Rondeau du Noyer). licence `Creative Commons Attribution 
#   4.0 International License`
# -------------------------------------------------------------




# PROBLÈME: ON MANQUE SÉRIEUSEMENT DE DONNÉES AVEC DES PRIX POUR LES FEMMES
# => CHANGER DE THÈME ?? URFH
# POSSIBILITÉ: SUR L'ÉVOLUTION DE LA COURBE DU PRIX D'AUTEURS PAR GENRE AU XVIIIE SIECLE
# CF: https://fr.wikipedia.org/wiki/Litt%C3%A9rature_fran%C3%A7aise_du_XVIIIe_si%C3%A8cle




def katapi_request(dataset, author_name):
    """
    fonction permettant de lancer une requête, traiter
    le résultat et construire notre jeu de données en 
    sortie.
    
    :param dataset: le jeu de données à compléter.
    :param author_name: le nom de l'auteur.ice recherché.e
    :returns: le jeu de données avec les résultats renvoyés par
              l'API pour le nom `author_name`
    """
    # étape 1: définir les paramètres
    root_url = " https://katabase.huma-num.fr/katapi?"  # l'URL pointant vers l'API
    params = {
        # les paramètres de notre requête
        "level": "item",  # la requête est faite sur les entrées de catalogue, pas sur un catalogue complet
        "format": "json",  # la réponse devra être en `json` (non en `xml-tei`)
        "sell_date": "1850-1910",  # les manuscrits ont été vendus entre 1850 et 1900
        "name": author_name  # l'auteur.ice du manuscrit est
    }

    # étape 2: lancer la requête
    # le module `requests` permet de faire des requêtes HTTP. ici on fait une
    # requête `GET` (qui sert à récupérer des données) avec `requests.get()`.
    # cette fonction prend, en premier argument, une URL et en deuxième argument,
    # un dictionnaire comprenant des paramètres additionnels.
    # dans une URL, les paramètres sont en général exprimés sous la forme d'un 
    # ensemble de mots clés associés à une valeur (par exemple: `author=sevigne`).
    # 
    # en fait, `requests` traite notre dictonnaire de paramètres pour compléter 
    # l'URL donnée en premier paramètre, ce qu'on voit avec `print(r.url)`.
    r = requests.get(root_url, params=params)
    # print(r.url)
    
    # étape 3: traiter les résultats    
    response = r.json()  # `r.json()` permet d'accéder aux résultats de la requête en `json`
    # on vérifie le code http de sortie. celui-ci est un nombre à 3 chiffres
    # qui indique si une requête s'est bien déroulée; si il y a une erreur, il
    # indique laquelle (la plus connue étant l'erreur 404 !)
    # dans cette API, le code HTTP s'affiche dans le corps de la réponse. le plus souvent,
    # il se trouve dans l'en-tête (nommée `HTTP header`) qui est renvoyé avec n'importe quelle
    # réponse HTTP et qui est accessible via `requests` avec:  `r.headers`
    if response["head"]["status_code"] == 200:
        
        # si tout va bien, on ajoute les résultats à notre dictionnaire `data`:
        # les résultats forment une liste d'identifiants d'item associés à un 
        # dictionnaire contenant une description structurée de cet item.
        # on ajoute donc ce couple identifiant-description à `data`.
        for manuscript_id in response["results"]:
            dataset[manuscript_id] = response["results"][manuscript_id]
        
        # n = 0
        # for v in response["results"].values():
        #     if v["price"] is not None:
        #         n += 1
        # print(author_name, len(response["results"].keys()), n)  # name, total results, results with price
    
    else:
        # si le code HTTP n'est pas 200, il y a une erreur, 
        # - soit de notre côté (on a mal formulé nos paramètres de recherche)
        # - soit du côté du serveur (c'est l'API qui a rencontré un problème). 
        # pour savoir, on affiche les paramètres de requête et le message d'erreur 
        # enfin, on quitte notre programme.
        print(response["head"]["query"])
        print(response["results"])
        sys.exit(1)
    
    return dataset


def get_katabase_dataset():
    """
    fonction permettant de créer le jeu de données avec lequel
    on travaillera à partir de l'API Katabase.
    
    une API Web, en bref, c'est une application qui permet de 
    récupérer automatiquement des données brutes depuis une source 
    en ligne. içi, on construit une URL en suivant la syntaxe 
    définie par l'API Katabase; l'API traite cette URL, récupère
    les données pertinentes et renvoie ces données réponse.
    """
    data_f = {}  # variable dans laquelle on stockera tous les résultats sur les autrices
    data_m = {}  # variable dans laquelle on stockera tous les résultats sur les auteurs 
    authors_f = [
        # les autrices
        "sand"         # George Sand
        , "sevigne"    # la marquise de Sévigné
        , "elssler"    # Fanny Elssler, danseuse de ballet 
        , "maintenon"  # madame de Maintenon
        , "pompadour"  # madame de Pompadour
        , "du barry"   # madame du Barry
        , "lamballe"   # princesse Lamballe
        , "montespan"  # madame de Montespan
        , "josephine"  # impératrice Josephine
    ]
    authors_m = [    
        # les auteurs
        "la rochefoucauld"
        , "verdi"
        , "voltaire"
        , "delacroix"
        , "mirabeau"
        , "musset"
        , "gericault"
    ]
    
    # on itère sur tou.te.s les auteur.ices pour faire une requête.
    # - à chaque itération, on donne à la variable `author` le nom
    #   d'un.e auteur.ice dans les listes `author_m` et `author_f`.
    # -  pour chaque `author`, on fait une requête sur ce nom pour récupérer 
    #   tous les manuscrits dont il ou elle est l'auteur.ice. 
    # - on complète ensuite nos jsons de sortie (`data_m` et `data_f`) avec
    #   les résultats obtenus via l'API.
    for author in authors_f:
        # d'abord, on s'occupe des autrices et l'on construit `data_f`
        data_f = katapi_request(data_f, author)
    for author in authors_m:
        # ensuite, on s'occupe des auteurs et l'on construit `data_m`
        data_m = katapi_request(data_m, author)
    
    return data_f, data_m


def clean_dataset(dataset):
    """
    ici, on traite légèrement les jeux de données en JSON:
    - on supprime les entrées sans prix
    - on supprime les éléments de description des entrées qui ne
      font pas partie du texte source (à l'exception du prix en 
      francs constants) et qui ne nous serviront pas ensuite
    - on supprime les espaces inutiles et sauts de lignes à l'intérieur
      de la description
    
    :param dataset: un jeu de données au format JSON construit avec `get_katabase_dataset()`.
    :returns: le jeu de données nettoyé.
    """
    dataset_out = {}  # jeu de données de sortie
    for key, value in dataset.items():
        
        # on ne traite que les items ayant un prix => les autres ne seront pas retenues
        if value["price"] is not None:
            
            # on supprime les éléments inutiles
            value.pop("author_wikidata_id", None)  # l'identifiant wikidata
            value.pop("format", None)  # le format de l'autographe
            value.pop("term", None)  # un terme normalisé décrivant le type de manuscrit (lettre autographe...)
            
            # on supprime à l'aide d'expressions régulières 
            # (système de détection de motifs dans le texte)
            # les espaces en trop dans la description.
            # la fonction `re.sub()` permet d'effectuer les remplacements.
            # la syntaxe est: `re.sub("motif à remplacer", "remplacement", texte_a_traiter)`
            #
            # `\n*\s+` représente zéro à plusieurs sauts de ligne suivis par un
            # ou plusieurs espaces. on replace par un unique espace, supprimant ainsi
            # les espaces et sauts de lignes dans la description..
            value["desc"] = re.sub("\n*\s+", " ", value["desc"])
            
            # pour finir, on ajoute à `dataset_out` avec les descriptions d'items nettoyées
            dataset_out[key] = value

    return dataset_out
    

def make_text(dataset, author_gender):
    """
    ici, on construit un fichier en texte brut à partir du JSON récupéré
    par l'API Katabase et on l'enregistre dans un fichier.
    
    :param dataset: le jeu de données à partir duquel produire un texte brut.
    :param author_gender: le genre des auteur.ices, pour savoir quel jeu de 
                          données on traite et quel sera le nom du fichier
                          produit.
    """
    text_out = ""  # le texte brut qui sera produit
    
    # on utilise `.values()` pour itérer seulement sur les valeurs: l'identifiant
    # des entrées de catalogues ne sera pas utilisé ici.
    for value in dataset.values():
        value_to_string = ""  # la version texte de l'entrée de catalogue
        
        # on ajoute le nom de l'auteur.ice
        value_to_string = f"{value['author']}\n"
        
        # si il existe une date d'écriture du manuscrit, on l'ajoute
        if value["date"] is not None:
            value_to_string += f"Écrit en {value['date']}. "
        
        # on ajoute ensuite la date de vente, le nombre de pages et une description
        value_to_string += f"Vendu en {value['sell_date']}.\n"\
                           + f"Dimensions: {value['number_of_pages']} pages.\n"\
                           + f"{value['desc']}\n"
        
        # on ajoute le prix, la monnaie et le prix en francs constants.
        value_to_string += f"Prix:{value['price']} {value['currency']} "\
                           + f"(en francs constants 1900: {value['price_c']}).\n"
        
        # enfin, pour signifier la fin d'une entrée, on ajoute 2 sauts de lignes
        # (soit une ligne vide)
        value_to_string += "\n\n"
        
        # on ajoute cette entrée à `text_out`, pour créer notre document de sortie.
        text_out += value_to_string
    
    # enfin, on enregistre le fichier.
    # pour construire les chemins de fichiers, on utilise `os`, une librairie qui
    # est très utile: les chemins de fichiers s'écrivent différemment selon le système
    # d'exploitation (Linux, Mac, Windows). `os` gère les différences de syntaxes selon
    # les systèmes, et on peut donc pointer vers un même chemin sous Linux, Mac et Windows.
    # par contre, la syntaxe n'est pas très légère
    #
    # ci dessous, on prend le chemin absolu (`abspath`) du dossier (`dirname`) où se trouve
    # le ficher actuel (`__file__`)
    current_directory = os.path.abspath(os.path.dirname(__file__))
    
    # on crée le chemin de sortie.
    # `os.path.join()` crée un chemin à partir de noms de dossiers
    outdir = os.path.join(current_directory, os.pardir, "in")
    
    # si le dossier de sortie n'existe pas, on le crée pour éviter les erreurs 
    # avec `os.makedirs()`
    if not os.path.isdir(outdir):
        os.makedirs(outdir)
    
    # on ouvre le fichier de sortie en écriture
    # `with open() as fh` permet d'ouvrir un fichier indiqué en premier argument de la
    # fonction `open` et de l'assigner à la vaviable `fh` pour pouvoir y écrire du contenu
    with open(os.path.join(
        # ci-dessous, le chemin vers le fichier. il sera nommé `catalogue_f.txt` ou `catalogue_h.txt`
        outdir, f"catalogue_{author_gender}.txt"),
        # `mode` permet d'indiquer que le fichier est ouvert en écriture, c'est à dire qu'on va y écrire du contenu
        mode="w+" 
    ) as fh:
        fh.write(text_out)  # on y écrit le contenu de `text_out`
    

def pipeline():
    """
    fonction décrivant le processus global
    """
    data_f, data_m = get_katabase_dataset()
    data_f = clean_dataset(data_f)
    data_m = clean_dataset(data_m)
    make_text(data_f, "f")
    make_text(data_m, "m")
    

if __name__ == "__main__":
    pipeline()
