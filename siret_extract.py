import pandas as pd
import duckdb

duckdb.sql("""
COPY(    
    SELECT
        siret,
        activitePrincipaleEtablissement AS code_naf
    FROM 'table_siret/siret_fr.csv') TO 'table_siret/siret_base.csv' (HEADER, DELIMITER ',')
""")  #  Connexion à la table via Duck DB et extraction des siret et code NAF
