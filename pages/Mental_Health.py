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
        color: #95A5A6;
        margin-bottom: 2rem;
    }
    </style>
""", unsafe_allow_html=True)

# En-tête
st.markdown('<h1 class="main-title">Student Mental Health Analysis</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Analyse de la Santé Mentale des Étudiants</p>', unsafe_allow_html=True)

# Message d'avertissement éthique - EN HAUT AVANT TOUT
st.markdown("""
<div style="padding: 1.2rem; background-color: rgba(255, 193, 7, 0.15); border-left: 5px solid #FFC107; border-radius: 8px; margin-bottom: 1.5rem;">
    <p style="color: #F39C12; font-weight: 600; margin: 0 0 0.5rem 0; font-size: 1.1rem;">
    Note importante
    </p>
    <p style="color: #E67E22; margin: 0; font-size: 0.95rem; line-height: 1.5;">
    Cette analyse est réalisée dans un cadre éducatif. Les données sur la santé mentale sont sensibles. 
    Si vous ou quelqu'un que vous connaissez éprouvez des difficultés psychologiques, veuillez consulter un professionnel.
    </p>
</div>
""", unsafe_allow_html=True)

# Sidebar pour l'upload
with st.sidebar:
    st.header("Import des Données")
    
    uploaded_file = st.file_uploader(
        "Choisissez le fichier CSV Mental Health",
        type=['csv'],
        help="Uploadez le fichier Student Mental health.csv"
    )
    
    st.markdown("---")

# Contenu principal
if uploaded_file is not None:
    # Initialiser la base de données
    db = MentalHealthDB()
    
    # Charger les données
    df = db.load_csv(uploaded_file)
    
    if df is not None:
        st.markdown("---")
        
        # Afficher les filtres dans la sidebar AVANT les KPI
        with st.sidebar:
            st.markdown("---")
            filters = render_filters(db)
        
        st.markdown("---")
        
        # Afficher les KPI
        render_all_kpis(db, filters)
        
        # Section données brutes (optionnel)
        st.markdown("---")
        with st.expander("Voir les Données Brutes"):
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
                label="Télécharger les données filtrées (CSV)",
                data=csv,
                file_name='mental_health_filtered.csv',
                mime='text/csv',
            )

else:
    # Message d'accueil si aucun fichier n'est uploadé
    st.markdown("""
    <div style="padding: 1rem; background-color: rgba(52, 152, 219, 0.15); border-left: 5px solid #3498DB; border-radius: 8px; margin-bottom: 1.5rem;">
        <p style="color: #3498DB; margin: 0; font-size: 1rem;">
        Veuillez uploader le fichier CSV Student Mental Health pour commencer l'analyse
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Instructions
    st.markdown("### Instructions")
    st.markdown("""
    1. Téléchargez le dataset depuis [Kaggle - Student Mental Health](https://www.kaggle.com/datasets/shariful07/student-mental-health)
    2. Uploadez le fichier `Student Mental health.csv` dans la barre latérale
    3. Utilisez les filtres pour affiner votre analyse
    4. Explorez les 4 indicateurs clés de performance (KPI) avec des visualisations interactives
    """)
    
    # Aperçu des KPI
    st.markdown("### KPI Disponibles")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Vue d'Ensemble de la Santé Mentale**
        - Répartition des étudiants par condition (dépression, anxiété, attaques de panique)
        - Taux de prévalence globaux
        - Statistiques sur le traitement
        
        **Analyse par Genre**
        - Comparaison des taux de dépression, anxiété et attaques de panique entre genres
        - Identification des groupes à risque
        - Distribution par genre
        """)
    
    with col2:
        st.markdown("""
        **Corrélation Performance Académique vs Santé Mentale**
        - Scatter plot : CGPA vs conditions mentales
        - Impact du stress sur les résultats académiques
        - CGPA moyen par état de santé mentale
        
        **Facteurs de Risque et Traitement**
        - Distribution des facteurs de risque
        - Taux de traitement
        - Analyse de l'efficacité du traitement
        """)

# Ressources d'aide - TOUJOURS VISIBLE EN BAS
st.markdown("---")
st.markdown("### Ressources d'Aide")

st.markdown("""
<div style="padding: 1.5rem; background-color: rgba(26, 188, 156, 0.15); border-left: 5px solid #1ABC9C; border-radius: 8px; margin-bottom: 1rem;">
    <p style="color: #16A085; margin: 0 0 1rem 0; font-size: 1rem; line-height: 1.6; font-weight: 600;">
    Si vous ou quelqu'un que vous connaissez avez besoin d'aide :
    </p>
    <ul style="color: #16A085; margin: 0; padding-left: 1.5rem; line-height: 1.8;">
        <li><strong>3114</strong> : Numéro national de prévention du suicide (France)</li>
        <li><strong>Fil Santé Jeunes</strong> : 0 800 235 236 (gratuit et anonyme)</li>
        <li><strong>SOS Amitié</strong> : 09 72 39 40 50</li>
        <li><strong>Nightline</strong> : Service d'écoute par et pour les étudiants</li>
        <li><strong>Psychologues.fr</strong> : Annuaire de psychologues</li>
    </ul>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# Information sur les services universitaires
st.markdown("### Services Universitaires")

st.markdown("""
<div style="padding: 1.5rem; background-color: rgba(155, 89, 182, 0.15); border-left: 5px solid #9B59B6; border-radius: 8px; margin-bottom: 1rem;">
    <p style="color: #8E44AD; margin: 0 0 1rem 0; font-size: 1rem; line-height: 1.6; font-weight: 600;">
    La plupart des universités proposent :
    </p>
    <ul style="color: #8E44AD; margin: 0 0 1rem 0; padding-left: 1.5rem; line-height: 1.8;">
        <li>Services de santé universitaire (SSU)</li>
        <li>Consultations psychologiques gratuites</li>
        <li>Cellules d'écoute et de soutien</li>
        <li>Aménagements d'études si nécessaire</li>
    </ul>
    <p style="color: #8E44AD; margin: 0; font-size: 0.9rem;">
    Contactez le service de santé de votre établissement pour plus d'informations.
    </p>
</div>
""", unsafe_allow_html=True)

# Footer
st.markdown("---")
st.caption("Student Mental Health Analytics | Projet MBAESG 2025-2026")

st.markdown("""
<div style="padding: 0.8rem; background-color: rgba(231, 76, 60, 0.15); border-left: 5px solid #E74C3C; border-radius: 8px; margin-top: 1rem;">
    <p style="color: #C0392B; margin: 0; font-size: 0.9rem; font-weight: 600; text-align: center;">
     En cas d'urgence, contactez le 15 (SAMU) ou le 112 (numéro d'urgence européen)
    </p>
</div>
""", unsafe_allow_html=True)