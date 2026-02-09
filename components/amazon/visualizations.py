import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

def render_all_kpis(db, filters):
    """
    Affiche tous les KPI pour Amazon Prime
    
    Args:
        db: Instance de AmazonPrimeDB
        filters: Dictionnaire des filtres actifs
    """
    
    st.header("Tableau de Bord - Indicateurs Clés")
    
    # KPI 1 : Évolution du Catalogue par Décennie
    render_kpi_evolution(db, filters)
    
    st.markdown("---")
    
    # KPI 2 et 3 côte à côte
    col1, col2 = st.columns(2)
    
    with col1:
        render_kpi_genres(db, filters)
    
    with col2:
        render_kpi_geography(db, filters)
    
    st.markdown("---")
    
    # KPI 4 : Films vs Séries
    render_kpi_comparison(db, filters)


def render_kpi_evolution(db, filters):
    """KPI 1 : Distribution du contenu par décennie de production"""
    
    st.subheader("Évolution de la Production Cinématographique")
    
    # Récupérer les données
    df = db.get_content_by_decade(filters)
    
    if df.empty:
        st.warning("Aucune donnée disponible pour cette visualisation")
        return
    
    # Créer un graphique en barres groupées
    fig = go.Figure()
    
    # Barres pour les films
    fig.add_trace(go.Bar(
        x=df['decade_label'],
        y=df['nb_movies'],
        name='Films',
        marker_color='#00A8E1',
        text=df['nb_movies'],
        textposition='auto',
        hovertemplate='<b>%{x}</b><br>Films: %{y}<extra></extra>'
    ))
    
    # Barres pour les séries
    fig.add_trace(go.Bar(
        x=df['decade_label'],
        y=df['nb_shows'],
        name='Séries TV',
        marker_color='#FF9900',
        text=df['nb_shows'],
        textposition='auto',
        hovertemplate='<b>%{x}</b><br>Séries: %{y}<extra></extra>'
    ))
    
    # Configuration du graphique
    fig.update_layout(
        title='Distribution du Catalogue par Décennie de Production',
        xaxis_title='Décennie',
        yaxis_title='Nombre de Contenus',
        barmode='group',
        height=450,
        hovermode='x unified',
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Insights automatiques
    total_content = df['total_content'].sum()
    max_decade = df.loc[df['total_content'].idxmax(), 'decade_label']
    max_content = df['total_content'].max()
    
    # Calculer la décennie dominante pour les films et séries
    top_movie_decade = df.loc[df['nb_movies'].idxmax(), 'decade_label']
    top_show_decade = df.loc[df['nb_shows'].idxmax(), 'decade_label']
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "Décennie Leader",
            max_decade,
            f"{int(max_content)} contenus",
            help="Décennie la plus représentée dans le catalogue"
        )
    
    with col2:
        st.metric(
            "Décennies Représentées",
            len(df),
            help="Nombre total de décennies couvertes"
        )
    
    with col3:
        oldest_decade = df['decade_label'].iloc[0]
        newest_decade = df['decade_label'].iloc[-1]
        st.metric(
            "Période Couverte",
            f"{oldest_decade} - {newest_decade}",
            help="Du contenu le plus ancien au plus récent"
        )
    
    # Insight supplémentaire
    st.info(f"**Films** : Pic dans les **{top_movie_decade}** | **Séries TV** : Pic dans les **{top_show_decade}**")


