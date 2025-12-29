### Explications du script
# ce fichier est réalise la gestion des modèles de machine learning (création, suppression et remplacement)
# bd_entrainement = base de données qui a des données utilisées pour l'entrainement des modèles (données des auteurs et utilisateurs)
# bd_produits = base de données avec tous les produits déjà traités par le logiciel

### bibliothèques
import os
import sqlite3
import joblib
import pandas as pd
from riche.console import Console
from datime import datetime
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.calibration import CalibratedClassifierCV
from sklearn.svm import LinearSVC
from rich.progress import Progress
from utils import console, MODELES_DIR, DONNEES_DIR, chemin_bd_entrainement, chemin_bd_produits, resourse_path

console = Console() # console pour enrichir les impressions dans le terminal (complément pour la fonction print)

con_entrainement = sqlite3.connect(chemin_bd_entrainement)
cursor_entrainement = con_entrainement.cursor()
con_produits = sqlite3.connect(chemin_bd_produits)
cursor_produits = con_produits.cursor()

### Fonctions
def __init__ (self, chemin_bd)
  #self.chemin_bd_entrainement = chemin_bd_entrainement
  self.maj_bd_entrainement()
  
def maj_bd_entraitenement (self):
  #creer fonctions de maj de la bd_entrainement à partir de la bd_produits
  
  recreer_modeles()

def recreer_modeles (self):
  """Supprime les modèles existants et crée de nouveaux modèles."""

  for fichier in [
    "vectoriseur.joblib",
    "modele_basevariante.joblib",
    "modele_gamme.joblib"
  ]:
    chemin_fichier_modele = os.path.join(MODELES_DIR, nom_fichier) # cette fonction réalise le chemin ".../MODELES_DIR/xxx.joblib"
    if os.path.exists (chemin_fichiers_modeles):
      os.remove(chemin_fichier_modele) # si le modèle déjà existe, le supprimer
    creer_modeles()

def creer_modeles (self):
  #### AF:écrire création des modèles
  try:
    with Progress() as progression:
    # tache_global

    chemin_bd_entrainement = resource_path("bases_de_donnees/bd_entrainement.db")
    if not os.path.exists(chemin_bd_entrainement):
      console.print("[red]La base de données d'entrainement est introuvable ![/red]")
    chunks = 

  

  
