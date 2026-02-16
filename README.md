# Dashboard Multi-Datasets - Projet Streamlit

Application web interactive d'analyse de données développée avec Streamlit et DuckDB.

## Description

Cette application permet d'analyser deux datasets distincts :
-  **Amazon Prime Movies & TV Shows** : Analyse du catalogue de contenu
- **Student Mental Health** : Analyse de la santé mentale des étudiants

Chaque dataset propose 4 indicateurs clés de performance (KPI) avec des visualisations interactives et des filtres dynamiques.

## Installation

### Prérequis
- Python 3.8 ou supérieur
- pip (gestionnaire de packages Python)

### Étapes d'installation

1. **Cloner le dépôt**
```bash
git clone https://github.com/seynabou2/appstreamlit.git
cd appstreamlit.git
```

2. **Installer les dépendances**
```bash
pip install streamlit duckdb pandas plotly
```

OU utiliser le fichier requirements.txt :
```bash
pip install -r requirements.txt
```

3. **Lancer l'application**
```bash
streamlit run app.py 
```
sinon faire :
 
```bash
python -m streamlit run app.py 
```

L'application s'ouvrira automatiquement dans votre navigateur à l'adresse `http://localhost:8501`

L'application est également disponible dans le cloud à l'adresse suivante : https://projetmbaesg.streamlit.app/

## Structure du Projet
```
projet-streamlit/
│
├── app.py                              # Page d'accueil
├── pages/
│   ├── Amazon_Prime.py           # Page Amazon Prime
│   └── Mental_Health.py          # Page Mental Health
│
├── database/
│   ├── db_manager_prime.py            # Gestion de la base Amazon Prime 
│   └── db_manager_health.py           # Gestion de la baseental Health
│
├── components/
│   ├── amazon/
│   │   ├── filters.py                 # Filtres Amazon
│   │   └── visualizations.py          # Visualisations Amazon
│   └── health/
│       ├── filters.py                 # Filtres Mental Health
│       └── visualizations.py          # Visualisations Mental Health
│
├── data/
│   └── uploaded/                      # Fichiers CSV uploadés
│
├── requirements.txt                   # Dépendances Python à installer
└── README.md                          # Ce fichier
```

## Fonctionnalités

### Amazon Prime Analytics
- **KPI 1** : Évolution du catalogue dans le temps
- **KPI 2** : Top 10 des genres
- **KPI 3** : Répartition géographique de la production
- **KPI 4** : Comparaison Films vs Séries TV

**Filtres disponibles :**
- Type de contenu (Movie/TV Show)
- Période d'ajout
- Genres
- Pays de production

### Student Mental Health Analytics
- **KPI 1** : Distribution des niveaux de stress
- **KPI 2** : Santé mentale par genre
- **KPI 3** : Corrélation performance académique vs stress
- **KPI 4** : Identification des facteurs de risque

**Filtres disponibles :**
- Genre des étudiants
- Tranche d'âge
- Niveau d'études
- Niveau de stress

##  Équipe de Développement

| Membre | Rôle | Responsabilités |
|--------|------|-----------------|
| **Seynabou SENE** | Chef de Projet + Backend Amazon | Git, page d'accueil, base de données Amazon |
| **Mame Diarra NDIAYE** | Frontend Amazon | Interface et visualisations Amazon Prime |
| **Emeric GNANVI** | Backend Mental Health | Base de données Mental Health |
| **Pla Ayebie DORGELES** | Frontend Mental Health | Interface et visualisations Mental Health |

## Technologies Utilisées

- **Streamlit** : Framework pour l'interface web
- **DuckDB** : Base de données analytique
- **Pandas** : Manipulation de données
- **Plotly** : Visualisations interactives
- **Python 3.8+** : Langage de programmation

## Datasets

### Amazon Prime Movies & TV Shows
- **Source** : [Kaggle - Amazon Prime Dataset](https://www.kaggle.com/datasets/shivamb/amazon-prime-movies-and-tv-shows)
- **Format** : CSV
- **Taille** : ~8000 entrées

### Student Mental Health
- **Source** : [Kaggle - Student Mental Health](https://www.kaggle.com/datasets/shariful07/student-mental-health)
- **Format** : CSV
- **Taille** : ~100 entrées

## Utilisation

1. **Lancer l'application** : `streamlit run app.py`
2. **Choisir un dataset** sur la page d'accueil
3. **Uploader le fichier CSV** correspondant
4. **Appliquer des filtres** dans la barre latérale
5. **Explorer les visualisations** interactives

## Licence

Projet académique - MBAESG 2024-2025

## Contact

Pour toute question concernant le projet, contactez l'équipe via le dépôt GitHub.

---

**Version** : 1.0  
**Date** : Février 2025  
**Cours** : Environnement, Agilité, Git, Devops - MBAESG