import streamlit as st
import sys
from pathlib import Path

# Ajouter le répertoire parent au path pour les imports
sys.path.append(str(Path(__file__).parent.parent))

from database.db_manager_prime import AmazonPrimeDB
from components.amazon.filters import render_filters
from components.amazon.visualizations import render_all_kpis

# Configuration de la page
st.set_page_config(
    page_title="Amazon Prime Analytics",
    layout="wide"
)

# CSS personnalisé
st.markdown("""
    <style>
    .main-title {
        font-size: 2.5rem;
        color: #00A8E1;
        text-align: center;
        margin-bottom: 1rem;
    }
    .subtitle {
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
    }
    </style>
""", unsafe_allow_html=True)

# En-tête
st.markdown('<h1 class="main-title">Amazon Prime Movies & TV Shows</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Analyse Complète du Catalogue de Streaming</p>', unsafe_allow_html=True)

# Sidebar pour l'upload
with st.sidebar:
    st.header("Import des Données")
    
    uploaded_file = st.file_uploader(
        "Choisissez le fichier CSV Amazon Prime",
        type=['csv'],
        help="Uploadez le fichier amazon_prime_titles.csv"
    )
    
    st.markdown("---")
    

# Contenu principal
if uploaded_file is not None:
    # Initialiser la base de données
    db = AmazonPrimeDB()
    
    # Charger les données
    df = db.load_csv(uploaded_file)
    
    if df is not None:
        st.markdown("---")
        
        # Afficher les filtres et récupérer les valeurs
        filters = render_filters(db)
        
        st.markdown("---")
        
        # Afficher les KPI
        render_all_kpis(db, filters)
        
        # Section données brutes (optionnel)
        st.markdown("---")
        with st.expander(" Voir les Données Brutes"):
            st.dataframe(df, use_container_width=True, height=400)
            
            # Bouton de téléchargement
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Télécharger les données filtrées (CSV)",
                data=csv,
                file_name='amazon_prime_filtered.csv',
                mime='text/csv',
            )

else:
    # Message d'accueil si aucun fichier n'est uploadé
    st.info("Veuillez uploader le fichier CSV Amazon Prime pour commencer l'analyse")
    

    # Instructions
    st.markdown("### Instructions")
    st.markdown("""
    1. Téléchargez le dataset depuis [Kaggle](https://www.kaggle.com/datasets/shivamb/amazon-prime-movies-and-tv-shows)
    2. Uploadez le fichier `amazon_prime_titles.csv` dans la barre latérale
    3. Utilisez les filtres pour affiner votre analyse
    4. Explorez les 4 KPI avec des visualisations interactives
    """)
    
    # Aperçu des KPI
    st.markdown("### KPI Disponibles")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Évolution du Catalogue**
        - Visualisation de la croissance du contenu dans le temps
        - Tendances d'ajout de films et séries
        
        **Top Genres**
        - Les 10 genres les plus représentés
        - Distribution par catégorie de contenu
        """)
    
    with col2:
        st.markdown("""
        **Répartition Géographique**
        - Pays de production principaux
        - Diversité géographique du catalogue
        
        **Films vs Séries**
        - Comparaison quantitative
        - Évolution temporelle
        """)
# Footer
st.markdown("---")
st.caption("Amazon Prime Analytics | Projet MBAESG 2025-2026")