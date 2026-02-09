import duckdb
import pandas as pd
import streamlit as st
from pathlib import Path

class MentalHealthDB:
    """Gestionnaire de base de données pour Student Mental Health"""
    
    def __init__(self):
        """Initialise la connexion à la base de données"""
        # Créer le dossier data s'il n'existe pas
        Path("data").mkdir(exist_ok=True)
        
        # Connexion à DuckDB
        self.conn = duckdb.connect('data/mental_health.db')
        self.table_name = 'health_data'
    
    def load_csv(self, uploaded_file):
        """
        Charge un fichier CSV dans DuckDB
        
        Args:
            uploaded_file: Fichier uploadé via Streamlit
            
        Returns:
            DataFrame pandas avec les données chargées
        """
        try:
            # Lecture du CSV
            df = pd.read_csv(uploaded_file)
            
            # Nettoyage des données
            df = self._clean_data(df)
            
            # Création de la table dans DuckDB
            self.conn.execute(f"""
                CREATE OR REPLACE TABLE {self.table_name} AS 
                SELECT * FROM df
            """)
            
            st.success(f"✅ {len(df)} lignes chargées avec succès dans la base de données!")
            
            # Afficher un aperçu des données
            with st.expander("👀 Aperçu des données chargées"):
                st.dataframe(df.head(10), use_container_width=True)
                st.write(f"**Nombre total de lignes :** {len(df)}")
                st.write(f"**Nombre de colonnes :** {len(df.columns)}")
                st.write(f"**Colonnes disponibles :** {', '.join(df.columns)}")
            
            return df
            
        except Exception as e:
            st.error(f"❌ Erreur lors du chargement du fichier : {str(e)}")
            return None
    
    def _clean_data(self, df):
        """Nettoie et prépare les données"""
        # Normaliser les noms de colonnes (enlever espaces et mettre en minuscules)
        df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
        
        # Convertir les colonnes numériques si nécessaire
        numeric_columns = ['age', 'cgpa']
        for col in numeric_columns:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # Nettoyer les valeurs textuelles
        text_columns = ['gender', 'year', 'course', 'depression', 'anxiety', 'panic_attack', 'treatment']
        for col in text_columns:
            if col in df.columns:
                df[col] = df[col].astype(str).str.strip()
        
        return df
    
    def get_mental_health_summary(self, filters=None):
        """
        KPI 1 : Résumé de la santé mentale (Dépression, Anxiété, Attaques de panique)
        
        Args:
            filters: Dictionnaire des filtres à appliquer
            
        Returns:
            DataFrame avec les comptages pour chaque condition
        """
        query = f"""
            SELECT 
                COUNT(*) as total_students,
                SUM(CASE WHEN depression = 'Yes' THEN 1 ELSE 0 END) as depression_count,
                SUM(CASE WHEN anxiety = 'Yes' THEN 1 ELSE 0 END) as anxiety_count,
                SUM(CASE WHEN panic_attack = 'Yes' THEN 1 ELSE 0 END) as panic_count,
                SUM(CASE WHEN treatment = 'Yes' THEN 1 ELSE 0 END) as treatment_count,
                ROUND(SUM(CASE WHEN depression = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as depression_pct,
                ROUND(SUM(CASE WHEN anxiety = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as anxiety_pct,
                ROUND(SUM(CASE WHEN panic_attack = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as panic_pct
            FROM {self.table_name}
            WHERE 1=1
        """
        
        if filters:
            query += self._build_filter_clause(filters)
        
        try:
            result = self.conn.execute(query).fetchdf()
            return result
        except Exception as e:
            st.error(f"Erreur lors de l'exécution de la requête : {str(e)}")
            return pd.DataFrame()
    
    def get_health_by_gender(self, filters=None):
        """
        KPI 2 : Santé mentale par genre
        
        Args:
            filters: Dictionnaire des filtres à appliquer
            
        Returns:
            DataFrame avec gender, total_students, pourcentages de chaque condition
        """
        query = f"""
            SELECT 
                gender,
                COUNT(*) as total_students,
                SUM(CASE WHEN depression = 'Yes' THEN 1 ELSE 0 END) as depression_count,
                SUM(CASE WHEN anxiety = 'Yes' THEN 1 ELSE 0 END) as anxiety_count,
                SUM(CASE WHEN panic_attack = 'Yes' THEN 1 ELSE 0 END) as panic_count,
                ROUND(SUM(CASE WHEN depression = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as depression_pct,
                ROUND(SUM(CASE WHEN anxiety = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as anxiety_pct,
                ROUND(SUM(CASE WHEN panic_attack = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as panic_pct
            FROM {self.table_name}
            WHERE gender IS NOT NULL AND gender != 'nan'
        """
        
        if filters:
            query += self._build_filter_clause(filters)
        
        query += " GROUP BY gender ORDER BY total_students DESC"
        
        try:
            result = self.conn.execute(query).fetchdf()
            return result
        except Exception as e:
            st.error(f"Erreur lors de l'exécution de la requête : {str(e)}")
            return pd.DataFrame()
    
    def get_performance_correlation(self, filters=None):
        """
        KPI 3 : Corrélation entre performance académique (CGPA) et santé mentale
        
        Args:
            filters: Dictionnaire des filtres à appliquer
            
        Returns:
            DataFrame avec cgpa, depression, anxiety, panic_attack, gender, age
        """
        query = f"""
            SELECT 
                cgpa,
                depression,
                anxiety,
                panic_attack,
                treatment,
                gender,
                age,
                year
            FROM {self.table_name}
            WHERE cgpa IS NOT NULL
        """
        
        if filters:
            query += self._build_filter_clause(filters)
        
        query += " ORDER BY cgpa DESC"
        
        try:
            result = self.conn.execute(query).fetchdf()
            return result
        except Exception as e:
            st.error(f"Erreur lors de l'exécution de la requête : {str(e)}")
            return pd.DataFrame()
    
    def get_cgpa_by_mental_health(self, filters=None):
        """
        KPI 3 (complément) : CGPA moyen selon l'état de santé mentale
        
        Args:
            filters: Dictionnaire des filtres à appliquer
            
        Returns:
            DataFrame avec condition, avg_cgpa, student_count
        """
        query = f"""
            SELECT 
                'Depression' as condition,
                depression as status,
                AVG(cgpa) as avg_cgpa,
                COUNT(*) as student_count
            FROM {self.table_name}
            WHERE cgpa IS NOT NULL AND depression IS NOT NULL
        """
        
        if filters:
            query += self._build_filter_clause(filters)
        
        query += """
            GROUP BY depression
            
            UNION ALL
            
            SELECT 
                'Anxiety' as condition,
                anxiety as status,
                AVG(cgpa) as avg_cgpa,
                COUNT(*) as student_count
            FROM {self.table_name}
            WHERE cgpa IS NOT NULL AND anxiety IS NOT NULL
        """
        
        if filters:
            query += self._build_filter_clause(filters)
        
        query += """
            GROUP BY anxiety
            
            UNION ALL
            
            SELECT 
                'Panic Attack' as condition,
                panic_attack as status,
                AVG(cgpa) as avg_cgpa,
                COUNT(*) as student_count
            FROM {self.table_name}
            WHERE cgpa IS NOT NULL AND panic_attack IS NOT NULL
        """
        
        if filters:
            query += self._build_filter_clause(filters)
        
        query += " GROUP BY panic_attack"
        
        try:
            result = self.conn.execute(query).fetchdf()
            return result
        except Exception as e:
            st.error(f"Erreur lors de l'exécution de la requête : {str(e)}")
            return pd.DataFrame()
    
    def get_risk_factors_distribution(self, filters=None):
        """
        KPI 4 : Distribution des facteurs de risque
        
        Args:
            filters: Dictionnaire des filtres à appliquer
            
        Returns:
            DataFrame avec category, status, count, percentage
        """
        # Première requête pour obtenir le total
        total_query = f"""
            SELECT COUNT(*) as total
            FROM {self.table_name}
            WHERE 1=1
        """
        
        if filters:
            total_query += self._build_filter_clause(filters)
        
        try:
            total_result = self.conn.execute(total_query).fetchdf()
            total_students = total_result['total'].iloc[0] if not total_result.empty else 1
        except:
            total_students = 1
        
        # Requête principale pour les facteurs de risque
        query = f"""
            SELECT 
                'Depression' as category,
                depression as status,
                COUNT(*) as count,
                ROUND(COUNT(*) * 100.0 / {total_students}, 2) as percentage
            FROM {self.table_name}
            WHERE depression IS NOT NULL
        """
        
        if filters:
            query += self._build_filter_clause(filters)
        
        query += f"""
            GROUP BY depression
            
            UNION ALL
            
            SELECT 
                'Anxiety' as category,
                anxiety as status,
                COUNT(*) as count,
                ROUND(COUNT(*) * 100.0 / {total_students}, 2) as percentage
            FROM {self.table_name}
            WHERE anxiety IS NOT NULL
        """
        
        if filters:
            query += self._build_filter_clause(filters)
        
        query += f"""
            GROUP BY anxiety
            
            UNION ALL
            
            SELECT 
                'Panic Attack' as category,
                panic_attack as status,
                COUNT(*) as count,
                ROUND(COUNT(*) * 100.0 / {total_students}, 2) as percentage
            FROM {self.table_name}
            WHERE panic_attack IS NOT NULL
        """
        
        if filters:
            query += self._build_filter_clause(filters)
        
        query += " GROUP BY panic_attack ORDER BY category, status"
        
        try:
            result = self.conn.execute(query).fetchdf()
            return result
        except Exception as e:
            st.error(f"Erreur lors de l'exécution de la requête : {str(e)}")
            return pd.DataFrame()
    
    def get_treatment_analysis(self, filters=None):
        """
        KPI 4 (complément) : Analyse du traitement
        
        Args:
            filters: Dictionnaire des filtres à appliquer
            
        Returns:
            DataFrame avec treatment status et conditions
        """
        query = f"""
            SELECT 
                treatment,
                COUNT(*) as total_students,
                SUM(CASE WHEN depression = 'Yes' THEN 1 ELSE 0 END) as with_depression,
                SUM(CASE WHEN anxiety = 'Yes' THEN 1 ELSE 0 END) as with_anxiety,
                SUM(CASE WHEN panic_attack = 'Yes' THEN 1 ELSE 0 END) as with_panic,
                ROUND(AVG(cgpa), 2) as avg_cgpa
            FROM {self.table_name}
            WHERE treatment IS NOT NULL
        """
        
        if filters:
            query += self._build_filter_clause(filters)
        
        query += " GROUP BY treatment"
        
        try:
            result = self.conn.execute(query).fetchdf()
            return result
        except Exception as e:
            st.error(f"Erreur lors de l'exécution de la requête : {str(e)}")
            return pd.DataFrame()
    
    def _build_filter_clause(self, filters):
        """
        Construit la clause WHERE à partir des filtres
        
        Args:
            filters: Dictionnaire contenant les filtres
                - gender: liste des genres
                - age_range: tuple (min_age, max_age)
                - year: liste des années d'études
                
        Returns:
            String: Clause WHERE SQL
        """
        conditions = []
        
        # Filtre par genre
        if filters.get('gender') and filters['gender']:
            genders_str = "', '".join(filters['gender'])
            conditions.append(f"gender IN ('{genders_str}')")
        
        # Filtre par âge
        if filters.get('age_range'):
            min_age, max_age = filters['age_range']
            conditions.append(f"age BETWEEN {min_age} AND {max_age}")
        
        # Filtre par année d'études
        if filters.get('year') and filters['year']:
            year_str = "', '".join(filters['year'])
            conditions.append(f"year IN ('{year_str}')")
        
        # Construire la clause WHERE
        if conditions:
            return " AND " + " AND ".join(conditions)
        return ""
    
    def get_available_genders(self):
        """Récupère la liste unique des genres"""
        query = f"""
            SELECT DISTINCT gender
            FROM {self.table_name}
            WHERE gender IS NOT NULL AND gender != 'nan'
            ORDER BY gender
        """
        
        try:
            result = self.conn.execute(query).fetchdf()
            return result['gender'].tolist() if not result.empty else []
        except:
            return []
    
    def get_available_years(self):
        """Récupère la liste unique des années d'études"""
        query = f"""
            SELECT DISTINCT year
            FROM {self.table_name}
            WHERE year IS NOT NULL AND year != 'nan'
            ORDER BY year
        """
        
        try:
            result = self.conn.execute(query).fetchdf()
            return result['year'].tolist() if not result.empty else []
        except:
            return []
    
    def get_available_courses(self):
        """Récupère la liste unique des cours/filières"""
        query = f"""
            SELECT DISTINCT course
            FROM {self.table_name}
            WHERE course IS NOT NULL AND course != 'nan'
            ORDER BY course
        """
        
        try:
            result = self.conn.execute(query).fetchdf()
            return result['course'].tolist() if not result.empty else []
        except:
            return []
    
    def get_age_range(self):
        """Récupère la plage d'âge disponible"""
        query = f"""
            SELECT 
                MIN(age) as min_age,
                MAX(age) as max_age
            FROM {self.table_name}
            WHERE age IS NOT NULL
        """
        
        try:
            result = self.conn.execute(query).fetchdf()
            return result if not result.empty else None
        except:
            return None
    
    def get_cgpa_range(self):
        """Récupère la plage de CGPA disponible"""
        query = f"""
            SELECT 
                MIN(cgpa) as min_cgpa,
                MAX(cgpa) as max_cgpa,
                AVG(cgpa) as avg_cgpa
            FROM {self.table_name}
            WHERE cgpa IS NOT NULL
        """
        
        try:
            result = self.conn.execute(query).fetchdf()
            return result if not result.empty else None
        except:
            return None
    
    def get_table_info(self):
        """Récupère des informations sur la table"""
        try:
            query = f"SELECT COUNT(*) as total FROM {self.table_name}"
            result = self.conn.execute(query).fetchdf()
            return result['total'].iloc[0] if not result.empty else 0
        except:
            return 0
    
    def get_table_stats(self):
        """Récupère des statistiques globales sur la table"""
        query = f"""
            SELECT 
                COUNT(*) as total_students,
                COUNT(DISTINCT gender) as nb_genders,
                COUNT(DISTINCT year) as nb_years,
                COUNT(DISTINCT course) as nb_courses,
                MIN(age) as min_age,
                MAX(age) as max_age,
                ROUND(AVG(cgpa), 2) as avg_cgpa
            FROM {self.table_name}
        """
        
        try:
            result = self.conn.execute(query).fetchdf()
            return result if not result.empty else None
        except:
            return None
    
    def get_column_names(self):
        """Récupère les noms de colonnes de la table"""
        try:
            query = f"SELECT * FROM {self.table_name} LIMIT 0"
            result = self.conn.execute(query).fetchdf()
            return result.columns.tolist()
        except:
            return []
    
    def close(self):
        """Ferme la connexion à la base de données"""
        self.conn.close()