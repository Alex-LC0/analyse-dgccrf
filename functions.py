"""Outils de contrôle qualité et d'analyse des sanctions de la DGCCRF.

Ce module regroupe des fonctions utilitaires pour contrôler la qualité de
trois jeux de données (les sanctions prononcées par la DGCCRF, les
établissements identifiés par leur SIRET et la nomenclature NAF) et pour
produire des statistiques descriptives sur les amendes et sur la
couverture des secteurs d'activité.

Fonctions
---------
Contrôle de la qualité des données :
    data_clean_dgccrf(df)
        Rapport de qualité sur les sanctions de la DGCCRF (taille,
        doublons, valeurs manquantes, types de ``Siret`` et ``Amende``,
        amendes hors normes, modalités de ``Raison amende``).
    data_clean_siret(df)
        Rapport de qualité sur les établissements (taille, doublons,
        valeurs manquantes, types de ``siret`` et ``code_naf``, SIRET
        mal renseignés).
    data_clean_naf(df)
        Rapport de qualité sur la nomenclature NAF (taille, doublons,
        valeurs manquantes, type de ``Code``).

Statistiques descriptives :
    descriptive_analyse(df)
        Effectif, moyenne, médiane, écart type, extrema et montant total
        des amendes, ainsi qu'un indicateur de couverture des secteurs
        d'activité par rapport à la nomenclature ``naf_division``.

Colonnes attendues
------------------
Selon les fonctions, les DataFrames doivent contenir tout ou partie des
colonnes suivantes :

- Sanctions de la DGCCRF :

  - ``Siret`` : numéro SIRET de l'entreprise sanctionnée ;
  - ``Amende`` : montant de l'amende ;
  - ``Raison amende`` : motif de la sanction ;
  - ``Division`` : division (secteur d'activité) de l'entreprise ;

- Établissements :

  - ``siret`` : numéro SIRET de l'établissement (14 chiffres) ;
  - ``code_naf`` : code NAF de l'établissement ;

- Nomenclature NAF :

  - ``Code`` : code NAF ;
  - ``Libellé`` : libellé de la division (colonne de ``naf_division``).

Dépendances
-----------
- ``pandas`` (importé sous l'alias ``pd``) ;
- ``matplotlib.pyplot`` (importé sous l'alias ``plt``) et ``seaborn``
  (importé sous l'alias ``sns``) : importés par le module mais
  inutilisés par les fonctions actuelles.

Notes
-----
- Les fonctions de rapport renvoient des dictionnaires dont les clés sont
  des libellés en français destinés à la lecture ; elles ne modifient
  jamais le DataFrame fourni.
- ``descriptive_analyse`` utilise la variable globale ``naf_division``,
  un DataFrame de la nomenclature NAF non passé en paramètre : il doit
  être défini dans l'espace de noms avant l'appel.
- Le module requiert Python 3.12 ou supérieur, en raison des guillemets
  doubles imbriqués dans la f-string de ``descriptive_analyse``.
- Les colonnes ``siret``, ``Siret``, ``code_naf`` et ``Code`` doivent
  être lues comme du texte (par exemple avec ``dtype=str`` à la lecture
  du fichier) pour conserver les zéros initiaux.

Examples
--------
>>> import pandas as pd
>>> df = pd.read_csv("sanctions_dgccrf.csv", dtype={"Siret": str})
>>> rapport = data_clean_dgccrf(df)
>>> stats = descriptive_analyse(df)
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def data_clean_dgccrf(df: pd.DataFrame) -> dict:
    """Génère un rapport de qualité sur le jeu de données des sanctions de la DGCCRF.

    La fonction calcule plusieurs indicateurs de qualité : taille du
    DataFrame, doublons, valeurs manquantes, types des colonnes ``Siret``
    et ``Amende``, nombre d'amendes jugées hors normes (supérieures ou
    égales à 3 000 000) et modalités distinctes des raisons de sanction.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame à analyser. Il doit contenir au minimum les colonnes
        suivantes :

        - ``Siret`` : numéro SIRET de l'entreprise sanctionnée ;
        - ``Amende`` : montant de l'amende ;
        - ``Raison amende`` : motif de la sanction.

    Returns
    -------
    dict
        Dictionnaire contenant les clés suivantes :

        - ``"Taille du dataframe"`` (int) : nombre total de lignes du
          DataFrame ;
        - ``"Nombre de doublons : "`` (numpy.int64) : nombre de lignes
          dupliquées ;
        - ``"Nombre de NaN : "`` (pd.Series) : nombre de valeurs
          manquantes pour chaque colonne ;
        - ``"Type de valeur de la colonne SIRET : "`` (numpy.dtype) : type
          de données de la colonne ``Siret`` (par exemple ``int64``) ;
        - ``"Type de valeur de la colonne Amende :"`` (numpy.dtype) : type
          de données de la colonne ``Amende`` (par exemple ``float64``) ;
        - ``"Nombre d'amendes hors normes :"`` (numpy.int64) : nombre
          d'amendes dont le montant est supérieur ou égal à 3 000 000 ;
        - ``"Type de sanction différentes : "`` (pandas.arrays.StringArray) :
          valeurs uniques de la colonne ``Raison amende``.

    Raises
    ------
    KeyError
        Si l'une des colonnes requises (``Siret``, ``Amende``,
        ``Raison amende``) est absente du DataFrame.
    TypeError
        Si la colonne ``Amende`` n'est pas de type numérique, la
        comparaison avec le seuil de 3 000 000 étant alors impossible.

    Notes
    -----
    - Le seuil de 3 000 000 pour les amendes « hors normes » est fixé
      arbitrairement dans le code (valeur jugée hors norme).
    - La colonne ``Amende`` est de type ``float64`` dès qu'elle contient
      des valeurs manquantes (``NaN``). Ces lignes ne sont pas comptées
      parmi les amendes hors normes.
    - Le type de l'objet renvoyé par ``unique()`` sur ``Raison amende``
      dépend de la version de pandas : ``StringArray`` pour une colonne
      de type chaîne de caractères pandas, ``numpy.ndarray`` pour une
      colonne de type ``object``. Les valeurs manquantes éventuelles y
      sont incluses.

    Examples
    --------
    >>> rapport = data_clean_dgccrf(df)
    >>> rapport["Taille du dataframe"]
    131
    """
    quality_report = {
        "Taille du dataframe": len(df),
        "Nombre de doublons : ": df.duplicated().sum(),
        "Nombre de NaN : ": df.isnull().sum(),
        "Type de valeur de la colonne SIRET : ": df["Siret"].dtype,
        "Type de valeur de la colonne Amende :": df["Amende"].dtype,
        "Nombre d'amendes hors normes :": df.loc[
            df["Amende"] >= 3000000, "Amende"
        ].count(),  #  Valeur jugée hors norme
        "Type de sanction différentes : ": df["Raison amende"].unique(),
    }
    return quality_report


def data_clean_siret(df: pd.DataFrame) -> dict:
    """Génère un rapport de qualité sur un jeu de données d'établissements identifiés par leur SIRET.

    La fonction calcule plusieurs indicateurs de qualité : taille du
    DataFrame, doublons, valeurs manquantes, types des colonnes ``siret``
    et ``code_naf`` et nombre de SIRET mal renseignés, c'est-à-dire
    comportant moins de 14 caractères.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame à analyser. Il doit contenir au minimum les colonnes
        suivantes :

        - ``siret`` : numéro SIRET de l'établissement (14 chiffres). La
          colonne doit être de type texte et ne contenir aucune valeur
          manquante (voir Notes) ;
        - ``code_naf`` : code NAF (activité principale) de l'établissement.

    Returns
    -------
    dict
        Dictionnaire contenant les clés suivantes :

        - ``"Taille du dataframe"`` (int) : nombre total de lignes du
          DataFrame ;
        - ``"Nombre de doublons : "`` (numpy.int64) : nombre de lignes
          dupliquées ;
        - ``"Nombre de NaN : "`` (pd.Series) : nombre de valeurs
          manquantes pour chaque colonne ;
        - ``"Type de valeur de la colonne SIRET : "`` (numpy.dtype) : type
          de données de la colonne ``siret`` ;
        - ``"Type de valeur de la colonne code_naf :"`` (numpy.dtype) : type
          de données de la colonne ``code_naf`` ;
        - ``"Nombre de siret mal renseignés"`` (int) : nombre de SIRET
          dont la longueur est strictement inférieure à 14 caractères.

    Raises
    ------
    KeyError
        Si l'une des colonnes requises (``siret``, ``code_naf``) est
        absente du DataFrame.
    TypeError
        Si la colonne ``siret`` est de type numérique ou contient des
        valeurs manquantes, car la fonction ``len`` ne s'applique ni à un
        entier ni à un ``NaN`` (voir Notes).

    Notes
    -----
    - La longueur est mesurée directement sur les valeurs de la colonne,
      sans conversion en chaîne de caractères. La colonne ``siret`` doit
      donc être lue comme du texte (par exemple avec
      ``dtype={"siret": str}`` à la lecture du fichier), ce qui préserve
      également les zéros initiaux.
    - Une valeur manquante dans ``siret`` (``NaN`` ou ``pd.NA``) provoque
      une ``TypeError`` : les valeurs manquantes doivent être traitées au
      préalable. Le nombre de valeurs manquantes par colonne est
      disponible dans la clé ``"Nombre de NaN : "``, mais seulement si
      la fonction aboutit.
    - Pour une colonne de type texte, le type renvoyé pour ``siret`` est
      ``object`` ou ``str`` selon la version de pandas.
    - Seuls les SIRET trop courts sont comptés : un SIRET de plus de 14
      caractères n'est pas considéré comme mal renseigné.

    Examples
    --------
    >>> rapport = data_clean_siret(df)
    >>> rapport["Nombre de siret mal renseignés"]
    12
    """
    count_siret = 0
    for vl in df["siret"]:
        if len(vl) < 14:
            count_siret += 1

    quality_report = {
        "Taille du dataframe": len(df),
        "Nombre de doublons : ": df.duplicated().sum(),
        "Nombre de NaN : ": df.isnull().sum(),
        "Type de valeur de la colonne SIRET : ": df["siret"].dtype,
        "Type de valeur de la colonne code_naf :": df["code_naf"].dtype,
        "Nombre de siret mal renseignés": count_siret,
    }
    return quality_report


def data_clean_naf(df: pd.DataFrame) -> dict:
    """Génère un rapport de qualité sur un jeu de données de la nomenclature NAF.

    La fonction calcule plusieurs indicateurs de qualité : taille du
    DataFrame, doublons, valeurs manquantes et type de données de la
    colonne ``Code``.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame à analyser. Il doit contenir au minimum la colonne
        suivante :

        - ``Code`` : code NAF (activité principale).

    Returns
    -------
    dict
        Dictionnaire contenant les clés suivantes :

        - ``"Taille du dataframe"`` (int) : nombre total de lignes du
          DataFrame ;
        - ``"Nombre de doublons : "`` (numpy.int64) : nombre de lignes
          dupliquées ;
        - ``"Nombre de NaN : "`` (pd.Series) : nombre de valeurs
          manquantes pour chaque colonne ;
        - ``"Type de valeur de la colonne Code : "`` (numpy.dtype) : type
          de données de la colonne ``Code``.

    Raises
    ------
    KeyError
        Si la colonne ``Code`` est absente du DataFrame.

    Notes
    -----
    - La colonne ``Code`` est indiquée avec une majuscule : le nom des
      colonnes est sensible à la casse, contrairement aux colonnes
      ``siret`` et ``code_naf`` de ``data_clean_siret``.
    - Les codes NAF pouvant commencer par un zéro (par exemple
      ``"0111Z"``), la colonne doit être lue comme du texte pour
      conserver ces zéros initiaux (par exemple avec
      ``dtype={"Code": str}`` à la lecture du fichier).

    Examples
    --------
    >>> rapport = data_clean_naf(df)
    >>> rapport["Taille du dataframe"]
    732
    """
    quality_report = {
        "Taille du dataframe": len(df),
        "Nombre de doublons : ": df.duplicated().sum(),
        "Nombre de NaN : ": df.isnull().sum(),
        "Type de valeur de la colonne Code : ": df["Code"].dtype,
    }
    return quality_report


def descriptive_analyse(df: pd.DataFrame) -> dict:
    """Calcule des statistiques descriptives sur les amendes et la couverture des secteurs d'activité.

    La fonction calcule, pour la colonne ``Amende``, l'effectif, la
    moyenne, la médiane, l'écart type, le minimum, le maximum et le
    montant total. Elle produit aussi un indicateur de comparaison entre
    le nombre de divisions présentes dans le jeu de données et le nombre
    total de divisions de la nomenclature ``naf_division``.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame des sanctions à analyser. Il doit contenir au minimum
        les colonnes suivantes :

        - ``Amende`` : montant de l'amende (numérique) ;
        - ``Division`` : division (secteur d'activité) de l'entreprise
          sanctionnée.

    Returns
    -------
    dict
        Dictionnaire contenant les clés suivantes :

        - ``"Taille du jeu de donnée : "`` (int) : nombre total de lignes
          du DataFrame ;
        - ``"Nombre total d'amendes sur la période"`` (numpy.int64) :
          nombre d'amendes renseignées (valeurs non manquantes de
          ``Amende``) ;
        - ``"Tarif moyen d'une amende : "`` (numpy.float64) : moyenne des
          amendes, arrondie à 2 décimales ;
        - ``"Tarif médian d'une amende"`` (numpy.float64) : médiane des
          amendes, arrondie à 2 décimales ;
        - ``"Ecart type entre les amendes"`` (numpy.float64) : écart type
          de l'échantillon (``ddof=1``), arrondi à 2 décimales ;
        - ``"Tarif minimal d'une amende : "`` (numpy.float64) : plus petite
          amende, arrondie à 2 décimales ;
        - ``"Tarif maximal d'une amende : "`` (numpy.float64) : plus grande
          amende, arrondie à 2 décimales ;
        - ``"Montant total généré par les amendes :"`` (numpy.float64) :
          somme des amendes, calculée avec la fonction ``sum`` native de
          Python ;
        - ``"Nombre de secteur sanctionnés vs. total secteur :"`` (str) :
          chaîne au format ``"X / Y"``, où ``Y`` est le nombre de
          libellés distincts de ``naf_division`` et ``X`` la valeur
          absolue de la différence entre ``Y`` et le nombre de divisions
          distinctes de ``df``.

    Raises
    ------
    KeyError
        Si la colonne ``Amende`` ou ``Division`` est absente de ``df``, ou
        si la colonne ``Libellé`` est absente de ``naf_division``.
    NameError
        Si la variable globale ``naf_division`` n'est pas définie.
    TypeError
        Si la colonne ``Amende`` n'est pas de type numérique.
    AttributeError
        Si ``unique()`` renvoie un ``numpy.ndarray`` (colonne de type
        ``object``), car ce type ne possède pas de méthode
        ``value_counts`` (voir Notes).

    Notes
    -----
     - **Dépendance globale** : la fonction utilise ``naf_division``, un
      DataFrame défini hors de la fonction et non passé en paramètre. Il
      doit exister dans l'espace de noms au moment de l'appel et contenir
      une colonne ``Libellé``.
    - **Valeurs manquantes** : ``count``, ``mean``, ``median``, ``std``,
      ``min`` et ``max`` ignorent les ``NaN``. En revanche, la fonction
      ``sum`` native de Python ne les ignore pas : si ``Amende`` contient
      au moins un ``NaN``, le montant total renvoyé est ``nan``.
      ``df["Amende"].sum()`` ignorerait les ``NaN``.
    - ``unique().value_counts()`` ne fonctionne que si ``unique()`` renvoie
      un tableau pandas (par exemple ``StringArray`` avec le type chaîne
      de pandas). Les valeurs manquantes sont alors exclues du décompte.
    - Les guillemets doubles imbriqués dans la f-string de la dernière
      clé (``f"{... df["Division"] ...}"``) ne sont acceptés qu'à partir
      de Python 3.12. Avant, le module lève une ``SyntaxError``.
    - Si la colonne ``Amende`` ne contient que des valeurs manquantes, les
      statistiques renvoient ``nan``.

    Examples
    --------
    >>> stats = descriptive_analyse(df)
    >>> stats["Taille du jeu de donnée : "]
    131
    """
    descriptive_stats = {
        "Taille du jeu de donnée : ": len(df),
        "Nombre total d'amendes sur la période": df["Amende"].count(),
        "Tarif moyen d'une amende : ": df["Amende"].mean().round(2),
        "Tarif médian d'une amende": df["Amende"].median().round(2),
        "Ecart type entre les amendes": df["Amende"].std().round(2),
        "Tarif minimal d'une amende : ": df["Amende"].min().round(2),
        "Tarif maximal d'une amende : ": df["Amende"].max().round(2),
        "Montant total généré par les amendes :": sum(df["Amende"]),
        "Nombre de secteur sanctionnés vs. total secteur :": f"{abs(df["Division"].unique().value_counts().sum() - naf_division["Libellé"].unique().value_counts().sum())} / {naf_division["Libellé"].unique().value_counts().sum()}",
    }
    return descriptive_stats
