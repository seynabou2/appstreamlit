import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd

def render_all_kpis(db, filters):
    """
    Affiche tous les KPI pour Student Mental Health
    
    Args:
        db: Instance de MentalHealthDB
        filters: Dictionnaire des filtres actifs
    """
    
    st.header("📊 Tableau de Bord - Indicateurs Clés")
    
    # KPI 1 : Vue d'ensemble de la santé mentale
    render_kpi_mental_health_overview(db, filters)
    
    st.markdown("---")
    
    # KPI 2 et 3 côte à côte
    col1, col2 = st.columns(2)
    
    with col1:
        render_kpi_gender_analysis(db, filters)
    
    with col2:
        render_kpi_performance_correlation(db, filters)
    
    st.markdown("---")
    
    # KPI 4 : Facteurs de risque
    render_kpi_risk_factors(db, filters)


def render_kpi_mental_health_overview(db, filters):
    """KPI 1 : Vue d'ensemble de la santé mentale"""
    
    st.subheader("📊 KPI 1 : Vue d'Ensemble de la Santé Mentale")
    
    # Récupérer les données
    df = db.get_mental_health_summary(filters)
    
    if df.empty:
        st.warning("Aucune donnée disponible pour cette visualisation")
        return
    
    # Extraire les données
    total_students = int(df['total_students'].iloc[0])
    depression_count = int(df['depression_count'].iloc[0])
    anxiety_count = int(df['anxiety_count'].iloc[0])
    panic_count = int(df['panic_count'].iloc[0])
    treatment_count = int(df['treatment_count'].iloc[0])
    
    depression_pct = df['depression_pct'].iloc[0]
    anxiety_pct = df['anxiety_pct'].iloc[0]
    panic_pct = df['panic_pct'].iloc[0]
    
    # Métriques en haut
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "👥 Total Étudiants",
            f"{total_students}",
            help="Nombre total d'étudiants dans l'échantillon"
        )
    
    with col2:
        st.metric(
            "😔 Dépression",
            f"{depression_count}",
            f"{depression_pct}%",
            delta_color="inverse",
            help="Étudiants souffrant de dépression"
        )
    
    with col3:
        st.metric(
            "😰 Anxiété",
            f"{anxiety_count}",
            f"{anxiety_pct}%",
            delta_color="inverse",
            help="Étudiants souffrant d'anxiété"
        )
    
    with col4:
        st.metric(
            "😱 Attaques de Panique",
            f"{panic_count}",
            f"{panic_pct}%",
            delta_color="inverse",
            help="Étudiants ayant des attaques de panique"
        )
    
    # Graphique en barres
    conditions_data = pd.DataFrame({
        'Condition': ['Dépression', 'Anxiété', 'Attaques de Panique'],
        'Nombre': [depression_count, anxiety_count, panic_count],
        'Pourcentage': [depression_pct, anxiety_pct, panic_pct]
    })
    
    fig = px.bar(
        conditions_data,
        x='Condition',
        y='Nombre',
        text='Pourcentage',
        title='Répartition des Conditions de Santé Mentale',
        labels={'Nombre': 'Nombre d\'Étudiants', 'Condition': 'Type de Condition'},
        color='Condition',
        color_discrete_map={
            'Dépression': '#E74C3C',
            'Anxiété': '#F39C12',
            'Attaques de Panique': '#E67E22'
        }
    )
    
    fig.update_traces(
        texttemplate='%{text:.1f}%',
        textposition='outside'
    )
    
    fig.update_layout(
        height=400,
        showlegend=False,
        yaxis_title="Nombre d'Étudiants"
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Insights
    col1, col2 = st.columns(2)
    
    with col1:
        # Condition la plus fréquente
        max_condition = conditions_data.loc[conditions_data['Nombre'].idxmax()]
        st.info(f"⚠️ **Condition la plus fréquente** : {max_condition['Condition']} ({max_condition['Pourcentage']:.1f}%)")
    
    with col2:
        # Taux de traitement
        treatment_pct = (treatment_count / total_students) * 100
        st.success(f"💊 **Taux de traitement** : {treatment_pct:.1f}% des étudiants suivent un traitement")


def render_kpi_gender_analysis(db, filters):
    """KPI 2 : Analyse par genre"""
    
    st.subheader("👥 KPI 2 : Analyse par Genre")
    
    # Récupérer les données
    df = db.get_health_by_gender(filters)
    
    if df.empty:
        st.warning("Aucune donnée disponible pour cette visualisation")
        return
    
    # Préparer les données pour le graphique groupé
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        name='Dépression',
        x=df['gender'],
        y=df['depression_pct'],
        marker_color='#E74C3C',
        text=df['depression_pct'].apply(lambda x: f'{x:.1f}%'),
        textposition='outside'
    ))
    
    fig.add_trace(go.Bar(
        name='Anxiété',
        x=df['gender'],
        y=df['anxiety_pct'],
        marker_color='#F39C12',
        text=df['anxiety_pct'].apply(lambda x: f'{x:.1f}%'),
        textposition='outside'
    ))
    
    fig.add_trace(go.Bar(
        name='Attaques de Panique',
        x=df['gender'],
        y=df['panic_pct'],
        marker_color='#E67E22',
        text=df['panic_pct'].apply(lambda x: f'{x:.1f}%'),
        textposition='outside'
    ))
    
    fig.update_layout(
        title='Taux de Prévalence par Genre',
        xaxis_title='Genre',
        yaxis_title='Pourcentage (%)',
        barmode='group',
        height=400,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Tableau détaillé
    with st.expander("📊 Voir les données détaillées"):
        display_df = df[['gender', 'total_students', 'depression_pct', 'anxiety_pct', 'panic_pct']].copy()
        display_df.columns = ['Genre', 'Total Étudiants', 'Dépression (%)', 'Anxiété (%)', 'Attaques de Panique (%)']
        st.dataframe(display_df, use_container_width=True, hide_index=True)
    
    # Insight
    if len(df) >= 2:
        max_depression_gender = df.loc[df['depression_pct'].idxmax(), 'gender']
        max_depression_pct = df['depression_pct'].max()
        st.warning(f"⚠️ Le genre **{max_depression_gender}** présente le taux de dépression le plus élevé ({max_depression_pct:.1f}%)")


def render_kpi_performance_correlation(db, filters):
    """KPI 3 : Corrélation performance académique vs santé mentale"""
    
    st.subheader("📈 KPI 3 : Performance Académique vs Santé Mentale")
    
    # Récupérer les données
    df = db.get_performance_correlation(filters)
    
    if df.empty:
        st.warning("Aucune donnée disponible pour cette visualisation")
        return
    
    # Créer une colonne combinée pour la couleur
    df['condition'] = df.apply(lambda row: 
        'Dépression' if row['depression'] == 'Yes' 
        else 'Anxiété' if row['anxiety'] == 'Yes'
        else 'Attaque de panique' if row['panic_attack'] == 'Yes'
        else 'Aucune condition', axis=1
    )
    
    # Scatter plot
    fig = px.scatter(
        df,
        x='cgpa',
        y='age',
        color='condition',
        size=[5]*len(df),  # Taille uniforme
        title='Distribution CGPA par Condition de Santé Mentale',
        labels={
            'cgpa': 'CGPA (Performance Académique)',
            'age': 'Âge',
            'condition': 'Condition'
        },
        color_discrete_map={
            'Dépression': '#E74C3C',
            'Anxiété': '#F39C12',
            'Attaque de panique': '#E67E22',
            'Aucune condition': '#27AE60'
        },
        hover_data=['gender', 'treatment']
    )
    
    fig.update_layout(
        height=400,
        showlegend=True,
        legend=dict(
            orientation="v",
            yanchor="top",
            y=1,
            xanchor="left",
            x=1.02
        )
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Statistiques CGPA par condition
    cgpa_stats_df = db.get_cgpa_by_mental_health(filters)
    
    if not cgpa_stats_df.empty:
        with st.expander("📊 CGPA Moyen par Condition"):
            # Filtrer pour avoir une ligne par condition
            summary = cgpa_stats_df.groupby(['condition', 'status']).agg({
                'avg_cgpa': 'mean',
                'student_count': 'sum'
            }).reset_index()
            
            st.dataframe(summary, use_container_width=True, hide_index=True)
    
    # Insight
    avg_cgpa_all = df['cgpa'].mean()
    avg_cgpa_depression = df[df['depression'] == 'Yes']['cgpa'].mean() if 'Yes' in df['depression'].values else 0
    
    if avg_cgpa_depression > 0:
        diff = avg_cgpa_all - avg_cgpa_depression
        if diff > 0:
            st.info(f"📉 Les étudiants avec dépression ont un CGPA moyen inférieur de **{diff:.2f}** points")
        else:
            st.success(f"📈 Pas d'impact significatif observé sur le CGPA")


def render_kpi_risk_factors(db, filters):
    """KPI 4 : Facteurs de risque et traitement"""
    
    st.subheader("⚠️ KPI 4 : Facteurs de Risque et Traitement")
    
    # Récupérer les données
    df_risk = db.get_risk_factors_distribution(filters)
    df_treatment = db.get_treatment_analysis(filters)
    
    if df_risk.empty:
        st.warning("Aucune donnée disponible pour cette visualisation")
        return
    
    # Graphique 1 : Distribution des facteurs de risque (Donut charts)
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Distribution des Conditions")
        
        # Filtrer pour avoir uniquement Yes/No par condition
        depression_data = df_risk[df_risk['category'] == 'Depression']
        
        if not depression_data.empty:
            fig = go.Figure(data=[go.Pie(
                labels=depression_data['status'],
                values=depression_data['count'],
                hole=0.5,
                marker_colors=['#E74C3C', '#27AE60'],
                textinfo='label+percent',
                textposition='outside'
            )])
            
            fig.update_layout(
                title='Dépression',
                height=300,
                showlegend=True,
                margin=dict(t=50, b=0, l=0, r=0)
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        if not df_treatment.empty:
            st.markdown("#### Analyse du Traitement")
            
            # Donut chart pour le traitement
            fig = go.Figure(data=[go.Pie(
                labels=df_treatment['treatment'],
                values=df_treatment['total_students'],
                hole=0.5,
                marker_colors=['#3498DB', '#95A5A6'],
                textinfo='label+percent',
                textposition='outside'
            )])
            
            fig.update_layout(
                title='Taux de Traitement',
                height=300,
                showlegend=True,
                margin=dict(t=50, b=0, l=0, r=0)
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    # Graphique 2 : Tableau récapitulatif
    st.markdown("#### Récapitulatif des Conditions")
    
    # Créer un tableau pivot
    pivot_data = []
    for category in ['Depression', 'Anxiety', 'Panic Attack']:
        cat_data = df_risk[df_risk['category'] == category]
        yes_data = cat_data[cat_data['status'] == 'Yes']
        
        if not yes_data.empty:
            pivot_data.append({
                'Condition': category,
                'Nombre (Yes)': int(yes_data['count'].iloc[0]),
                'Pourcentage': f"{yes_data['percentage'].iloc[0]:.1f}%"
            })
    
    if pivot_data:
        pivot_df = pd.DataFrame(pivot_data)
        
        # Créer un bar chart horizontal
        fig = px.bar(
            pivot_df,
            y='Condition',
            x='Nombre (Yes)',
            orientation='h',
            text='Pourcentage',
            title='Nombre d\'Étudiants Affectés par Condition',
            color='Condition',
            color_discrete_map={
                'Depression': '#E74C3C',
                'Anxiety': '#F39C12',
                'Panic Attack': '#E67E22'
            }
        )
        
        fig.update_traces(textposition='outside')
        fig.update_layout(
            height=300,
            showlegend=False,
            xaxis_title="Nombre d'Étudiants"
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Insights finaux
    if not df_treatment.empty:
        treatment_yes = df_treatment[df_treatment['treatment'] == 'Yes']
        if not treatment_yes.empty:
            treatment_students = int(treatment_yes['total_students'].iloc[0])
            total_students = int(df_treatment['total_students'].sum())
            treatment_pct = (treatment_students / total_students) * 100
            
            col1, col2 = st.columns(2)
            
            with col1:
                if treatment_pct < 50:
                    st.error(f"⚠️ Seulement **{treatment_pct:.1f}%** des étudiants suivent un traitement")
                else:
                    st.success(f"✅ **{treatment_pct:.1f}%** des étudiants suivent un traitement")
            
            with col2:
                # CGPA des étudiants en traitement vs sans traitement
                if 'avg_cgpa' in treatment_yes.columns:
                    treatment_cgpa = treatment_yes['avg_cgpa'].iloc[0]
                    no_treatment = df_treatment[df_treatment['treatment'] == 'No']
                    if not no_treatment.empty:
                        no_treatment_cgpa = no_treatment['avg_cgpa'].iloc[0]
                        diff = treatment_cgpa - no_treatment_cgpa
                        if diff > 0:st.info(f"📚 CGPA moyen avec traitement : {treatment_cgpa:.2f} (+{diff:.2f})")
                    else:
                        st.info(f"📚 CGPA moyen avec traitement : {treatment_cgpa:.2f}")
                else:
                    st.info("ℹ️ Aucune donnée de CGPA disponible")
    else:
        st.info("ℹ️ Aucune donnée de traitement disponible")