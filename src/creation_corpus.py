import requests  # le paquet pour faire des requêtes HTTP et récupérer des données de sources distantes
import sys  # librarie pour des opérations sur le système d'exploitation
import os  # le paquet pour construire des chemins de fichiers
import re  # librairie pour les expressions régulières


# *************************************************************
# script pour produire le texte utilisé lors de ce cours.
# processus:
# - récupérer les données en `json` depuis l'API Katabase
# - filtrer les résultats pour ne garder que les items ayant
#   un prix de vente
# - transformer ce `json` en un texte brut
# - enregristrer ce texte dans un fichier
#
# petit conseil pour lire le code: aller tout en bas du fichier
# et commencer par lire la fonction `pipeline()`. c'est elle
# qui contient la logique globale de ce script. quand cette
# fonction appelle une autre fonction, aller lire cette 
# fonction : )
#
# crédits: 
# - code: Paul Kervegan, 2023. code sous licence `GNU GPLv3.0`
# - données: Katabase (Alexandre Bartz, Simon Gabay, Matthias 
#   Gille Levenson, Paul Kervegan, Ljudmila Petkovic et Lucie 
#   Rondeau du Noyer). licence `Creative Commons Attribution 
#   4.0 International License`
# *************************************************************


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
        
        # décommenter le bloc ci dessous pour avoir, pour chaque auteur,
        # le nombre d'entrées de catalogue qui lui corresponsent, et le
        # nombre d'entrées de catalogue avec un prix
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
    on travaillera. ce jeu de données est créé à partir de l'API 
    Katabase.
    
    une API Web, en bref, c'est une application qui permet de 
    récupérer automatiquement des données brutes depuis une source 
    en ligne. içi, on construit une URL en suivant la syntaxe 
    définie par l'API Katabase; l'API traite cette URL, récupère
    les données pertinentes et renvoie ces données réponse.
    """
    # variables contenant nos 4 corpus
    data_idees = {}
    data_theatre = {}
    data_roman = {}
    data_poeme = {}
    
    auteurs_idees = [
        "voltaire"       # françois-marie arouet, dit voltaire
        , "montesquieu"  # charles louis de secondat, baron de montesquieu
        , "rousseau"     # jean-jacques rousseau
        , "diderot"      # denis diderot
        , "d'alembert"    # jean le rond d'alembert
    ]
    
    auteurs_theatre = [
        "beaumarchais"  # pierre-augustin caron de beaumarchais
        , "marivaux"    # marivaux, né pierre carlet
        , "regnard"     # jean-françois regnard
        , "lesage"      # alain-rené lesage
        , "sedaine"     # michel-jean sedaine
    ]
    
    auteurs_roman = [
        "restif de la bretonne"  # nicolas edme restif de la bretonne
        , "laclos"               # choderlos de laclos
        , "sade"                 # marquis de sadee
        , "crebillon"            # claude-prosper joylot de crébillon
        , "cazotte"              # jacques cazotte
    ]
    
    auteurs_poeme = [
        "lefranc de pompignan"  # jean-jacques lefranc de pompignan
        , "gilbert"             # nicolas gilbert
        , "delille"             # jacques delille
        , "chenier"             # andré chénier
        , "parny"               # évariste de parny
    ]
    
    # on itère sur tous les auteurs pour faire une requête.
    # - à chaque itération, on donne à la variable `author` le nom
    #   d'un auteur dans les listes `author_*` définies ci-dessus.
    # -  pour chaque `auteur`, on fait une requête sur ce nom pour récupérer 
    #   tous les manuscrits dont il ou elle est l'auteur.ice. 
    # - on construit ensuite nos jsons de sortie (`data_idees`...) avec
    #   les résultats obtenus via l'API.
    for auteur in auteurs_idees:
        data_idees = katapi_request(data_idees, auteur)
    for auteur in auteurs_theatre:
        data_theatre = katapi_request(data_theatre, auteur)
    for auteur in auteurs_roman:
        data_roman = katapi_request(data_roman, auteur)
    for auteur in auteurs_poeme:
        data_poeme = katapi_request(data_poeme, auteur)
    
    return data_idees, data_theatre, data_roman, data_poeme
    
    
def clean_dataset(dataset):
    """
    ici, on traite légèrement les jeux de données en JSON:
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
        
        # on supprime les éléments inutiles
        value.pop("author_wikidata_id", None)  # l'identifiant wikidata
        value.pop("format", None)  # le format de l'autographe
        value.pop("term", None)  # un terme normalisé décrivant le type de manuscrit (lettre autographe...)
        
        # on supprime à l'aide d'expressions régulières 
        # les espaces en trop dans la description.
        # (les expressions régulières sont expressions permettant de 
        # détecter des motifs dans un texte à l'aide d'une grammaire normalisée)
        # la fonction `re.sub()` permet d'effectuer les remplacements à l'aide
        # d'expressions régulières.
        # la syntaxe est: `re.sub("motif à remplacer", "remplacement", texte_a_traiter)`
        #
        # `\n*\s+` représente zéro à plusieurs sauts de ligne suivis par un
        # ou plusieurs espaces. on replace par un unique espace, supprimant ainsi
        # les espaces et sauts de lignes dans la description..
        value["desc"] = re.sub("\n*\s+", " ", value["desc"])
        
        # pour finir, on ajoute à `dataset_out` avec les descriptions d'items nettoyées
        dataset_out[key] = value

    return dataset_out
    

