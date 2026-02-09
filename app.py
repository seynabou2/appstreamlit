import streamlit as st

# Configuration de la page
st.set_page_config(
    page_title="Dashboard Multi-Datasets",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personnalisé pour un design moderne
st.markdown("""
    <style>
    /* Titre principal */
    .main-title {
        font-size: 3.5rem;
        font-weight: 800;
        background: linear-gradient(120deg, #00A8E1 0%, #9B59B6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.5rem;
        letter-spacing: -1px;
    }
    
    /* Sous-titre */
    .subtitle {
        text-align: center;
        color: #95A5A6;
        font-size: 1.3rem;
        margin-bottom: 3rem;
        font-weight: 300;
    }
    
    /* Carte de dataset */
    .dataset-card {
        background: linear-gradient(135deg, rgba(0, 168, 225, 0.1) 0%, rgba(155, 89, 182, 0.05) 100%);
        border: 2px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 2rem;
        margin: 1rem 0;
        transition: all 0.3s ease;
        cursor: pointer;
        backdrop-filter: blur(10px);
    }
    
    .dataset-card:hover {
        transform: translateY(-5px);
        border-color: rgba(0, 168, 225, 0.5);
        box-shadow: 0 10px 30px rgba(0, 168, 225, 0.2);
    }
    
    .dataset-title {
        font-size: 1.8rem;
        font-weight: 700;
        color: #00A8E1;
        margin-bottom: 0.8rem;
    }
    
    .dataset-description {
        color: #BDC3C7;
        font-size: 1rem;
        line-height: 1.6;
        margin-bottom: 1rem;
    }
    
    .dataset-features {
        display: flex;
        flex-wrap: wrap;
        gap: 0.5rem;
        margin-top: 1rem;
    }
    
    .feature-badge {
        background: rgba(0, 168, 225, 0.2);
        color: #3498DB;
        padding: 0.4rem 0.8rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 500;
    }
    
    /* Section d'introduction */
    .intro-section {
        background: rgba(52, 152, 219, 0.05);
        border-left: 5px solid #3498DB;
        border-radius: 8px;
        padding: 1.5rem;
        margin: 2rem 0;
    }
    
    .intro-text {
        color: #ECF0F1;
        font-size: 1.1rem;
        line-height: 1.8;
        margin: 0;
    }
    
    /* Stats */
    .stat-container {
        display: flex;
        justify-content: space-around;
        margin: 3rem 0;
        flex-wrap: wrap;
        gap: 1rem;
    }
    
    .stat-box {
        text-align: center;
        padding: 1.5rem;
        background: rgba(255, 255, 255, 0.03);
        border-radius: 12px;
        min-width: 150px;
    }
    
    .stat-number {
        font-size: 2.5rem;
        font-weight: 800;
        background: linear-gradient(120deg, #00A8E1 0%, #9B59B6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .stat-label {
        color: #95A5A6;
        font-size: 0.9rem;
        margin-top: 0.5rem;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Tech stack */
    .tech-badge {
        display: inline-block;
        background: rgba(155, 89, 182, 0.2);
        color: #9B59B6;
        padding: 0.5rem 1rem;
        border-radius: 25px;
        margin: 0.3rem;
        font-size: 0.9rem;
        font-weight: 600;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        margin-top: 4rem;
        padding: 2rem 0;
        border-top: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .footer-text {
        color: #7F8C8D;
        font-size: 0.9rem;
    }
    </style>
""", unsafe_allow_html=True)

# En-tête
st.markdown('<h1 class="main-title">Dashboard Multi-Datasets</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Projet Streamlit + DuckDB • Management Opérationnel des Données</p>', unsafe_allow_html=True)

# Section d'introduction
st.markdown("""
<div class="intro-section">
    <p class="intro-text">
    Bienvenue sur notre plateforme d'analyse de données interactive. Cette application permet d'analyser deux datasets distincts 
    avec des visualisations dynamiques, des filtres personnalisables et des insights actionnables alimentés par DuckDB.
    </p>
</div>
""", unsafe_allow_html=True)

# Statistiques clés
st.markdown("""
<div class="stat-container">
    <div class="stat-box">
        <div class="stat-number">2</div>
        <div class="stat-label">Datasets</div>
    </div>
    <div class="stat-box">
        <div class="stat-number">8</div>
        <div class="stat-label">KPI Interactifs</div>
    </div>
    <div class="stat-box">
        <div class="stat-number">100%</div>
        <div class="stat-label">Temps Réel</div>
    </div>
    <div class="stat-box">
        <div class="stat-number">∞</div>
        <div class="stat-label">Possibilités</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# Section des datasets
st.markdown("## Explorez les Datasets")

col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown("""
    <div class="dataset-card">
        <h3 class="dataset-title">Amazon Prime Movies & TV Shows</h3>
        <p class="dataset-description">
        Analyse complète du catalogue de streaming Amazon Prime avec plus de 9 000 titres. 
        Explorez les tendances de production, les genres dominants et la distribution géographique du contenu.
        </p>
        <div class="dataset-features">
            <span class="feature-badge">Distribution par Décennie</span>
            <span class="feature-badge">Top Genres</span>
            <span class="feature-badge">Répartition Géographique</span>
            <span class="feature-badge">Films vs Séries</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("Accéder à Amazon Prime Analytics", use_container_width=True, type="primary"):
        st.switch_page("pages/Amazon_Prime.py")

with col2:
    st.markdown("""
    <div class="dataset-card">
        <h3 class="dataset-title">Student Mental Health</h3>
        <p class="dataset-description">
        Analyse sensible et approfondie de la santé mentale des étudiants. 
        Identifiez les facteurs de risque, analysez les corrélations avec la performance académique et explorez les tendances par genre.
        </p>
        <div class="dataset-features">
            <span class="feature-badge">Vue d'Ensemble Santé Mentale</span>
            <span class="feature-badge">Analyse par Genre</span>
            <span class="feature-badge">Performance Académique</span>
            <span class="feature-badge">Facteurs de Risque</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("Accéder à Mental Health Analytics", use_container_width=True, type="primary"):
        st.switch_page("pages/Mental_Health.py")

st.markdown("---")

# Section caractéristiques
st.markdown("## Fonctionnalités Clés")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    ### Visualisations Interactives
    - Graphiques dynamiques avec Plotly
    - Filtres en temps réel
    - Export des données
    - Insights automatiques
    """)

with col2:
    st.markdown("""
    ### Performance Optimale
    - DuckDB pour requêtes ultra-rapides
    - Architecture modulaire
    - Cache intelligent
    - Scalabilité garantie
    """)

with col3:
    st.markdown("""
    ### Éthique & Sécurité
    - Données anonymisées
    - Ressources d'aide intégrées
    - Conformité RGPD
    - Analyse responsable
    """)

st.markdown("---")

# Section tech stack
st.markdown("##  Stack Technologique")

st.markdown("""
<div style="text-align: center; margin: 2rem 0;">
    <span class="tech-badge">Python 3.13</span>
    <span class="tech-badge">Streamlit</span>
    <span class="tech-badge">DuckDB</span>
    <span class="tech-badge">Plotly</span>
    <span class="tech-badge">Pandas</span>
    <span class="tech-badge">Git</span>
</div>
""", unsafe_allow_html=True)

# Sidebar - Navigation rapide
with st.sidebar:
    st.markdown("### Navigation Rapide")
    st.markdown("Sélectionnez une page dans le menu ci-dessus")
    
    st.markdown("---")
    
    st.markdown("### Ressources")
    st.markdown("""
    - [Documentation Streamlit](https://docs.streamlit.io)
    - [DuckDB](https://duckdb.org)
    - [Plotly](https://plotly.com/python)
    """)
    
    st.markdown("---")
    
    st.markdown("### Équipe Projet")
    st.markdown("""
    **MBA Big Data & IA**  
    École Supérieure de Gestion  
    Promotion 2025-2026
    """)

# Footer
st.markdown("""
<div class="footer">
    <p class="footer-text">
    Développé avec ❤️ par l'équipe MBDIA | Projet Management Opérationnel
    </p>
    <p class="footer-text">
    © 2025-2026 ESG Paris • Tous droits réservés
    </p>
</div>
""", unsafe_allow_html=True)

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
