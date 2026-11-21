# analyse-dgccrf

Analyse des sanctions publiées par la Direction générale de la concurrence, de la consommation et de la répression des fraudes afin de répondre à la question : 

*Quels secteurs d’activité reçoivent le plus de sanctions publiés par la DGCCRF ?*

En se basant sur les données dont la publication était active le 14/11/2026

## Sommaire

- [Résultats clés](#résultats-clés)
- [Contexte](#contexte)
- [Méthodologie](#méthodologie)
- [Stack technique](#stack-technique)
- [Structure du repo](#structure-du-repo)
- [Lancer le projet](#lancer-le-projet)
- [Limites et pistes futures](#limites-et-pistes-futures)
- [Auteur](#auteur)

## Résultats clés

La **phase de nettoyage** a fait perdre : 

- 11.45% des données pour les sanctions de la DGCCRF
- 0.048% des données pour la base des SIRET
- 19.06% des données pour les codes NAF

La **phase d'analyse** nous a informé sur : 

- Certains secteurs semblent être plus affichés que d'autres par la DGCCRF
- Les délais de paiement entre entreprises est la cause la plus affichée sur la période collectée (88.3% des sanctions publiées)
- Le Commerce de gros, à l'exception des automobiles et des motocycles est le plus représenté en nombre d'amendes (16.52%) et en somme total des amendes (14.70%)

**Interpretation** des résultats : 

Mon analyse illustre une large représentation du secteur du commerce de gros dans les sanctions publiées sur le site de la DGCCRF. Sachant que 88.3% des sanctions concernent des délais de paiement, ce résultat s'explique par la logique d'information de ces sanctions. Ainsi, l'affichage de cette dernière informe les fournisseurs de l'entreprise sur ces pratiques, permettant de rétablir un équilibre dans l'information.

De ce fait, ce résultat démontre un autre rôle de la DGCCRF dans **l'information et la mise à disposition d'informations pouvant impacter les relations inter-entreprises**.

## Contexte

La DGCCRF est un organisme de l'État français ayant pour mission le contrôle du respect de la concurrence, de l'économie et des consommateurs. Ainsi, il peut sanctionner des organismes, des individus ou des entreprises si ces derniers ne respectent pas les lois en vigueur. (*Source : Site de la DGCCRF*)

Dans une logique de prévention des consommateurs et des acteurs économiques, la DGCCRF peut dans certains cas appliquer une sanction supplémentaire : **l'affichage public de l'entreprise et de la sanction qui lui est imposée**. Ces sanctions peuvent concerner : des pratiques commerciales déloyales, des défauts d’affichage des prix, la commercialisation de produits non conformes ou dangereux, des pratiques anticoncurrentielles locales ou restrictives de concurrence, le non-respect des délais de paiement interentreprises, etc. Dès lors, l'ensemble des acteurs économiques possèdent l'information sur cette entreprise/individu. (*Source : Site de la DGCCRF*)

Il est donc pertinent de s'intéresser à ces publications de sanctions, et les secteurs les plus à même de recevoir ce genre de sanctions, et c'est l'objectif de cette analyse. Cependant, je tiens à rappeler que cette dernière ne porte aucunement sur les secteurs les plus à risque de sanction, car l'échantillon des sanctions publié par la DGCCRF est largement plus faible que celles appliquées tout au long de l'année.

## Méthodologie

- Collecte des sanctions publiées par la DGCCRF, des SIRET (identifiant d'entreprise en France) et des codes NAF (Identifiant de l'activité principale de l'entreprise).
- Nettoyage des données collectées : Vérification de la taille des tables, suppression des valeurs nulles, suppression des doublons, enrichissement des données.
- Croisement des données de SIRET et de code NAF puis croisement avec les sanctions de la DGCCRF pour identifier le secteur des entreprises
- Analyse et réponse à la question
- Création d'un rapport Power BI

## Stack technique

- Python 3
- DuckDB
- pandas
- matplotlib
- seaborn
- re
- BeautifulSoup
- Power Query
- Power BI

## Structure du repo

```bash
analyse-dgccrf/
├── html_dgccrf/                 # Pages HTML enregristrée sur le site de la DGCCRF (Non inclues)
│   │   └── *.csv
├── table_dgccrf/                # Table .csv contenant les siret / amendes / cause des sanctions publiées crée à partir des HTML
│   │   └── *.csv
├── table_naf/                   # Tables .csv contenant les codes NAF et les divisions
│   │   └── *.csv
├── table_siret/                 # Table .csv contenant les numéros de SIRET et les code NAF identifant les entreprises
│   │   └── *.csv                   
├── analyse.ipynb                # Jupyter Notebook contenant l'ensemble du code d'analyse du projet
├── functions.py                 # Module de fonctions de analyse.ipynb
├── scrap.py                     # Script d'extraction des données des pages HTML
├── siret_extract.py             # Script d'extraction des données de la table SIRET
├── rapport-dgccrf.pbix          # Rapport Power BI du projet
├── requierment.txt
├── .gitignore   
└── README.md
```

## Lancer le projet

### Prérequis

- Python 3.14
- Jupyter Notebook (installé via `requirements.txt`)

### 1. Cloner le dépôt et installer les dépendances

```bash
git clone https://github.com/Alex-LC0/analyse-dgccrf.git
cd analyse-dgccrf
pip install -r requirement.txt
```

### 2. Collecter les données HTML 

```bash
python scrap.py
```
Ce script collecte les données des pages HTML (stockées dans `/html_dgccrf`) et les stocke dans une table .csv (`dataframe_dgccrf_{date du jour}.csv`)

*Note :* Par soucis d'anonymisation des entreprises et car les affichages par la DGCCRF sont temporaires, les pages ne sont pas fournies. A vous de les télécharger et de les placer dans `/html_dgccrf`

### 3. Collecter les données SIRET

```bash
python siret_extract.py
```
Ce script collecte les SIRET et codes NAF (stockés dans `/table_siret`) et les stocke dans une table .csv (`siret_base.csv`)

*Note :* Étant donné que la base de données des siret pèse 9 gigaoctets, elle n'est pas disponible dans ce repo mais téléchargeable à l'adresse `https://www.data.gouv.fr/datasets/base-sirene-des-entreprises-et-de-leurs-etablissements-siren-siret`

### 3. Lancer l'analyse

```bash
jupyter notebook analyse.ipynb
```
Le notebook produit les fichiers CSV nettoyés dans le dossier `rapport_bi`. Ce dernier est complémentaire du fichier `functions.py` qui intègre l'ensemble de ses fonctions d'analyse.


### 4. Consulter le rapport Power BI

Le rapport est disponible au Power BI desktop (nécessaire pour lancer le rapport) : `rapport-dgccrf.pbix`

## Limites et pistes futures

Mon analyse **relève d'une limite qu'il est important de mentionner**. Le nombre d'amendes publiées sur le site de la DGCCRF est relativement faible (*115 amendes*). Ceci a un impact sur les données obtenues, réduisant la puissance des conclusions de l'analyse. De plus, la méthode de collecte utilisée a également impacté la qualité des données récupérées, réduisant la taille de l'échantillon.

A l'avenir, il serait pertinent de collecter plus de données de sanctions publiées par la DGCCRF et de les passer dans ce pipeline, afin de constater si les résultats obtenus se confirment ou non. Également, croiser plus finement les SIRET et les sanctions, notamment en comparant sur le nombre d'entreprises par sous-division du NAF serait un projet pertinent pour confirmer mes résultats.