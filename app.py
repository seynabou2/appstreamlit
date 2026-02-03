import streamlit as st

# Configuration de la page
st.set_page_config(
    page_title="Multi-Dataset Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personnalisé
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .dataset-card {
        padding: 2rem;
        border-radius: 10px;
        background-color: #f0f2f6;
        margin: 1rem 0;
    }
    .feature-list {
        font-size: 1.1rem;
        line-height: 2rem;
    }
    </style>
""", unsafe_allow_html=True)

# En-tête principal
st.markdown('<h1 class="main-header">Dashboard Multi-Datasets</h1>', unsafe_allow_html=True)
st.markdown("### Projet Streamlit + DuckDB - Management Opérationnel")
st.markdown("---")

# Introduction
st.write("""
Bienvenue sur notre plateforme d'analyse de données interactive. 
Cette application permet d'analyser deux datasets distincts avec des visualisations dynamiques 
et des filtres personnalisables.
""")

st.markdown("---")

# Section des datasets
col1, col2 = st.columns(2)

with col1:
    st.markdown("### Amazon Prime Movies & TV Shows")
    
    st.markdown("""
    <div class="dataset-card">
        <h4>Analyse complète du catalogue Amazon Prime</h4>
        <ul class="feature-list">
            <li>Évolution temporelle du contenu</li>
            <li>Distribution par genres</li>
            <li>Répartition géographique</li>
            <li>Comparaison Films vs Séries</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("Analyser Amazon Prime", use_container_width=True, type="primary"):
        st.switch_page("pages/Amazon_Prime.py")

with col2:
    st.markdown("###Student Mental Health")
    
    st.markdown("""
    <div class="dataset-card">
        <h4>Analyse de la santé mentale des étudiants</h4>
        <ul class="feature-list">
            <li>Distribution du stress</li>
            <li>Analyse par genre</li>
            <li>Corrélation performance/santé</li>
            <li>Identification des facteurs de risque</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("Analyser Mental Health", use_container_width=True, type="primary"):
        st.switch_page("pages/Mental_Health.py")

st.markdown("---")

# Instructions
st.info("""
**Instructions d'utilisation :**
1. Choisissez un dataset à analyser en cliquant sur le bouton correspondant
2. Uploadez le fichier CSV du dataset sélectionné
3. Utilisez les filtres dans la barre latérale pour affiner votre analyse
4. Explorez les 4 indicateurs clés de performance (KPI) avec des visualisations interactives
""")

# Footer avec informations sur l'équipe
st.markdown("---")
st.markdown("### Notre Équipe")

team_col1, team_col2, team_col3, team_col4 = st.columns(4)

with team_col1:
    st.markdown("""
    **Seynabou SENE**  
     Chef de Projet  
    Amazon Backend
    """)

with team_col2:
    st.markdown("""
    **Mame Diarra NDIAYE**  
    Frontend  
    Amazon Visualisations
    """)

with team_col3:
    st.markdown("""
    **Emeric GNANVI**  
    Backend  
    Mental Health Database
    """)

with team_col4:
    st.markdown("""
    **Pla Ayebie DORGELES**  
    Frontend  
    Mental Health Visualisations
    """)

# Version et date
st.markdown("---")  
st.caption("Version 1.0 | Projet MBAESG 2024-2025")