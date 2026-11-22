# L'État au bout du chemin

**Où les services publics s'arrêtent au Togo — et si l'argent public va là où le manque est.**

Tableau de bord produit pour l'**Open Data Challenge · Défi 01** (thème libre) du Togo AI Lab /
MESPTN, novembre 2026. Auteur : **SADJINA Christ**.

---

## Le propos en trois phrases

Un Togolais sur six vit dans une préfecture où l'eau, l'électricité, les services financiers et la
route manquent **tous les quatre à la fois**. Ce tableau de bord construit, à partir de 16 jeux de
données ouverts du portail national, un indice d'accès comparable sur les 39 préfectures. Il
confronte ensuite cet indice aux 813 ouvrages du projet COSO — le seul jeu ouvert qui publie une
dépense publique réelle, géolocalisée et chiffrée — pour répondre à une question simple :
**l'investissement va-t-il là où le besoin est le plus grand ?**

## Les trois résultats

1. **Les Plateaux sont l'angle mort.** Cinq des dix préfectures les moins bien servies du pays sont
   dans les Plateaux (Akébou, Anié, Haho, Est-Mono, Moyen-Mono), soit 814 000 habitants, et aucune
   ne relève d'un programme d'investissement communautaire identifiable dans les données ouvertes.
   Akébou ferme le classement national avec 3,7 % d'accès à l'électricité et zéro ouvrage.

2. **À l'intérieur de la zone COSO, l'argent va au moins mal servi.** La corrélation entre
   l'investissement par habitant et le niveau d'accès y vaut **+0,63**. Les quatre préfectures les
   plus mal servies de la zone ont reçu 6 061 F CFA par habitant ; les quatre mieux servies,
   11 767 F — 1,9 fois plus. Le ciblage *régional* du projet est juste ; sa répartition *interne*
   est inversée par rapport au besoin mesuré.

3. **Le courant est le maillon faible.** L'électricité est le premier point noir de 19 préfectures
   sur 39, et c'est la seule dimension encore publiée sur un découpage commercial antérieur aux
   39 préfectures : six zones en regroupent deux à la fois, ce qui rend cinq préfectures invisibles.

## Les données

**16 jeux, 17 fichiers, 100 % téléchargés depuis [opendata.gouv.tg](https://opendata.gouv.tg).**
La liste complète, avec le lien de la page de chaque jeu et le lien de téléchargement direct du
fichier exact utilisé, est dans [`catalogue/liens_jeux_utilises.json`](catalogue/liens_jeux_utilises.json)
et affichée dans la page « Méthode & sources » du tableau de bord.

Producteurs : INSEED · Ministère de l'Eau et de l'Assainissement · Ministère des Mines et des
Ressources énergétiques · Ministère des Transports · Ministère de l'Économie et des Finances ·
ANADEB (projet COSO).

Seul apport extérieur : les **contours de préfectures** (geoBoundaries, dérivés d'OpenStreetMap,
millésime 2017), faute de référentiel géographique publié sur le portail national. Ils servent
uniquement à dessiner les cartes et n'entrent dans **aucun** calcul.

## L'indice d'accès

Quatre dimensions, ramenées à l'habitant puis normalisées de 0 à 100 sur les 39 préfectures, et
moyennées à parts égales :

| Dimension | Indicateur | Source |
|---|---|---|
| Eau | points d'eau (PEA + PMH) pour 10 000 habitants | Ministère de l'Eau |
| Électricité | taux d'accès basse tension 2021 | CEET |
| Services financiers | établissements + agents mobile money pour 10 000 habitants | Min. Économie / MESPTN |
| Mobilité | mètres de route classée par habitant | Ministère des Transports |

L'indice est **relatif** : 0 = la moins bien dotée des 39, 100 = la mieux dotée. Il mesure une
**couverture**, pas un niveau de bien-être. Les cinq limites de l'exercice sont énoncées dans la
page « Méthode & sources » du tableau de bord, pas seulement ici.

## Faire tourner le projet

```bash
pip install -r app/requirements.txt
python app/pipeline/build_data.py     # reconstruit toutes les tables agrégées
streamlit run app/app.py
```

```
app/
├─ app.py                     navigation et barre latérale
├─ pipeline/build_data.py     tout le calcul, en un seul script
├─ data/raw/                  les 17 fichiers téléchargés, non modifiés
├─ data/processed/            les tables agrégées lues par les pages
├─ data/liens_jeux_utilises.json
├─ lib/ui.py                  charte graphique
├─ lib/data.py                chargement et filtres globaux
└─ views/                     une page par fichier
```

Aucun calcul n'est fait dans les pages : elles lisent les tables produites par le pipeline. Tout
chiffre affiché est donc reproductible en relançant un seul script.

## Trois anomalies signalées au producteur

- Le jeu intitulé « RGPH-5 2022 » sur le portail contient en réalité les effectifs de 2010 (total
  national 6,19 M contre 8,10 M au RGPH-5). Le vrai RGPH-5 est publié sous un autre slug.
- La série de scolarisation ventilée par sexe donne des taux « nets » supérieurs à 100 % dans six
  régions sur sept ; au Kara, le Total publié est inférieur à ses deux composantes.
- Plusieurs jeux exposent deux CSV dont l'un est le dictionnaire des champs, sans que les
  métadonnées le distinguent : un script de téléchargement naïf récupère le mauvais fichier.

---

SADJINA Christ — Open Data Challenge · Défi 01, Togo AI Lab / MESPTN, novembre 2026.
Les données sont publiques ; les calculs, les choix de méthode et les erreurs éventuelles sont les
miens.
