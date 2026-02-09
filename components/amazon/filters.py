import streamlit as st
from typing import Dict, Any

def render_filters(db) -> Dict[str, Any]:
    """
    Affiche les filtres dans la sidebar et retourne les valeurs sélectionnées.
    
    Args:
        db: Instance de AmazonPrimeDB
        
    Returns:
        Dict contenant les filtres sélectionnés
    """
    st.sidebar.header("Filtres")
    
    filters = {}
    
    # Filtre par type de contenu
    st.sidebar.subheader("Type de Contenu")
    content_types = db.get_unique_values('type')
    filters['content_type'] = st.sidebar.multiselect(
        "Sélectionnez le type",
        options=['Tous'] + content_types,
        default=['Tous']
    )
    
    # Filtre par année de sortie
    st.sidebar.subheader("Année de Sortie")
    min_year, max_year = db.get_year_range()
    if min_year and max_year:
        filters['year_range'] = st.sidebar.slider(
            "Plage d'années",
            min_value=int(min_year),
            max_value=int(max_year),
            value=(int(min_year), int(max_year))
        )
    else:
        filters['year_range'] = None
    
    # Filtre par rating
    st.sidebar.subheader("Classification")
    ratings = db.get_unique_values('rating')
    filters['rating'] = st.sidebar.multiselect(
        "Sélectionnez les classifications",
        options=['Tous'] + ratings,
        default=['Tous']
    )
    
    # Filtre par pays
    st.sidebar.subheader("Pays de Production")
    countries = db.get_top_countries(20)  # Top 20 pays
    filters['country'] = st.sidebar.multiselect(
        "Sélectionnez les pays",
        options=['Tous'] + countries,
        default=['Tous']
    )
    
    # Filtre par genre
    st.sidebar.subheader("Genres")
    genres = db.get_top_genres(15)  # Top 15 genres
    filters['genre'] = st.sidebar.multiselect(
        "Sélectionnez les genres",
        options=['Tous'] + genres,
        default=['Tous']
    )
    
    # Bouton reset
    st.sidebar.markdown("---")
    if st.sidebar.button("Réinitialiser les filtres"):
        st.rerun()
    
    return filters