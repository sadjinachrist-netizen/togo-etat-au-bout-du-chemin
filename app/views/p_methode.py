"""Méthode, sources et limites."""
import json

import pandas as pd
import streamlit as st

from lib import data as D
from lib import ui

k = D.kpi()
flt = D.sidebar_filters()
pref = D.prefectures()

ui.header("Méthode & sources",
          "Tout ce qui est affiché dans ce tableau de bord est reconstructible à partir de cette "
          "page : les 16 jeux ouverts utilisés avec leurs liens de téléchargement, le calcul exact "
          "de l'indice, et les cinq limites qui en bornent la portée.")

# ------------------------------------------------------------------ 01
ui.section("01", "Provenance des données", "La consigne du défi est respectée et vérifiable.")
ui.kpis([
    dict(label="Jeux de données utilisés", value="16",
         sub="17 fichiers, tous téléchargés depuis le portail national",
         source="opendata.gouv.tg"),
    dict(label="Part venant d'opendata.gouv.tg", value="100 %", tone="",
         sub="aucune donnée chiffrée ne vient d'une autre source",
         source="voir le tableau ci-dessous"),
    dict(label="Producteurs publics distincts", value="6", tone="slate",
         sub="INSEED, Min. Eau, Min. Mines & Énergie, Min. Transports, Min. Économie, ANADEB",
         source="métadonnées des jeux"),
    dict(label="Seul apport extérieur", value="Contours", tone="gold",
         sub="les polygones de préfectures viennent de geoBoundaries (OpenStreetMap, 2017) : "
             "aucune valeur du tableau de bord n'en dépend",
         source="geoboundaries.org"),
])

ui.note(
    "<b>Pourquoi un fond de carte extérieur.</b> Le portail national publie des points et des "
    "tracés géolocalisés, mais aucun jeu de polygones des 39 préfectures. Les contours utilisés ici "
    "viennent donc de geoBoundaries (dérivés d'OpenStreetMap, millésime 2017) et servent "
    "<i>uniquement</i> à dessiner les cartes : ils n'entrent dans aucun calcul. Ils datent d'avant "
    "le découpage actuel, ce qui explique les 36 contours pour 39 préfectures. Publier le "
    "référentiel géographique officiel des 39 préfectures en données ouvertes rendrait ce "
    "tableau de bord 100 % national.", "gold")

# ------------------------------------------------------------------ 02
ui.section("02", "Les 16 jeux utilisés, avec leurs liens",
           "Chaque ligne renvoie à la page du jeu sur le portail et au fichier exact téléchargé.")
L = json.loads((D.ROOT / "data" / "liens_jeux_utilises.json").read_text(encoding="utf-8"))
rows = []
for e in L:
    for f in e["fichiers"]:
        if f.get("role") != "données":
            continue
        rows.append({"Jeu de données": e["nom"], "Producteur": e["producteur"].strip(),
                     "Format": f["format"], "Fichier local": f["fichier"],
                     "Page du jeu": e["page"], "Téléchargement direct": f["url"]})
tbl = pd.DataFrame(rows)
st.dataframe(tbl, hide_index=True, use_container_width=True, height=520,
             column_config={"Page du jeu": st.column_config.LinkColumn("Page du jeu",
                                                                       display_text="ouvrir"),
                            "Téléchargement direct": st.column_config.LinkColumn(
                                "Téléchargement", display_text="fichier")})
st.download_button("Télécharger la liste complète des sources (JSON)",
                   data=json.dumps(L, ensure_ascii=False, indent=2).encode("utf-8"),
                   file_name="liens_jeux_utilises.json", mime="application/json")
st.caption("Le fichier JSON inclut en outre les dictionnaires de champs téléchargés, la remarque "
           "sur le jeu de population mal millésimé, et les 11 jeux sectoriels COSO qui composent "
           "l'inventaire agrégé.")

# ------------------------------------------------------------------ 03
ui.section("03", "Le calcul de l'indice, au complet")
st.markdown(r"""
**Étape 1 — numérateurs.** Les points de service sont comptés par préfecture après rattachement
géographique. Pour l'eau : PEA + PMH. Pour les services financiers : établissements de finance +
agents mobile money. Pour la mobilité : longueur du réseau classé, obtenue en sommant les distances
orthodromiques (formule de haversine) entre points successifs de chaque `MULTILINESTRING` publié.

**Étape 2 — dénominateur.** Population 2022 par préfecture (RGPH-5). Les 39 préfectures actuelles
sont reconstituées, y compris Mô et Avé, absentes de plusieurs jeux géolocalisés.

**Étape 3 — ratios.**

- eau : `points d'eau / population × 10 000`
- services financiers : `points financiers / population × 10 000`
- mobilité : `mètres de route classée / population`
- électricité : taux d'accès basse tension CEET 2021, repris tel quel

**Étape 4 — normalisation min-max sur les 39 préfectures.** Pour chaque dimension :

$$\text{score} = 100 \times \frac{x - x_{\min}}{x_{\max} - x_{\min}}$$

**Étape 5 — indice.** Moyenne arithmétique non pondérée des quatre scores.

**Étape 6 — cartographie.** Les 39 préfectures sont agrégées sur les 36 contours disponibles par
moyenne pondérée par la population (Agoè-Nyivé dans Golfe, Kpendjal-Ouest dans Kpendjal, Oti-Sud
dans Oti). Cette agrégation ne concerne que l'affichage des cartes, jamais les classements.
""")

# ------------------------------------------------------------------ 04
ui.section("04", "Cinq limites, assumées",
           "Aucune ne casse les constats de la page de synthèse, toutes en bornent la portée.")
