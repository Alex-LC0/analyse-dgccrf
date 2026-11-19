import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
import datetime

today = datetime.datetime.today().strftime("%d_%m_%Y")
siret_list = []  #  Liste de stockage des données de Siret
tarif_am = []  #  Liste de stockage des montant des amendes
tag_am = []  #  Liste de stockage des causes d'amendes

print("\n === LANCEMENT DU SCRIPT DE COLLECTE DES DONNÉES ===")
print(" ")
print(f"Les données sont datée du {today}")

for n in range(1, 8):
    with open(
        f"html_dgccrf/page_{n}.html", encoding="utf-8"
    ) as f:  #  Ouverture du fichier HTML sauvegardé en local
        soup = BeautifulSoup(f, "html.parser")  #  Extraction du code HTML
        print(f"Page {n} chargée")
    for a in soup.find_all(
        "a", href=re.compile(r"/amende")
    ):  #  Extraction des codes amendes
        text = a.get_text(strip=True)  #  Récupération du texte
        chiffre = re.sub(r"\D", "", text)  #  Isolement des chiffres de la string
        size_chiffre = len(chiffre)  #  Calcul de la taile de la string pour indexing
        siret = chiffre[-14:]  #  Indexing sur le siret (14 chiffres)
        tarif = chiffre[: size_chiffre - 14]  #  Indexing sur l'amendes
        siret_list.append(siret)  #  Stockage des données dans la liste
        tarif_am.append(tarif)  #  Stockage des données dans la liste
    for card in soup.select(
        "div.views-row"
    ):  #  Récupération des tags dans l'ensemble de la page
        tags = [
            p.get_text(strip=True) for p in card.select("ul.fr-tags-group p.fr-tag")
        ]  #  Récupération de l'ensemble des tags
        tags_1 = tags[0] if len(tags) > 0 else None  #  Récupération du tag 1
        tags_2 = tags[1] if len(tags) > 1 else None  #  Récupération du tag 2
        if tags_1 == "Protection économique du consommateur":  #  Filtrage du tag
            tag_am.append(tags_2)
        else:
            tag_am.append(tags_1)

    print(f"Page {n} collectée")

df = pd.DataFrame(
    zip(siret_list, tarif_am, tag_am), columns=["Siret", "Amende", "Raison amende"]
)  #  Création d'un dataframe pour stockage en .csv

df.to_csv(f"table_dgccrf/dataframe_dgccrf_{today}.csv", index=False)

print("\n === RESULTAT DU SCRIPT ===")
print("L'ensemble des données ont été collectée et stockée dans un .csv")
