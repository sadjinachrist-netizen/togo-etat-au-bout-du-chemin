#!/bin/bash
# Reconstruit le rapport, le dossier Livrables et l'archive de soumission.
set -e
cd "D:/coursprojets/Data_Challenges_Togo_AI_Lab/Open_Data_Challenge"
node rapport/build_pptx.js
rm -rf Livrables
mkdir -p Livrables/captures Livrables/code/data
cp rapport/Rapport_Etat_au_bout_du_chemin_Togo.pptx Livrables/
cp README.md SOURCES.md catalogue/liens_jeux_utilises.json Livrables/
cp app/qa/*.png Livrables/captures/
cp app/data/processed/prefectures.csv Livrables/togo_indice_acces_prefectures.csv
cp app/data/processed/regions.csv  Livrables/togo_indice_acces_regions.csv
rm -rf app/lib/__pycache__ app/views/__pycache__
cp -r app/app.py app/requirements.txt app/lib app/views app/pipeline app/tools app/assets app/.streamlit README.md Livrables/code/
cp -r app/data/raw app/data/geo app/data/processed Livrables/code/data/
cp app/data/liens_jeux_utilises.json Livrables/code/data/
python - <<'PY'
import zipfile, pathlib
root = pathlib.Path("Livrables")
out = pathlib.Path("Soumission_Open_Data_Challenge_Defi01_SADJINA_Christ.zip")
out.unlink(missing_ok=True)
n = 0
with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
    for p in sorted(root.rglob("*")):
        if p.is_file():
            z.write(p, p.relative_to(root.parent)); n += 1
print(f"archive : {n} fichiers, {out.stat().st_size/1e6:.1f} Mo")
PY