LIM = [
    ("L'électricité est publiée sur un découpage périmé",
     "La CEET publie son taux d'accès BT par zone commerciale. Six zones regroupent deux "
     "préfectures : les valeurs de Kpendjal-Ouest, Oti-Sud, Anié, Moyen-Mono et Mô sont héritées de "
     "leur préfecture d'origine. Cela ne peut que <b>surestimer</b> leur accès, jamais le "
     "sous-estimer — les constats sur ces préfectures sont donc conservateurs.",
     "Dimension électricité"),
    ("Certains taux dépassent 100 %",
     "Le Zio affiche 106,8 % d'accès BT : le numérateur compte les abonnés, le dénominateur les "
     "ménages estimés. Un abonné non résidentiel ou un compteur partagé suffit à franchir le seuil. "
     "Ces valeurs sont conservées telles que publiées et signalées, plutôt que rognées à 100 % — "
     "rogner reviendrait à modifier la source.",
     "Qualité de la source"),
    ("Un point d'eau recensé n'est pas un point d'eau qui coule",
     "Les inventaires PEA et PMH recensent les ouvrages, mais ne publient ni champ d'état de "
     "service ni date de dernier contrôle — à la différence des annuaires d'agences, qui "
     "signalent 97 points fermés. L'indice mesure donc une <b>couverture théorique</b> : une "
     "préfecture au parc ancien et mal entretenu y apparaît mieux servie qu'elle ne l'est.",
     "Dimension eau"),
    ("Le réseau mesuré est le réseau classé",
     "Les pistes rurales, qui portent l'essentiel du dernier kilomètre, ne figurent dans aucun jeu "
     "ouvert géoréférencé. Mô apparaît à 0 mètre de route classée : c'est exact au sens du réseau "
     "structurant, et cela ne veut pas dire qu'aucune voie n'y existe.",
     "Dimension mobilité"),
    ("L'indice est relatif, et non pondéré",
     "Un score de 100 signifie « la mieux dotée des 39 », pas « bien dotée ». Et les quatre "
     "dimensions pèsent à parts égales, faute de base pour hiérarchiser les besoins. Les quatre "
     "scores restent donc visibles séparément dans tout le tableau de bord, afin que le lecteur "
     "puisse refaire sa propre pondération.",
     "Construction de l'indice"),
]
for i, (t, c, tag) in enumerate(LIM, 1):
    st.markdown(f"<div class='reco'><span class='n gold' style='background:{ui.C['gold']}'>{i}</span>"
                f"<span class='t'>{t}</span>"
                f"<span class='tag gold' style='float:right;margin-top:.45rem'>{tag}</span>"
                f"<p>{c}</p></div>", unsafe_allow_html=True)

# ------------------------------------------------------------------ 05
ui.section("05", "Trois anomalies signalées au producteur",
           "Trouvées en travaillant les jeux, elles valent d'être remontées.")
c1, c2, c3 = st.columns(3)
c1.markdown(
    "<div class='note red'><b>Jeu de population mal millésimé.</b> Le jeu intitulé « RGPH-5 2022 » "
    "sur le portail contient en réalité les effectifs du recensement de 2010 : son total national "
    "est de 6,19 millions, contre 8,10 millions au RGPH-5. Le vrai RGPH-5 est publié sous un autre "
    "slug. Les deux sont utilisés ici, chacun à sa bonne date.</div>", unsafe_allow_html=True)
c2.markdown(
    "<div class='note red'><b>Scolarisation : ventilation par sexe inutilisable.</b> La série "
    "« Féminin » dépasse 100 % dans six régions sur sept, ce qui est impossible pour un taux net. "
    "Au Kara, le Total publié est inférieur à ses deux composantes. Seule la colonne « Total » est "
    "exploitée ici.</div>", unsafe_allow_html=True)
c3.markdown(
    "<div class='note red'><b>Dictionnaires de champs servis comme données.</b> Plusieurs jeux "
    "exposent deux CSV, dont l'un est le dictionnaire des champs, sans que les métadonnées le "
    "distinguent clairement. Un script naïf télécharge le mauvais fichier. Un champ "
    "<code>role</code> dans l'API éviterait l'erreur.</div>", unsafe_allow_html=True)

# ------------------------------------------------------------------ 06
ui.section("06", "Reproduire ce travail")
st.markdown("""
Le tableau de bord est écrit en Python. Un seul script reconstruit toutes les tables agrégées à
partir des 17 fichiers bruts, et les pages ne font que lire ces tables — aucun calcul n'est caché
dans l'interface.

```
app/
├─ pipeline/build_data.py     recalcule tout : python pipeline/build_data.py
├─ data/raw/                  les 17 fichiers téléchargés, non modifiés
├─ data/processed/            les tables agrégées lues par les pages
├─ data/liens_jeux_utilises.json   la liste des sources, avec les liens
├─ lib/                       charte graphique et chargement des données
└─ views/                     une page par fichier
```
""")
st.download_button("Télécharger la table des 39 préfectures (CSV)",
                   data=pref.to_csv(index=False).encode("utf-8-sig"),
                   file_name="togo_indice_acces_prefectures.csv", mime="text/csv")

ui.note(
    "<b>Auteur.</b> SADJINA Christ — Open Data Challenge · Défi 01, Togo AI Lab / MESPTN, "
    "novembre 2026. Les données sont publiques ; les calculs, les choix de méthode et les erreurs "
    "éventuelles sont les miens. Toute correction est bienvenue : elle se vérifie en relançant un "
    "seul script.")