def render_kpi_genres(db, filters):
    """KPI 2 : Top 10 des genres"""
    
    st.subheader("Top 10 des Genres")
    
    # Récupérer les données
    df = db.get_top_genres(limit=10, filters=filters)
    
    if df.empty:
        st.warning("Aucune donnée disponible pour cette visualisation")
        return
    
    # Créer le graphique en barres horizontales avec dégradé de couleur
    fig = px.bar(
        df,
        x='nb_content',
        y='genre',
        orientation='h',
        title='Genres les Plus Représentés',
        labels={'nb_content': 'Nombre de Contenus', 'genre': 'Genre'},
        color='nb_content',
        color_continuous_scale='Teal',
        text='nb_content'
    )
    
    # Configuration du graphique
    fig.update_layout(
        yaxis={'categoryorder': 'total ascending'},
        height=400,
        showlegend=False
    )
    
    fig.update_traces(
        texttemplate='%{text}', 
        textposition='outside',
        marker=dict(
            line=dict(color='rgba(255,255,255,0.3)', width=1)
        )
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Insights
    top_genre = df.iloc[0]
    total_top10 = df['nb_content'].sum()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric(
            "Genre #1",
            top_genre['genre'],
            f"{int(top_genre['nb_content'])} contenus"
        )
    
    with col2:
        st.metric(
            "Top 10 Genres",
            f"{int(total_top10)} contenus",
            help="Total des 10 genres les plus populaires"
        )


def render_kpi_geography(db, filters):
    """KPI 3 : Répartition géographique"""
    
    st.subheader("Répartition Géographique")
    
    # Récupérer les données
    df = db.get_countries_distribution(limit=15, filters=filters)
    
    if df.empty:
        st.warning("Aucune donnée disponible pour cette visualisation")
        return
    
    # Créer un treemap
    fig = px.treemap(
        df,
        path=['country'],
        values='nb_content',
        title='Top 15 Pays de Production',
        color='nb_content',
        color_continuous_scale='Viridis',
        hover_data={'nb_content': True, 'percentage': ':.2f'}
    )
    
    fig.update_layout(height=400)
    fig.update_traces(
        textposition='middle center',
        textfont=dict(size=14, color='white', family='Arial Black')
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Insights
    top_country = df.iloc[0]
    total_countries = len(df)
    top3_percentage = df.head(3)['percentage'].sum()
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "Pays Leader",
            top_country['country'],
            f"{top_country['percentage']:.1f}%"
        )
    
    with col2:
        st.metric(
            "Top 3 Pays",
            f"{top3_percentage:.1f}%",
            help="Part du catalogue des 3 premiers pays"
        )
    
    with col3:
        st.metric(
            "Pays Représentés",
            f"{total_countries}"
        )


def render_kpi_comparison(db, filters):
    """KPI 4 : Comparaison Films vs Séries"""
    
    st.subheader("Films vs Séries TV")
    
    # Récupérer les données
    df = db.get_movies_vs_shows(filters=filters)
    
    if df.empty:
        st.warning("Aucune donnée disponible pour cette visualisation")
        return
    
    # Extraire les données
    movies_data = df[df['type'] == 'Movie']
    shows_data = df[df['type'] == 'TV Show']
    
    total_movies = int(movies_data['total'].iloc[0]) if not movies_data.empty else 0
    total_shows = int(shows_data['total'].iloc[0]) if not shows_data.empty else 0
    
    # Layout avec métriques et graphiques
    col1, col2 = st.columns([1, 1])
    
    with col1:
        # Métriques
        st.markdown("### Statistiques Globales")
        
        metric_col1, metric_col2 = st.columns(2)
        
        with metric_col1:
            st.metric("Films", f"{total_movies:,}")
            if not movies_data.empty:
                oldest_movie = int(movies_data['oldest_year'].iloc[0])
                newest_movie = int(movies_data['newest_year'].iloc[0])
                st.caption(f"Période: {oldest_movie}-{newest_movie}")
        
        with metric_col2:
            st.metric(" Séries", f"{total_shows:,}")
            if not shows_data.empty:
                oldest_show = int(shows_data['oldest_year'].iloc[0])
                newest_show = int(shows_data['newest_year'].iloc[0])
                st.caption(f"Période: {oldest_show}-{newest_show}")
        
        # Ratio
        if total_shows > 0:
            ratio = total_movies / total_shows
            st.metric(
                "Ratio Films/Séries", 
                f"{ratio:.2f}:1",
                help="Nombre de films pour 1 série"
            )
    
    with col2:
        # Graphique en donut
        fig = go.Figure(data=[go.Pie(
            labels=['Films', 'Séries TV'],
            values=[total_movies, total_shows],
            hole=0.6,
            marker_colors=['#00A8E1', '#FF9900'],
            textinfo='label+percent',
            textposition='outside',
            textfont=dict(size=14),
            pull=[0.05, 0]  # Légère séparation pour le segment dominant
        )])
        
        fig.update_layout(
            title='Répartition du Catalogue',
            height=350,
            showlegend=False,
            annotations=[dict(
                text=f'{total_movies + total_shows:,}<br>Contenus',
                x=0.5, y=0.5,
                font_size=20,
                showarrow=False
            )]
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Insight détaillé
    if total_movies > total_shows:
        dominant = "Films"
        percentage = (total_movies / (total_movies + total_shows)) * 100
    else:
        dominant = "Séries TV"
        percentage = (total_shows / (total_movies + total_shows)) * 100
       
    
    st.success(f"**Insight** : Les {dominant} dominent le catalogue avec **{percentage:.1f}%** du contenu total")
    
    # Comparaison de la diversité temporelle
    if not movies_data.empty and not shows_data.empty:
        movie_span = int(movies_data['year_range'].iloc[0])
        show_span = int(shows_data['year_range'].iloc[0])
        
        st.info(f"**Diversité temporelle** : Films couvrent **{movie_span} années** différentes | Séries couvrent **{show_span} années** différentes")