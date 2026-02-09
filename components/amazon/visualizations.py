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
    
    st.header("📊 Tableau de Bord - Indicateurs Clés")
    
    # KPI 1 : Évolution du Catalogue
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
    """KPI 1 : Évolution du contenu dans le temps"""
    
    st.subheader("📈 KPI 1 : Évolution du Catalogue Amazon Prime")
    
    # Récupérer les données
    df = db.get_content_evolution(filters)
    
    if df.empty:
        st.warning("Aucune donnée disponible pour cette visualisation")
        return
    
    # Créer le graphique
    fig = go.Figure()
    
    # Ligne pour le total
    fig.add_trace(go.Scatter(
        x=df['year'],
        y=df['total_content'],
        mode='lines+markers',
        name='Total Contenu',
        line=dict(color='#00A8E1', width=3),
        marker=dict(size=8),
        hovertemplate='<b>Année %{x}</b><br>Total: %{y}<extra></extra>'
    ))
    
    # Ligne pour les films
    fig.add_trace(go.Scatter(
        x=df['year'],
        y=df['nb_movies'],
        mode='lines+markers',
        name='Films',
        line=dict(color='#FF9900', width=2, dash='dash'),
        marker=dict(size=6),
        hovertemplate='<b>Année %{x}</b><br>Films: %{y}<extra></extra>'
    ))
    
    # Ligne pour les séries
    fig.add_trace(go.Scatter(
        x=df['year'],
        y=df['nb_shows'],
        mode='lines+markers',
        name='Séries TV',
        line=dict(color='#1DB954', width=2, dash='dash'),
        marker=dict(size=6),
        hovertemplate='<b>Année %{x}</b><br>Séries: %{y}<extra></extra>'
    ))
    
    # Configuration du graphique
    fig.update_layout(
        title='Croissance du Catalogue par Année',
        xaxis_title='Année d\'Ajout',
        yaxis_title='Nombre de Contenus',
        hovermode='x unified',
        height=450,
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
    avg_per_year = df['total_content'].mean()
    max_year = df.loc[df['total_content'].idxmax(), 'year']
    max_content = df['total_content'].max()
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "Total Contenu Ajouté",
            f"{int(total_content):,}",
            help="Nombre total de contenus sur la période"
        )
    
    with col2:
        st.metric(
            "Moyenne par An",
            f"{int(avg_per_year):,}",
            help="Nombre moyen de contenus ajoutés chaque année"
        )
    
    with col3:
        st.metric(
            "Année Record",
            f"{int(max_year)} ({int(max_content)} contenus)",
            help="Année avec le plus d'ajouts"
        )


def render_kpi_genres(db, filters):
    """KPI 2 : Top 10 des genres"""
    
    st.subheader("🎭 KPI 2 : Top 10 des Genres")
    
    # Récupérer les données
    df = db.get_top_genres(limit=10, filters=filters)
    
    if df.empty:
        st.warning("Aucune donnée disponible pour cette visualisation")
        return
    
    # Créer le graphique en barres horizontales
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
    
    fig.update_traces(texttemplate='%{text}', textposition='outside')
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Insight
    top_genre = df.iloc[0]
    st.info(f"🥇 **Genre leader** : {top_genre['genre']} avec {int(top_genre['nb_content'])} contenus")


def render_kpi_geography(db, filters):
    """KPI 3 : Répartition géographique"""
    
    st.subheader("🌍 KPI 3 : Répartition Géographique")
    
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
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Insights
    top_country = df.iloc[0]
    total_countries = len(df)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric(
            "Pays Leader",
            top_country['country'],
            f"{top_country['percentage']:.1f}%"
        )
    
    with col2:
        st.metric(
            "Pays Représentés",
            f"{total_countries}"
        )


def render_kpi_comparison(db, filters):
    """KPI 4 : Comparaison Films vs Séries"""
    
    st.subheader("🎬 KPI 4 : Films vs Séries TV")
    
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
    
    # Métriques en haut
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("🎬 Total Films", f"{total_movies:,}")
    
    with col2:
        st.metric("📺 Total Séries", f"{total_shows:,}")
    
    with col3:
        if total_shows > 0:
            ratio = total_movies / total_shows
            st.metric("📊 Ratio Films/Séries", f"{ratio:.2f}:1")
        else:
            st.metric("📊 Ratio Films/Séries", "N/A")
    
    # Graphique en donut
    fig = go.Figure(data=[go.Pie(
        labels=['Films', 'Séries TV'],
        values=[total_movies, total_shows],
        hole=0.5,
        marker_colors=['#00A8E1', '#FF9900'],
        textinfo='label+percent',
        textposition='outside'
    )])
    
    fig.update_layout(
        title='Répartition Films vs Séries TV',
        height=400,
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.1,
            xanchor="center",
            x=0.5
        )
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Insight
    if total_movies > total_shows:
        dominant = "Films"
        percentage = (total_movies / (total_movies + total_shows)) * 100
    else:
        dominant = "Séries TV"
        percentage = (total_shows / (total_movies + total_shows)) * 100
    
    st.success(f"📌 **Insight** : Les {dominant} dominent le catalogue avec {percentage:.1f}% du contenu total")