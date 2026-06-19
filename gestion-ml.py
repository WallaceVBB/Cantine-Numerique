### Explications du script
# ce fichier réalise la gestion des modèles de machine learning (création, suppression et remplacement)
# bd_entrainement = base de données qui a des données utilisées pour l'entrainement des modèles (données des auteurs et utilisateurs)
# bd_pt = base de données avec tous les produits déjà traités par le logiciel

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
from utils import console, MODELES_DIR, DONNEES_DIR, chemin_bd_entrainement, chemin_bd_pt, resourse_path

console = Console() # console pour enrichir les impressions dans le terminal (complément pour la fonction print)

con_entrainement = sqlite3.connect(chemin_bd_entrainement)
cursor_entrainement = con_entrainement.cursor()
con_pt = sqlite3.connect(chemin_bd_pt)
cursor_pt = con_pt.cursor()

### Fonctions

# Connection à la base de données d'entrainement des modèles de machine learning
def __init__ (self, chemin_bd_entrainement):
  #self.chemin_bd_entrainement = chemin_bd_entrainement
  self.maj_bd_entrainement()
  
def maj_bd_entraitenement (self):
  #creer fonctions de maj de la bd_entrainement à partir de la bd_produits
  
  recreer_modeles()


# Modèles de machine learning


def recreer_modeles (self):
  """Supprime les modèles existants et crée de nouveaux modèles."""

  for fichier in [
    "vectoriseur.joblib",
    "modele_basevariante.joblib"
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
    chunks = pd.read_csv(chemin_csv_aliments, chunksize=1000)
    donnees = pd.concat(chunks)
    progression.update(tache_globale, advance=10)
    progression.update(tache_etape, advance=1)


    # Nettoyage des données
    console.print("Nettoyage des données...")
    donnees = donnees[donnees['base_variante'].map(donnees['base_variante'].value_counts()) >= 4]
    progression.update(tache_globale, advance=10)
    progression.update(tache_etape, advance=1)
    print("Nettoyage des texte designation réalisé pour la vectorisation")

    # Vectorialisation de bases variantes
    self.vectoriseur = TfidfVectorizer(max_features=3000, ngram_range=(1, 2), sublinear_tf=True, min_df=3)
    textes = donnees['designation'].apply(self.nettoyer_texte).tolist()
    X = self.vectoriseur.fit_transform(textes)
    progression.update(tache_globale, advance=20)
    progression.update(tache_etape, advance=1)

    # Configuration des modèles avec LinearSVC
    svc_params = {
        'class_weight': 'balanced',
        'max_iter': 1000
    }

    # Modèle base_variante
    console.print("[blue]Entraînement du modèle base_variante (LinearSVC)...")
    self.modele_basevariante = CalibratedClassifierCV(
        LinearSVC(**svc_params),
        cv=3
    ).fit(X, donnees['base_variante'])
    progression.update(tache_globale, advance=30)
    progression.update(tache_etape, advance=1)

    # Sauvegarde
    console.print("Sauvegarde des modèles...")
    joblib.dump(self.vectoriseur, os.path.join(USER_MODELES_DIR, 'vectoriseur.joblib'), compress=3)
    joblib.dump(self.modele_basevariante, os.path.join(USER_MODELES_DIR, 'modele_basevariante.joblib'),
                compress=3)
    progression.update(tache_globale, advance=10)
    progression.update(tache_etape, advance=1)

    console.print(f"[bold green]✓ Modèles LinearSVC entraînés et sauvegardés dans {MODELES_DIR}")

        except Exception as e:
            console.print(f"[bold red]✗ Erreur lors de l'entraînement: {e}")
            raise


def nettoyer_texte(self, texte):
      """Nettoie et normalise le texte"""
      texte = str(texte).lower()
      texte = re.sub(r'[^\w\s-]', '', texte)
      texte = re.sub(r'\s+', ' ', texte).strip()
      return texte
  
