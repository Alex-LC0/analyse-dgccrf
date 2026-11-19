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

La **phase de nettoyage** a fais perdre : 

- 11.45% des données pour les sanctions de la DGCCRF
- 0.048% des données pour la base des SIRET
- 19.06% des données pour les code NAF

La **phase d'analyse** nous a informé sur : 

- Certains secteurs semblent être plus affichés que d'autres par la DGCCRF
- Les délais de paiement entre entreprise est la cause la plus affichée sur la période collectée (% A METTRE)
- Le Commerce de gros, à l'exception des automobiles et des motocycles est le plus représenter en nombre d'amendes (16.52%) et en quantité (14.70%)


## Contexte

La DGCCRF est un organisme de l'État français ayant pour mission le contrôle du respect de la concurrence, de l'économie et des consommateurs. Ainsi, il peut sanctionner des organisme, des individus ou des entreprises si ces derniers ne respectent pas les lois en vigeur. (*Source : Site de la DGCCRF*)

Dans une logique de prévention des consommateurs et des acteurs économiques, la DGCCRF peut dans certains cas appliquer une sanction supplémentaire : **l'affichage public de l'entreprise et de la sanction qui lui est imposée**. Ces sanctions peuvent concerner : des pratiques commerciales déloyales, des défauts d’affichage des prix, la commercialisation de produits non conformes ou dangereux, des pratiques anticoncurrentielles locales ou restrictives de concurrence, le non-respect des délais de paiement interentreprises, etc. Dès lors, l'ensemble des acteurs économiques possèdent l'information sur cet entreprise/individu. (*Source : Site de la DGCCRF*)

Il est donc intéressant de s'intéresser à ces publications de sanctions, et les secteurs les plus à même de recevoir ce genre de sanctions, et c'est l'objectif de cette analyse. Cependant, je tiens à rappeler que cette dernière ne porte aucunement sur les secteurs les plus à risque de sanction, car l'échantillon des sanctions publiée par la DGCCRF est largement plus faible que celles appliquée tout au long de l'année. 

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
├── scrap.py                     # Script d'extraction des données des pages HTML
├── siret_extract.py             # Script d'extraction des données de la table SIRET
├── dgccrf.pbix                  # Rapport Power BI du projet
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
Ce script collectes les données des pages HTML (stockée dans `/html_dgccrf`) et les stock dans une table .csv (`dataframe_dgccrf_{date du jour}.csv`)

*Note :* Par soucis d'anonymisation des entreprises et car les affichages par la DGCCRF sont temporaire, les pages ne sont pas fournies. A vous de les télécharger et de les placer dans `/html_dgccrf`

### 3. Collecter les données SIRET

```bash
python siret_extract.py
```
Ce script collectes les SIRET et codes NAF (stockée dans `/table_siret`) et les stock dans une table .csv (`siret_base.csv`)

*Note :* Étant donné que la base de données des siret pèse 9 gigaoctets, elle n'est pas disponible dans ce repo mais téléchargeable à l'adresse `https://www.data.gouv.fr/datasets/base-sirene-des-entreprises-et-de-leurs-etablissements-siren-siret`

### 3. Lancer l'analyse

```bash
jupyter notebook analyse.ipynb
```
Le notebook produit les fichiers CSV nettoyés dans le dossier `X`.


### 4. Consulter le rapport Power BI

Le rapport est disponible au Power BI desktop (nécessaire pour lancer le rapport) : `dgccrf.pbix`

## Limites et pistes futures

- La taille du jeu de donnée de la DGCCRF est relativement faible (115 amendes publiées), ce qui réduit la puissance des conclusions de cette analyse
- La focalisation sur les amendes publiées expose plus les problèmes inter entreprises que les atteintes aux consommateurs (notamment vis à vis de l'économie des contrats)
- Relative propretée des données collectées sur le site, avec certains SIRET non renseigné réduisant les données récupérées 
- Etudier ces SIRET pour les démarchages car secteurs étranges