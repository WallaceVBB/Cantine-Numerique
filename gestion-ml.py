### Explications du fichier
# ce fichier réalise la gestion des modèles de machine learning (création, suppression et remplacement)

## Varibles
# bd_entrainement = base de données qui a des données utilisées pour l'entrainement des modèles (données des auteurs (csv "baseet utilisateurs)
# bd_pt = base de données avec tous les produits déjà traités par le logiciel

## TODO's:


### bibliothèques
import os
import sqlite3
import joblib
import pandas as pd
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.calibration import CalibratedClassifierCV
from sklearn.svm import LinearSVC
from rich.progress import Progress
from utils import console, MODELES_DIR, PARAMETRES_DIR, bd_entrainement, bd_pt, ressource_path


## Code

class GestionML:
    """Gestion des modèles de machine learning"""
    
    def __init__(self, bd_entrainement_path):
        """Initialise la gestion ML"""
        self.bd_entrainement = bd_entrainement_path
        if not os.path.exists(bd_entrainement_path):
            console.print("[yellow]La base de données d'entrainement est introuvable, création d'une nouvelle base...[/yellow]")
            self.creer_bd_entrainement()
        self.maj_bd_entrainement()

    def recreer_modeles(self):
        """Supprime les modèles existants et crée de nouveaux modèles."""
        for fichier in [
            "vectoriseur.joblib",
            "modele_basevariante.joblib"
        ]:
            chemin_fichiers_modeles = os.path.join(MODELES_DIR, fichier)
            if os.path.exists(chemin_fichiers_modeles):
                os.remove(chemin_fichiers_modeles)
        self.creer_modeles()

    def creer_modeles(self):
        """Crée les modèles de machine learning"""
        try:
            with Progress() as progression:
                tache_globale = progression.add_task("[cyan]Entraînement global...", total=100)
                tache_etape = progression.add_task("[magenta]Étape en cours...", total=100)

                bd_entrainement_path = ressource_path("bases_de_donnees/bd_entrainement.db")
                if not os.path.exists(bd_entrainement_path):
                    console.print("[red]La base de données d'entrainement est introuvable ![/red]")
                    return
                    
                chunks = pd.read_csv(bd_entrainement_path, chunksize=1000)
                donnees = pd.concat(chunks)
                progression.update(tache_globale, advance=10)
                progression.update(tache_etape, advance=1)

                # Nettoyage des données
                console.print("Nettoyage des données...")
                donnees = donnees[donnees['base_variante'].map(donnees['base_variante'].value_counts()) >= 4]
                progression.update(tache_globale, advance=10)
                progression.update(tache_etape, advance=1)

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
                joblib.dump(self.vectoriseur, os.path.join(MODELES_DIR, 'vectoriseur.joblib'), compress=3)
                joblib.dump(self.modele_basevariante, os.path.join(MODELES_DIR, 'modele_basevariante.joblib'),
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
