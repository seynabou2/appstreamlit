import streamlit as st

def render_filters(db):
    """
    Affiche les filtres dans la sidebar pour Mental Health
    
    Args:
        db: Instance de MentalHealthDB
        
    Returns:
        dict: Dictionnaire contenant les valeurs des filtres
    """
    
    st.sidebar.header("Filtres d'Analyse")
    st.sidebar.markdown("Affinez votre analyse en appliquant des filtres")
    
    # Filtre 1 : Genre
    st.sidebar.subheader("Genre")
    
    # Récupérer les genres disponibles
    available_genders = db.get_available_genders()
    
    if available_genders:
        selected_genders = st.sidebar.multiselect(
            "Sélectionnez le(s) genre(s)",
            options=available_genders,
            default=[],
            help="Filtrer par genre des étudiants"
        )
    else:
        selected_genders = []
        st.sidebar.warning("Aucun genre disponible")
    
    # Filtre 2 : Tranche d'âge
    st.sidebar.subheader(" Âge")
    
    # Récupérer la plage d'âges depuis la DB
    age_range_data = db.get_age_range()
    
    if age_range_data is not None and not age_range_data.empty:
        min_age = int(age_range_data['min_age'].iloc[0]) if age_range_data['min_age'].iloc[0] else 18
        max_age = int(age_range_data['max_age'].iloc[0]) if age_range_data['max_age'].iloc[0] else 30
    else:
        min_age, max_age = 18, 30
    
    age_range = st.sidebar.slider(
        "Sélectionnez la tranche d'âge",
        min_value=min_age,
        max_value=max_age,
        value=(min_age, max_age),
        help="Filtrer par âge des étudiants"
    )
    
    # Filtre 3 : Année d'études
    st.sidebar.subheader("Année d'Études")
    
    # Récupérer les années disponibles
    available_years = db.get_available_years()
    
    if available_years:
        selected_years = st.sidebar.multiselect(
            "Sélectionnez l'année d'études",
            options=available_years,
            default=[],
            help="Filtrer par année d'études (Year 1, Year 2, etc.)"
        )
    else:
        selected_years = []
        st.sidebar.info("Aucune année d'études disponible")
    
    # Bouton de réinitialisation
    st.sidebar.markdown("---")
    if st.sidebar.button("Réinitialiser tous les filtres", use_container_width=True):
        st.rerun()
    
    # Retourner le dictionnaire de filtres
    filters = {
        'gender': selected_genders if selected_genders else None,
        'age_range': age_range,
        'year': selected_years if selected_years else None
    }
    
    # Afficher un résumé des filtres actifs
    active_filters = []
    if selected_genders:
        active_filters.append(f"Genre: {', '.join(selected_genders)}")
    if age_range != (min_age, max_age):
        active_filters.append(f"Âge: {age_range[0]}-{age_range[1]} ans")
    if selected_years:
        active_filters.append(f"Année: {', '.join(map(str, selected_years))}")
    
    if active_filters:
        st.sidebar.success(f"{len(active_filters)} filtre(s) actif(s)")
        with st.sidebar.expander("Voir les filtres actifs"):
            for f in active_filters:
                st.sidebar.write(f"• {f}")
    else:
        st.sidebar.info("ℹAucun filtre appliqué")
    
    # Informations supplémentaires
    st.sidebar.markdown("---")
    st.sidebar.markdown("### À propos des données")
    st.sidebar.caption("""
    Les données analysées proviennent d'une enquête sur la santé mentale 
    des étudiants universitaires. Les résultats sont anonymisés et à usage pédagogique uniquement.
    """)
    
    return filters