import duckdb
import pandas as pd
import streamlit as st
from pathlib import Path

class AmazonPrimeDB:
    """Gestionnaire de base de données pour Amazon Prime"""
    
    def __init__(self):
        """Initialise la connexion à la base de données"""
        # Créer le dossier data s'il n'existe pas
        Path("data").mkdir(exist_ok=True)
        
        # Connexion à DuckDB
        self.conn = duckdb.connect('data/amazon_prime.db')
        self.table_name = 'prime_content'
    
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
            
            st.success(f"{len(df)} lignes chargées avec succès dans la base de données!")
            
            # Afficher un aperçu des données
            with st.expander("Aperçu des données chargées"):
                st.dataframe(df.head(10), use_container_width=True)
                st.write(f"**Nombre total de lignes :** {len(df)}")
                st.write(f"**Nombre de colonnes :** {len(df.columns)}")
                st.write(f"**Colonnes disponibles :** {', '.join(df.columns)}")
            
            return df
            
        except Exception as e:
            st.error(f" Erreur lors du chargement du fichier : {str(e)}")
            return None
    
    def _clean_data(self, df):
        """Nettoie et prépare les données"""
        # Normaliser les noms de colonnes
        df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
        
        # Convertir date_added en format date
        if 'date_added' in df.columns:
            df['date_added'] = pd.to_datetime(df['date_added'], errors='coerce')
        
        # Convertir release_year en entier
        if 'release_year' in df.columns:
            df['release_year'] = pd.to_numeric(df['release_year'], errors='coerce')
        
        # Nettoyer les colonnes textuelles
        text_columns = ['type', 'title', 'director', 'cast', 'country', 'rating', 'listed_in', 'description']
        for col in text_columns:
            if col in df.columns:
                df[col] = df[col].astype(str).str.strip()
        
        return df
    
    def get_content_by_decade(self, filters=None):
        """
        KPI 1 : Distribution du contenu par décennie de production
        
        Args:
            filters: Dictionnaire des filtres à appliquer
            
        Returns:
            DataFrame avec decade, decade_label, total_content, nb_movies, nb_shows
        """
        query = f"""
            SELECT 
                (release_year / 10) * 10 as decade,
                COUNT(*) as total_content,
                SUM(CASE WHEN type = 'Movie' THEN 1 ELSE 0 END) as nb_movies,
                SUM(CASE WHEN type = 'TV Show' THEN 1 ELSE 0 END) as nb_shows
            FROM {self.table_name}
            WHERE release_year IS NOT NULL
        """
        
        # Ajouter les filtres si nécessaire
        if filters:
            query += self._build_filter_clause(filters)
        
        query += " GROUP BY decade ORDER BY decade"
        
        try:
            result = self.conn.execute(query).fetchdf()
            # Formater les décennies (1990 → "1990s")
            if not result.empty:
                result['decade'] = result['decade'].astype(int)
                result['decade_label'] = result['decade'].astype(str) + 's'
            return result
        except Exception as e:
            st.error(f"Erreur lors de l'exécution de la requête : {str(e)}")
            return pd.DataFrame()
    
    def get_content_evolution(self, filters=None):
        """
        ANCIENNE VERSION - Évolution du nombre de contenus ajoutés par année
        Conservée pour compatibilité mais get_content_by_decade est recommandée
        
        Args:
            filters: Dictionnaire des filtres à appliquer
            
        Returns:
            DataFrame avec year, total_content, nb_movies, nb_shows
        """
        query = f"""
            SELECT 
                EXTRACT(YEAR FROM date_added) as year,
                COUNT(*) as total_content,
                SUM(CASE WHEN type = 'Movie' THEN 1 ELSE 0 END) as nb_movies,
                SUM(CASE WHEN type = 'TV Show' THEN 1 ELSE 0 END) as nb_shows
            FROM {self.table_name}
            WHERE date_added IS NOT NULL
        """
        
        # Ajouter les filtres si nécessaire
        if filters:
            query += self._build_filter_clause(filters)
        
        query += " GROUP BY year ORDER BY year"
        
        try:
            result = self.conn.execute(query).fetchdf()
            return result
        except Exception as e:
            st.error(f"Erreur lors de l'exécution de la requête : {str(e)}")
            return pd.DataFrame()
    
    def get_top_genres(self, limit=15, filters=None):
        """
        KPI 2 : Top genres les plus représentés
        
        Args:
            limit: Nombre de genres à retourner
            filters: Dictionnaire des filtres à appliquer
            
        Returns:
            DataFrame avec genre, nb_content OU Liste des noms de genres
        """
        # Construction de la requête avec CTE pour éviter l'erreur UNNEST
        if filters:
            # Version avec filtres
            filter_clause = self._build_filter_clause(filters)
            query = f"""
                WITH filtered_content AS (
                    SELECT show_id, listed_in
                    FROM {self.table_name}
                    WHERE listed_in IS NOT NULL AND listed_in != 'nan'
                    {filter_clause}
                ),
                genre_split AS (
                    SELECT 
                        show_id,
                        UNNEST(STRING_SPLIT(listed_in, ',')) as genre_raw
                    FROM filtered_content
                )
                SELECT 
                    TRIM(genre_raw) as genre,
                    COUNT(DISTINCT show_id) as nb_content
                FROM genre_split
                GROUP BY genre 
                ORDER BY nb_content DESC 
                LIMIT {limit}
            """
        else:
            # Version sans filtres
            query = f"""
                WITH genre_split AS (
                    SELECT 
                        show_id,
                        UNNEST(STRING_SPLIT(listed_in, ',')) as genre_raw
                    FROM {self.table_name}
                    WHERE listed_in IS NOT NULL AND listed_in != 'nan'
                )
                SELECT 
                    TRIM(genre_raw) as genre,
                    COUNT(DISTINCT show_id) as nb_content
                FROM genre_split
                GROUP BY genre 
                ORDER BY nb_content DESC 
                LIMIT {limit}
            """
        
        try:
            result = self.conn.execute(query).fetchdf()
            # Si appelé depuis filters.py (sans filtres), retourne juste la liste
            if filters is None:
                return result['genre'].tolist() if not result.empty else []
            # Sinon retourne le DataFrame complet pour les visualisations
            return result
        except Exception as e:
            st.error(f"Erreur get_top_genres : {str(e)}")
            return [] if filters is None else pd.DataFrame()
    
    def get_countries_distribution(self, limit=15, filters=None):
        """
        KPI 3 : Répartition géographique de la production
        
        Args:
            limit: Nombre de pays à retourner
            filters: Dictionnaire des filtres à appliquer
            
        Returns:
            DataFrame avec country, nb_content, percentage
        """
        if filters:
            # Version avec filtres
            filter_clause = self._build_filter_clause(filters)
            query = f"""
                WITH filtered_content AS (
                    SELECT show_id, country
                    FROM {self.table_name}
                    WHERE country IS NOT NULL AND country != 'nan'
                    {filter_clause}
                ),
                country_split AS (
                    SELECT 
                        show_id,
                        UNNEST(STRING_SPLIT(country, ',')) as country_raw
                    FROM filtered_content
                ),
                country_counts AS (
                    SELECT 
                        TRIM(country_raw) as country,
                        COUNT(DISTINCT show_id) as nb_content
                    FROM country_split
                    GROUP BY country
                )
                SELECT 
                    country,
                    nb_content,
                    ROUND(nb_content * 100.0 / SUM(nb_content) OVER (), 2) as percentage
                FROM country_counts
                ORDER BY nb_content DESC
                LIMIT {limit}
            """
        else:
            # Version sans filtres
            query = f"""
                WITH country_split AS (
                    SELECT 
                        show_id,
                        UNNEST(STRING_SPLIT(country, ',')) as country_raw
                    FROM {self.table_name}
                    WHERE country IS NOT NULL AND country != 'nan'
                ),
                country_counts AS (
                    SELECT 
                        TRIM(country_raw) as country,
                        COUNT(DISTINCT show_id) as nb_content
                    FROM country_split
                    GROUP BY country
                )
                SELECT 
                    country,
                    nb_content,
                    ROUND(nb_content * 100.0 / SUM(nb_content) OVER (), 2) as percentage
                FROM country_counts
                ORDER BY nb_content DESC
                LIMIT {limit}
            """
        
        try:
            result = self.conn.execute(query).fetchdf()
            return result
        except Exception as e:
            st.error(f"Erreur get_countries_distribution : {str(e)}")
            return pd.DataFrame()
    
    def get_movies_vs_shows(self, filters=None):
        """
        KPI 4 : Comparaison entre Films et Séries
        
        Args:
            filters: Dictionnaire des filtres à appliquer
            
        Returns:
            DataFrame avec type, total, year_range, oldest_year, newest_year
        """
        query = f"""
            SELECT 
                type,
                COUNT(*) as total,
                COUNT(DISTINCT release_year) as year_range,
                MIN(release_year) as oldest_year,
                MAX(release_year) as newest_year
            FROM {self.table_name}
            WHERE type IS NOT NULL
        """
        
        if filters:
            query += self._build_filter_clause(filters)
        
        query += " GROUP BY type ORDER BY total DESC"
        
        try:
            result = self.conn.execute(query).fetchdf()
            return result
        except Exception as e:
            st.error(f"Erreur lors de l'exécution de la requête : {str(e)}")
            return pd.DataFrame()
    
    def get_content_by_year(self, filters=None):
        """
        Bonus : Distribution du contenu par année de sortie
        
        Returns:
            DataFrame avec release_year, count
        """
        query = f"""
            SELECT 
                release_year,
                COUNT(*) as count
            FROM {self.table_name}
            WHERE release_year IS NOT NULL
        """
        
        if filters:
            query += self._build_filter_clause(filters)
        
        query += " GROUP BY release_year ORDER BY release_year DESC"
        
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
                - content_type: liste des types (Movie, TV Show)
                - year_range: tuple (min_year, max_year)
                - genre: liste des genres
                - country: liste des pays
                - rating: liste des ratings
                
        Returns:
            String: Clause WHERE SQL
        """
        conditions = []
        
        # Filtre par type de contenu
        if filters.get('content_type') and 'Tous' not in filters['content_type']:
            types_str = "', '".join(filters['content_type'])
            conditions.append(f"type IN ('{types_str}')")
        
        # Filtre par année de sortie (release_year)
        if filters.get('year_range'):
            min_year, max_year = filters['year_range']
            conditions.append(f"release_year BETWEEN {min_year} AND {max_year}")
        
        # Filtre par rating
        if filters.get('rating') and 'Tous' not in filters['rating']:
            ratings_str = "', '".join(filters['rating'])
            conditions.append(f"rating IN ('{ratings_str}')")
        
        # Filtre par genres
        if filters.get('genre') and 'Tous' not in filters['genre']:
            genres_conditions = []
            for genre in filters['genre']:
                safe_genre = genre.replace("'", "''")
                genres_conditions.append(f"listed_in LIKE '%{safe_genre}%'")
            conditions.append(f"({' OR '.join(genres_conditions)})")
        
        # Filtre par pays
        if filters.get('country') and 'Tous' not in filters['country']:
            countries_conditions = []
            for country in filters['country']:
                safe_country = country.replace("'", "''")
                countries_conditions.append(f"country LIKE '%{safe_country}%'")
            conditions.append(f"({' OR '.join(countries_conditions)})")
        
        # Construire la clause WHERE
        if conditions:
            return " AND " + " AND ".join(conditions)
        return ""
    
    def get_available_genres(self):
        """Récupère la liste unique des genres"""
        query = f"""
            WITH genre_split AS (
                SELECT UNNEST(STRING_SPLIT(listed_in, ',')) as genre_raw
                FROM {self.table_name}
                WHERE listed_in IS NOT NULL AND listed_in != 'nan'
            )
            SELECT DISTINCT TRIM(genre_raw) as genre
            FROM genre_split
            ORDER BY genre
        """
        
        try:
            result = self.conn.execute(query).fetchdf()
            return result['genre'].tolist() if not result.empty else []
        except:
            return []
    
    def get_available_countries(self):
        """Récupère la liste unique des pays"""
        query = f"""
            WITH country_split AS (
                SELECT UNNEST(STRING_SPLIT(country, ',')) as country_raw
                FROM {self.table_name}
                WHERE country IS NOT NULL AND country != 'nan'
            )
            SELECT DISTINCT TRIM(country_raw) as country
            FROM country_split
            ORDER BY country
        """
        
        try:
            result = self.conn.execute(query).fetchdf()
            return result['country'].tolist() if not result.empty else []
        except:
            return []
    
    def get_date_range(self):
        """Récupère la plage de dates disponible"""
        query = f"""
            SELECT 
                MIN(EXTRACT(YEAR FROM date_added)) as min_year,
                MAX(EXTRACT(YEAR FROM date_added)) as max_year
            FROM {self.table_name}
            WHERE date_added IS NOT NULL
        """
        
        try:
            result = self.conn.execute(query).fetchdf()
            return result if not result.empty else None
        except:
            return None
    
    def get_release_year_range(self):
        """Récupère la plage d'années de sortie"""
        query = f"""
            SELECT 
                MIN(release_year) as min_year,
                MAX(release_year) as max_year
            FROM {self.table_name}
            WHERE release_year IS NOT NULL
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
            WITH genre_split AS (
                SELECT UNNEST(STRING_SPLIT(listed_in, ',')) as genre_raw
                FROM {self.table_name}
                WHERE listed_in IS NOT NULL
            ),
            country_split AS (
                SELECT UNNEST(STRING_SPLIT(country, ',')) as country_raw
                FROM {self.table_name}
                WHERE country IS NOT NULL
            )
            SELECT 
                (SELECT COUNT(*) FROM {self.table_name}) as total_content,
                (SELECT COUNT(DISTINCT type) FROM {self.table_name}) as nb_types,
                (SELECT COUNT(DISTINCT TRIM(country_raw)) FROM country_split) as nb_countries,
                (SELECT COUNT(DISTINCT TRIM(genre_raw)) FROM genre_split) as nb_genres,
                (SELECT MIN(release_year) FROM {self.table_name}) as oldest_content,
                (SELECT MAX(release_year) FROM {self.table_name}) as newest_content
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
    
    # ==================== MÉTHODES POUR FILTERS.PY ====================
    
    def get_unique_values(self, column: str):
        """
        Récupère les valeurs uniques d'une colonne
        
        Args:
            column: Nom de la colonne
            
        Returns:
            Liste des valeurs uniques
        """
        try:
            query = f"""
                SELECT DISTINCT {column}
                FROM {self.table_name}
                WHERE {column} IS NOT NULL AND {column} != 'nan'
                ORDER BY {column}
            """
            result = self.conn.execute(query).fetchdf()
            return result[column].tolist() if not result.empty else []
        except Exception as e:
            st.error(f"Erreur get_unique_values: {str(e)}")
            return []
    
    def get_year_range(self):
        """
        Récupère la plage d'années de release_year
        
        Returns:
            Tuple (min_year, max_year)
        """
        try:
            query = f"""
                SELECT 
                    MIN(release_year) as min_year,
                    MAX(release_year) as max_year
                FROM {self.table_name}
                WHERE release_year IS NOT NULL
            """
            result = self.conn.execute(query).fetchdf()
            if not result.empty:
                return (int(result['min_year'].iloc[0]), int(result['max_year'].iloc[0]))
            return (None, None)
        except:
            return (None, None)
    
    def get_top_countries(self, limit=20):
        """
        Récupère les top N pays
        
        Args:
            limit: Nombre de pays à retourner
            
        Returns:
            Liste des noms de pays
        """
        try:
            df = self.get_countries_distribution(limit=limit, filters=None)
            return df['country'].tolist() if not df.empty else []
        except:
            return []
    
    # ============================================================================
    
    def close(self):
        """Ferme la connexion à la base de données"""
        self.conn.close()