def make_text(dataset, genre):
    """
    ici, on construit un fichier en texte brut à partir du JSON récupéré
    par l'API Katabase et on l'enregistre dans un fichier.
    
    :param dataset: le jeu de données à partir duquel produire un texte brut.
    :param genre: le genre dans lequel les auteurs sont actifs, pour savoir quel 
                  jeu de données on traite et quel sera le nom du fichier produit.
    """
    text_out = ""  # le texte brut qui sera produit
    
    # on utilise `.values()` pour itérer seulement sur les valeurs: 
    # - `.values()` produit une liste des valeurs d'un dictionnaire,
    #   c'est-à-dire des éléments à droite dans des entrées de
    #   dictionnaire
    # - l'identifiant des entrées de catalogues ne sera pas retenu 
    #   dans le texte qu'on est en train de construire, donc pas la
    #   peine d'itérer sur celui-ci.
    for value in dataset.values():
        value_to_string = ""  # la version texte de l'entrée de catalogue
        
        # on ajoute le nom de l'auteur
        value_to_string = f"{value['author']}\n"
        
        # si il existe une date d'écriture du manuscrit, on l'ajoute
        if value["date"] is not None:
            value_to_string += f"Écrit en {value['date']}. "
        
        # on ajoute ensuite la date de vente, le nombre de pages et une description
        value_to_string += f"Vendu en {value['sell_date']}.\n"\
                           + f"Dimensions: {value['number_of_pages']} pages.\n"\
                           + f"{value['desc']}\n"
        
        # si il y a un prix, on ajoute le prix, la monnaie et le prix en francs constants.
        if value["price"] is not None:
            value_to_string += f"Prix: {value['price']} {value['currency']} "\
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
    # `os.path.join()` crée un chemin à partir de noms de dossiers ou de fichiers
    # ici, on crée un chemin depuis le dossier actuel vers le dossier parent, puis
    # vers le dossier `in/`
    outdir = os.path.join(current_directory, os.pardir, "in")
    
    # si le dossier de sortie n'existe pas, on le créée pour éviter les erreurs 
    # avec `os.makedirs()`
    if not os.path.isdir(outdir):
        os.makedirs(outdir)
    
    # on ouvre le fichier de sortie en écriture
    # `with open() as fh` permet d'ouvrir un fichier indiqué en premier argument de la
    # fonction `open` et de l'assigner à la variable `fh` pour pouvoir y écrire du contenu
    with open(os.path.join(
        # ci-dessous, le chemin vers le fichier: `catalogue_idees.txt`, `catalogue_theatre.txt`...
        outdir, f"catalogue_{genre}.txt"),
        # `mode='w+'` permet d'indiquer que le fichier est ouvert en écriture, 
        # c'est à dire qu'on va y écrire du contenu
        mode="w+" 
    ) as fh:
        fh.write(text_out)  # on y écrit le contenu de `text_out`
    

def pipeline():
    """
    fonction décrivant le processus global
    """
    # faire les requêtes sur l'api
    data_idees, data_theatre, data_roman, data_poeme = get_katabase_dataset()
    
    # nettoyer les jeux de données
    data_idees = clean_dataset(data_idees)
    data_theatre = clean_dataset(data_theatre)
    data_roman = clean_dataset(data_roman)
    data_poeme = clean_dataset(data_poeme)
    
    # transformer les jeux de données `json` en 
    # fichiers texte et les enregistrer
    make_text(data_idees, "idees")
    make_text(data_theatre, "theatre")
    make_text(data_roman, "roman")
    make_text(data_poeme, "poeme")


if __name__ == "__main__":
    pipeline()
