### Explications du script
# Ce fichier gère les chemins et répertoires utilisés par l'application.

# AF (à faire) : 
    # + ajouter la reconnaissance de la plateforme (Windows, MacOS, Linux)


### Bibliothèque
import os
import sys
import shutil


###Fonctions et constantes

#### AF: ajouter fonction qui reconnaît la plateforme et choisi la bonne option pour le USER_APP_DIR
USER_APP_DIR = os.path.expanduser("~AppData/Local/Cantine Egalim") # Dossier père sur Linux et Windows
# USER_DATA_DIR = os.path.expanduser("~/Library/Application Support/Cantine Egalim") # Dossier père sur MacOS
MODELES_DIR = os.path.join(USER_APP_DIR, "modeles") # sous-dossier pour les modèles de machine learning
PARAMETRES_DIR = os.path.join(USER_APP_DIR, "parametres") # sous-dossier pour les paramètres pour le traitement
GUI_DIR = os.path.join(USER_APP_DIR, "gui") # sous-dossier pour les fichiers graphiques
BD_DIR = os.path.join(USER_APP_DIR, "bases_de_donnees") # sous-dossier pour les bases de données
chemin_bd_entrainement = os.path.join(BD_DIR, "bd_entrainement.db") # chemin vers la base de données d'entrainement
chemin_bd_produits = os.path.join(BD_DIR, "bd_produits.db") # chemin vers la base de données des produits

os.makedirs(USER_APP_DIR, exist_ok=True)
os.makedirs(MODELES_DIR, exist_ok=True)
os.makedirs(PARAMETRES_DIR, exist_ok=True)
os.makedirs(GUI_DIR, exist_ok=True)
os.makedirs(BD_DIR, exist_ok=True)

def ressource_path (relative_path):
    """Obtient le chemin absolu vers les ressources du programme, que le programme 
    soit empaqueté ou en script."""
    
    if hasattr(sys, '_MEIPASS'): # si le programme est empaqueté (.exe)
        base_path = sys._MEIPASS
    else: # si le programme est lancé en script (.py)
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)

def assurer_fichier_utilisateur (nom_fichier, sous_dossier=None):
    """Assure que le fichier spécifié existe dans le directoire utilisateur.
    Si le fichier n'existe pas, il est copié depuis les ressources de l'application."""

    if sous_dossier:
        dossier_utilisateur = os.path.join(USER_APP_DIR, sous_dossier)
        os.makedirs(dossier_utilisateur, exist_ok=True)
    else:
        dossier_utilisateur = USER_APP_DIR

    chemin_fichier_utilisateur = os.path.join(dossier_utilisateur, nom_fichier)
    chemin_bundle = ressource_path(os.path.join(sous_dossier, nom_fichier) if sous_dossier else nom_fichier)

    if not os.path.exists(chemin_fichier_utilisateur):
        shutil.copy(chemin_bundle, chemin_fichier_utilisateur)

    return chemin_fichier_utilisateur

def copier_fichier_ressource_vers_utilisateur ():
    """"Copie les fichiers nécessaires depuis les ressources de l'application vers le
    dossier utilisateur lors de la première exécution."""

    fichiers_a_copier = [
        ("bd_entrainement.db", "bases_de_donnees"),
        ("bd_produits.db", "bases_de_donnees")
    ]

    for nom_fichier, sous_dossier in fichiers_a_copier:
        assurer_fichier_utilisateur(nom_fichier, sous_dossier)