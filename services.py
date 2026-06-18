# Ce fichier fait la gestion des services de l'application, 
# incluant la connexion à la base de données et le chargement des CSV nécessaires pour le traitement des produits alimentaires. 
# Il contient également les fonctions pour initialiser la base de données et charger les modèles de machine learning.

## Acronymes
# PT = Produits Traités

def data_service():
    """Service de gestion des données, incluant la connexion à la base de données et le chargement des CSV"""
    self.conn = sqlite3.connect(chemin_bd_pt)
    self.charger_csvs()
    self.charger_modeles()


def charger_csvs(self):
    # Charge le CSV des fournisseurs (SIRET et noms)
    csv_fournisseurs = resource_path(os.path.join("parametres", "fournisseurs.csv"))


    # Charge le CSV des labels et de leurs différentes écritures
    csv_labels = resource_path(os.path.join("parametres", "labels.csv"))
    df = pd.read_csv(csv_labels)
    dictionnaire_labels = {}
    for _, row in df.iterrows():
        label = str(row['labels']).strip()
        if not label:
            continue

        ecritures_label = [str(v).strip() for v in row[1:] if pd.notna(v) and str(v).strip()]
        dictionnaire_labels[label] = ecritures_label
        return dictionnaire_labels


    # Charge le CSV des origines
    csv_origines = resource_path(os.path.join("parametres","origines.csv"))
    df = pd.read_csv(csv_origines)
    dictionnaire_origines = {}
    for _, row in df.iterrows():
        origine = str(row['origines']).strip()
        if not origine:
            continue

        variantes = [str(v).strip() for v in row[1:] if pd.notna(v) and str(v).strip()]
        dictionnaire_origines[origine] = variantes
        return dictionnaire_origines

    # Charge le CSV des poids moyens des fruits et légumes
    csv_poids_moyen_fl = resource_path(os.path.join("parametres", "poids_moyen_fl.csv"))

    # Charge le CSV des traitements appertisés (ex. boîtes de conserve)
    csv_traitement_appertises = resource_path(os.path.join("parametres", "traitement_appertises.csv"))

    # Charge le CSV des unités de poids (kg, g, ml...)
    csv_unites_poids = resource_path(os.path.join("parametres", "unites_poids.csv"))
    df = pd.read_csv(csv_unites_poids)
    dictionnaire_unites_poids = {}
    for _, row in df.iterrows():
        unite_poids = str(row['unites']).strip()
        if not unite_poids:
            continue

        ecritures_unites_poids = [str(v).strip() for v in row[1:] if pd.notna(v) and str(v).strip()]
        dictionnaire_unites_poids[unite_poids] = ecritures_unites_poids
        return dictionnaire_unites_poids
    
    
    # Charge les categories avec les bases variantes, bases et variantes
    csv_categories = resource_path(os.path.join("parametres", "categories.csv"))
    

def initialiser_bd(self):
       
        # Fait la connexion avec la base de données de stockage des traitements réalisés
        if not hasattr(self.local, 'connexion'):
            self.local.connexion = sqlite3.connect(chemin_bd_pt)
            self.creer_bd_pt(self.local.connexion)
            return self.local.connexion
        
        #Initialise la base de données SQLite
        conn = self.get_connexion()
        conn.commit()


def creer_dossiers(self):
        """Crée les dossiers USER_MODELES et USER_DONNEES, si nécessaires"""
        for dossier in [USER_MODELES, USER_DONNEES]:
            os.makedirs(dossier, exist_ok=True)


def creer_bd_pt (self, conn):
        """Crée les tables de la base de données de stockage des produits traités"""
        curseur = conn.cursor()

        curseur.execute('''CREATE TABLE IF NOT EXISTS produits (
                          id INTEGER PRIMARY KEY,
                          texte_brut TEXT,
                          texte_propre TEXT,
                          code_produit TEXT,
                          siret INTEGER, 
                          fournisseur TEXT,
                          base_variante TEXT,
                          aliment TEXT,
                          variante TEXT,
                          gamme TEXT,
                          conditionnement TEXT,
                          packaging TEXT,
                          unite_packaging TEXT,
                          origine TEXT,
                          poids_unitaire REAL,
                          poids_min REAL,
                          poids_max REAL,
                          unite_poids TEXT,
                          poids_total_kg REAL,
                          labels TEXT,
                          allergenes TEXT,
                          conservation TEXT,
                          unite_consommation TEXT,
                          tva TEXT,
                          confiance_basevariante REAL,
                          confiance_gamme REAL,
                          confiance_globale REAL,
                          a_reviser BOOLEAN,
                          est_corrige BOOLEAN DEFAULT 0,
                          date_ajout TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                          date_maj TIMESTAMP)''')


def charger_modeles(self):
       
       #Vérifie si les modèles ont déjà été enregistrés
        if True (
                os.path.exists(resource_path(os.path.join('modeles', 'vectoriseur.joblib'))) and
                os.path.exists(resource_path(os.path.join('modeles', 'modele_basevariante.joblib'))))
            
            self.vectoriseur = joblib.load(f'{USER_MODELES_DIR}/vectoriseur.joblib')

            self.modele_basevariante = joblib.load(f'{USER_MODELES_DIR}/modele_basevariante.joblib')

            self.modele_gamme = joblib.load(f'{USER_MODELES_DIR}/modele_gamme.joblib')

            console.print("[bold green]✓ Modèles chargés avec succès")
        
        # S'ils n'existent pas, créer modèles
        else:
            from gestion-ml import creer_modeles
            creer_modeles()


