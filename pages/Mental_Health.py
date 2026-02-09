import streamlit as st
import sys
from pathlib import Path

# Ajouter le répertoire parent au path pour les imports
sys.path.append(str(Path(__file__).parent.parent))

from database.db_manager_health import MentalHealthDB
from components.health.filters import render_filters
from components.health.visualizations import render_all_kpis

# Configuration de la page
st.set_page_config(
    page_title="Student Mental Health Analytics",
    page_icon="🧠",
    layout="wide"
)

# CSS personnalisé
st.markdown("""
    <style>
    .main-title {
        font-size: 2.5rem;
        color: #9B59B6;
        text-align: center;
        margin-bottom: 1rem;
    }
    .subtitle {
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
    }
    .alert-box {
        padding: 1rem;
        background-color: #FFF3CD;
        border-left: 4px solid #FFC107;
        margin: 1rem 0;
        border-radius: 5px;
    }
    .info-box {
        padding: 1rem;
        background-color: #D1ECF1;
        border-left: 4px solid #0C5460;
        margin: 1rem 0;
        border-radius: 5px;
    }
    </style>
""", unsafe_allow_html=True)

# En-tête
st.markdown('<h1 class="main-title">🧠 Student Mental Health Analysis</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Analyse de la Santé Mentale des Étudiants</p>', unsafe_allow_html=True)

# Message d'avertissement
st.markdown("""
<div class="alert-box">
    <strong>⚠️ Note Importante :</strong> Cette analyse est réalisée à des fins pédagogiques uniquement. 
    Les données présentées ne doivent pas être utilisées pour un diagnostic médical. 
    Si vous ressentez des difficultés psychologiques, consultez un professionnel de santé.
</div>
""", unsafe_allow_html=True)

# Sidebar pour l'upload
with st.sidebar:
    st.header("📁 Import des Données")
    
    uploaded_file = st.file_uploader(
        "Choisissez le fichier CSV Mental Health",
        type=['csv'],
        help="Uploadez le fichier Student Mental health.csv"
    )
    
    st.markdown("---")
    
    st.info("""
    📌 **Format attendu :**
    - Gender
    - Age
    - Year (année d'études)
    - CGPA (performance académique)
    - Depression (Yes/No)
    - Anxiety (Yes/No)
    - Panic Attack (Yes/No)
    - Treatment (Yes/No)
    """)

# Contenu principal
if uploaded_file is not None:
    # Initialiser la base de données
    db = MentalHealthDB()
    
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
        with st.expander("📋 Voir les Données Brutes"):
            st.dataframe(df, use_container_width=True, height=400)
            
            # Statistiques de base
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total Étudiants", len(df))
            
            with col2:
                if 'gender' in df.columns:
                    unique_genders = df['gender'].nunique()
                    st.metric("Genres", unique_genders)
            
            with col3:
                if 'age' in df.columns:
                    avg_age = df['age'].mean()
                    st.metric("Âge Moyen", f"{avg_age:.1f} ans")
            
            with col4:
                if 'cgpa' in df.columns:
                    avg_cgpa = df['cgpa'].mean()
                    st.metric("CGPA Moyen", f"{avg_cgpa:.2f}")
            
            # Bouton de téléchargement
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Télécharger les données filtrées (CSV)",
                data=csv,
                file_name='mental_health_filtered.csv',
                mime='text/csv',
            )

else:
    # Message d'accueil si aucun fichier n'est uploadé
    st.info("👆 Veuillez uploader le fichier CSV Student Mental Health pour commencer l'analyse")
    
    # Instructions
    st.markdown("### 📖 Instructions")
    st.markdown("""
    1. Téléchargez le dataset depuis [Kaggle - Student Mental Health](https://www.kaggle.com/datasets/shariful07/student-mental-health)
    2. Uploadez le fichier `Student Mental health.csv` dans la barre latérale
    3. Utilisez les filtres pour affiner votre analyse
    4. Explorez les 4 indicateurs clés de performance (KPI) avec des visualisations interactives
    """)
    
    # Aperçu des KPI
    st.markdown("### 🎯 KPI Disponibles")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **📊 KPI 1 : Vue d'Ensemble de la Santé Mentale**
        - Répartition des étudiants par condition (dépression, anxiété, attaques de panique)
        - Taux de prévalence globaux
        - Statistiques sur le traitement
        
        **👥 KPI 2 : Analyse par Genre**
        - Comparaison des taux de dépression, anxiété et attaques de panique entre genres
        - Identification des groupes à risque
        - Distribution par genre
        """)
    
    with col2:
        st.markdown("""
        **📈 KPI 3 : Corrélation Performance Académique vs Santé Mentale**
        - Scatter plot : CGPA vs conditions mentales
        - Impact du stress sur les résultats académiques
        - CGPA moyen par état de santé mentale
        
        **⚠️ KPI 4 : Facteurs de Risque et Traitement**
        - Distribution des facteurs de risque
        - Taux de traitement
        - Analyse de l'efficacité du traitement
        """)
    
    # Ressources d'aide
    st.markdown("---")
    st.markdown("### 🆘 Ressources d'Aide")
    
    st.markdown("""
    <div class="info-box">
        Si vous ou quelqu'un que vous connaissez avez besoin d'aide :
        <ul>
            <li><strong>3114</strong> : Numéro national de prévention du suicide (France)</li>
            <li><strong>Fil Santé Jeunes</strong> : 0 800 235 236 (gratuit et anonyme)</li>
            <li><strong>SOS Amitié</strong> : 09 72 39 40 50</li>
            <li><strong>Nightline</strong> : Service d'écoute par et pour les étudiants</li>
            <li><strong>Psychologues.fr</strong> : Annuaire de psychologues</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Information sur les services universitaires
    st.markdown("### 🏫 Services Universitaires")
    st.markdown("""
    La plupart des universités proposent des services de soutien psychologique gratuits pour les étudiants :
    - Services de santé universitaire (SSU)
    - Bureaux d'aide psychologique universitaire (BAPU)
    - Cellules d'écoute et de soutien
    
    **N'hésitez pas à contacter le service de santé de votre établissement.**
    """)

# Footer
st.markdown("---")
st.caption("🧠 Student Mental Health Analytics | Projet MBAESG 2024-2025")
st.caption("⚕️ En cas d'urgence, contactez le 15 (SAMU) ou le 112 (numéro d'urgence européen)")