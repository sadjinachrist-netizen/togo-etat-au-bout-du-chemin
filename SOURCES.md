# Sources des données

**16 jeux de données, 17 fichiers — 100 % téléchargés depuis le portail national [opendata.gouv.tg](https://opendata.gouv.tg).**

Seul apport extérieur au portail : les contours de préfectures ([geoBoundaries](https://www.geoboundaries.org), dérivés d'OpenStreetMap, millésime 2017), utilisés uniquement pour dessiner les cartes — ils n'entrent dans aucun calcul.

---

## 1. Recensement Général de la Population et de l'Habitat (RGPH-5, 2022)

- **Producteur** : Institut National de la Statistique et des Études Économiques et Démographiques
- **Usage** : Population 2022 par préfecture — dénominateur de tous les ratios par habitant.
- **Page du jeu** : https://opendata.gouv.tg/datasets/donnee-ouverte-de-recensement-general-de-la-population-et-de-lhabitat-rgph
- **Fichier (données)** : `population_rgph5_2022.csv` — https://opendata.gouv.tg/s/resources/donnee-ouverte-de-recensement-general-de-la-population-et-de-lhabitat-rgph/20241227-082722/observationdata-kwwolwb.csv

## 2. Population par subdivision administrative (effectifs 2010)

- **Producteur** : Institut National de la Statistique et des Études Économiques et Démographiques
- **Page du jeu** : https://opendata.gouv.tg/datasets/donnees-ouvertes-sur-la-population-par-subdivision-administrative-du-togo
- **Fichier (données)** : `population_2010.csv` — https://opendata.gouv.tg/s/resources/donnees-ouvertes-sur-la-population-par-subdivision-administrative-du-togo/20241226-182338/observationdata-sapxctg.csv
- **⚠ Remarque** : Jeu intitulé RGPH-5 2022 sur le portail, mais dont les effectifs correspondent au recensement de 2010 (vérifié par recoupement avec le total national publié). Utilisé ici comme base 2010 pour mesurer la croissance, et non comme population de référence.

## 3. Taux d'accès à l'électricité par préfecture

- **Producteur** : Institut National de la Statistique et des Études Économiques et Démographiques
- **Page du jeu** : https://opendata.gouv.tg/datasets/donnees-ouvertes-sur-le-taux-dacces-a-lelectricite-par-prefecture-au-togo
- **Fichier (données)** : `electricite_taux_prefecture.csv` — https://opendata.gouv.tg/s/resources/donnees-ouvertes-sur-le-taux-dacces-a-lelectricite-par-prefecture/20241226-145522/observationdata-puncgpd.csv

## 4. Agences de la CEET (électricité)

- **Producteur** : Ministère des Mines et des Ressources Énergétiques
- **Page du jeu** : https://opendata.gouv.tg/datasets/donnees-ouvertes-sur-les-agences-de-la-ceet
- **Fichier (données)** : `agences_ceet.csv` — https://opendata.gouv.tg/s/resources/donnees-ouvertes-sur-les-agences-de-la-ceet/20241223-110618/agences-ceet.csv
- **Fichier (dictionnaire de champs)** : `(non conservé)` — https://opendata.gouv.tg/s/resources/donnees-ouvertes-sur-les-agences-de-la-ceet/20241223-110716/file-agences-ceet-23-12-2024-11-06-42.csv

## 5. Agences de la Togolaise des Eaux

- **Producteur** : Ministère de l’Eau et de l’Assainissement
- **Page du jeu** : https://opendata.gouv.tg/datasets/donnees-ouvertes-sur-les-agences-togolaise-des-eaux-tde
- **Fichier (données)** : `agences_tde.csv` — https://opendata.gouv.tg/s/resources/donnees-ouvertes-sur-les-agences-togolaise-des-eaux-tde/20241219-174958/file-agences-togolaise-des-eaux-tde-19-12-2024-17-48-23.csv
- **Fichier (dictionnaire de champs)** : `(non conservé)` — https://opendata.gouv.tg/s/resources/donnees-ouvertes-sur-les-agences-togolaise-des-eaux-tde/20241219-174740/agences-togolaise-des-eaux-tde-.csv

## 6. Postes d'Eau Autonomes (PEA)

- **Producteur** : Ministère de l’Eau et de l’Assainissement
- **Page du jeu** : https://opendata.gouv.tg/datasets/donnees-ouvertes-sur-les-postes-deau-autonomes-pea-au-togo
- **Fichier (données)** : `eau_pea.csv` — https://opendata.gouv.tg/s/resources/donnees-ouvertes-sur-les-postes-deau-autonomes-pea-au-togo/20241223-105106/file-postes-deau-autonomes-pea-23-12-2024-10-50-37.csv
- **Fichier (dictionnaire de champs)** : `(non conservé)` — https://opendata.gouv.tg/s/resources/donnees-ouvertes-sur-les-postes-deau-autonomes-pea-au-togo/20241223-105002/postes-deau-autonomes-pea-.csv

## 7. Pompes à Motricité Humaine (PMH)

- **Producteur** : Ministère de l’Eau et de l’Assainissement
- **Page du jeu** : https://opendata.gouv.tg/datasets/donnees-ouvertes-sur-les-pompes-a-motricite-humaine-pmh-au-togo
- **Fichier (données)** : `eau_pmh.csv` — https://opendata.gouv.tg/s/resources/donnees-ouvertes-sur-les-pompes-a-motricite-humaine-pmh-au-togo/20241223-104710/file-pompes-a-motricite-humaine-pmh-23-12-2024-10-44-36.csv
- **Fichier (dictionnaire de champs)** : `(non conservé)` — https://opendata.gouv.tg/s/resources/donnees-ouvertes-sur-les-pompes-a-motricite-humaine-pmh-au-togo/20241223-104357/pompes-a-motricite-humaine-pmh-.csv

## 8. Formations sanitaires par type et par région

- **Producteur** : Institut National de la Statistique et des Études Économiques et Démographiques
- **Page du jeu** : https://opendata.gouv.tg/datasets/donnees-ouvertes-sur-les-formations-sanitaires-par-type-et-par-region-au-togo
- **Fichier (données)** : `sante_formations.csv` — https://opendata.gouv.tg/s/resources/donnees-ouvertes-sur-les-formations-sanitaires-par-type-et-par-region-au-togo/20250103-170630/observationdata-mtdaogb.csv

## 9. Densité démographique des infrastructures sanitaires

- **Producteur** : Institut National de la Statistique et des Études Économiques et Démographiques
- **Page du jeu** : https://opendata.gouv.tg/datasets/donnees-ouvertes-sur-la-densite-demographique-des-infrastructures-sanitaires-au-togo
- **Fichier (données)** : `sante_densite.csv` — https://opendata.gouv.tg/s/resources/donnees-ouvertes-sur-la-densite-demographique-des-infrastructures-sanitaires-au-togo/20250102-182640/observationdata-ghqqsde.csv

## 10. Taux de pauvreté et revenus

- **Producteur** : Institut National de la Statistique et des Études Économiques et Démographiques
- **Page du jeu** : https://opendata.gouv.tg/datasets/donnees-ouvertes-sur-le-taux-de-pauvrete-et-revenus-au-togo
- **Fichier (données)** : `pauvrete.csv` — https://opendata.gouv.tg/s/resources/donnees-ouvertes-sur-pauvrete-et-revenus-au-togo/20241226-160154/observationdata-lknstac.csv

## 11. Taux net de scolarisation au primaire par région

- **Producteur** : Institut National de la Statistique et des Études Économiques et Démographiques
- **Page du jeu** : https://opendata.gouv.tg/datasets/donnees-ouvertes-sur-le-taux-net-de-scolarisation-au-primaire-par-region-au-togo
- **Fichier (données)** : `scolarisation_primaire.csv` — https://opendata.gouv.tg/s/resources/donnees-ouvertes-sur-le-taux-net-de-scolarisation-au-primaire-par-region-au-togo/20250109-182944/observationdata-vzztmjc.csv

## 12. Entreprises auto-écoles

- **Producteur** : Ministère des Transports
- **Page du jeu** : https://opendata.gouv.tg/datasets/donnees-ouvertes-sur-les-entreprises-auto-ecoles-au-togo
- **Fichier (données)** : `auto_ecoles.csv` — https://opendata.gouv.tg/s/resources/donnees-ouvertes-sur-les-entreprises-auto-ecoles-au-togo/20250102-162842/file-entreprises-auto-ecoles-02-01-2025-16-28-05.csv
- **Fichier (dictionnaire de champs)** : `(non conservé)` — https://opendata.gouv.tg/s/resources/donnees-ouvertes-entreprises-auto-ecoles/20241218-100922/entreprises-auto-ecoles.csv

## 13. Routes classées (tracés géolocalisés)

- **Producteur** : Ministère des Transports
- **Page du jeu** : https://opendata.gouv.tg/datasets/donnees-ouvertes-sur-les-routes-routes-classees-au-togo
- **Fichier (données)** : `routes_classees.csv` — https://opendata.gouv.tg/s/resources/donnees-ouvertes-sur-les-routes-routes-classees-au-togo/20241218-203810/file-routes-routes-classees-18-12-2024-20-38-02.csv
- **Fichier (dictionnaire de champs)** : `(non conservé)` — https://opendata.gouv.tg/s/resources/donnees-ouvertes-sur-les-routes-routes-classees-au-togo/20241218-150814/routes-routes-classees.csv

## 14. Agents mobile money

- **Producteur** : Ministère de l'Éfficacité du Service Public et de la Transformation Numérique
- **Page du jeu** : https://opendata.gouv.tg/datasets/donnees-ouvertes-sur-les-agents-mobile-money-au-togo
- **Fichier (données)** : `agents_mobile_money.csv` — https://opendata.gouv.tg/s/resources/donnees-ouvertes-sur-les-agents-mobile-money-au-togo/20241219-165539/file-agents-mobile-money-19-12-2024-16-55-32.csv
- **Fichier (dictionnaire de champs)** : `(non conservé)` — https://opendata.gouv.tg/s/resources/donnees-ouvertes-sur-les-agents-mobile-money-au-togo/20241217-162510/agents-mobile-money.csv

## 15. Inventaire des sous-projets du Projet COSO

- **Producteur** : Ministère du Développement à la Base, de l'Inclusion Financière, de la Jeunesse et de l'Emploi des Jeunes
- **Usage** : 813 ouvrages géolocalisés et chiffrés — confrontation de la dépense publique au besoin mesuré.
- **Page du jeu** : https://opendata.gouv.tg/datasets/inventaire-des-sous-projets-dinfrastructure-realises-dans-le-cadre-du-projet-coso-au-togo
- **Fichier (données)** : `coso_inventaire.geojson` — https://opendata.gouv.tg/s/resources/inventaire-des-sous-projets-dinfrastructure-realises-dans-le-cadre-du-projet-coso-au-togo/20260603-175704/subprojects-opendata.geojson
- **Fichier (dictionnaire de champs)** : `(non conservé)` — https://opendata.gouv.tg/s/resources/inventaire-des-sous-projets-dinfrastructure-realises-dans-le-cadre-du-projet-coso-au-togo/20260603-175702/subprojects-opendata.csv
- **Fichier (données)** : `coso_inventaire.csv` — https://opendata.gouv.tg/s/resources/inventaire-des-sous-projets-dinfrastructure-realises-dans-le-cadre-du-projet-coso-au-togo/20260603-175702/subprojects-opendata.csv
- **Jeux sectoriels liés** (11) :
  - https://opendata.gouv.tg/datasets/projet-coso-infrastructures-de-sport-et-loisir-au-togo
  - https://opendata.gouv.tg/datasets/projet-coso-infrastructures-du-secteur-de-la-sante-au-togo
  - https://opendata.gouv.tg/datasets/projet-coso-ouvrages-de-desenclavement-et-pistes-rurales-au-togo
  - https://opendata.gouv.tg/datasets/projet-coso-actions-du-secteur-de-lenvironnement-au-togo
  - https://opendata.gouv.tg/datasets/projet-coso-infrastructures-du-secteur-de-lenergie-au-togo
  - https://opendata.gouv.tg/datasets/projet-coso-infrastructures-du-secteur-de-leducation-au-togo
  - https://opendata.gouv.tg/datasets/projet-coso-infrastructures-dalimentation-en-eau-potable-et-hydraulique-au-togo
  - https://opendata.gouv.tg/datasets/projet-coso-infrastructures-de-developpement-a-la-base-et-cohesion-sociale-au-togo
  - https://opendata.gouv.tg/datasets/projet-coso-infrastructures-du-secteur-du-commerce-et-des-marches-au-togo
  - https://opendata.gouv.tg/datasets/projet-coso-infrastructures-du-secteur-de-lassainissement-au-togo
  - https://opendata.gouv.tg/datasets/projet-coso-infrastructures-du-secteur-de-lagriculture-au-togo

## 16. Établissements de finance au Togo

- **Producteur** : Ministère de l'Économie et des Finances
- **Usage** : Banques, IMF et bureaux de change géolocalisés — dimension « services financiers ».
- **Page du jeu** : https://opendata.gouv.tg/datasets/donnees-ouvertes-sur-les-etablissements-de-finance-au-togo
- **Fichier (données)** : `etablissements_finance.csv` — https://opendata.gouv.tg/s/resources/donnees-ouvertes-sur-les-etablissements-de-finance-au-togo/20250107-113010/file-finance-etablissements-07-01-2025-11-07-50.csv
- **Fichier (dictionnaire de champs)** : `(non conservé)` — https://opendata.gouv.tg/s/resources/donnees-ouvertes-sur-les-etablissements-de-finance-au-togo/20250107-113744/metadonnee-finance-etablissements.csv

---

SADJINA Christ — Open Data Challenge · Défi 01, Togo AI Lab / MESPTN, novembre 2026.