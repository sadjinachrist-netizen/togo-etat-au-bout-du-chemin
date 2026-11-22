"""
Pipeline — Open Data Challenge · Défi 01 (sujet libre)
« L'État au bout du chemin » : indice d'accès aux services publics de base, préfecture par préfecture,
confronté au ciblage du Projet COSO.

Toutes les sources proviennent de opendata.gouv.tg (voir data/raw/SOURCES.md).
Lancer : python pipeline/build_data.py   (depuis app/)
"""
from __future__ import annotations

import csv
import json
import math
import re
import sys
import unicodedata
from pathlib import Path

import pandas as pd
from shapely.geometry import mapping, shape
from shapely.ops import unary_union

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
csv.field_size_limit(10 ** 9)

ROOT = Path(__file__).resolve().parents[1]
RAW, GEO, OUT = ROOT / "data" / "raw", ROOT / "data" / "geo", ROOT / "data" / "processed"
OUT.mkdir(parents=True, exist_ok=True)

GRAND_LOME = {"GOLFE", "AGOE-NYIVE"}
REGIONS_SOURCE = {"SAVANES", "KARA", "CENTRALE", "PLATEAUX", "MARITIME"}
REGION_ORDER = ["Grand Lomé", "Maritime", "Plateaux", "Centrale", "Kara", "Savanes"]


def norm(s) -> str:
    s = unicodedata.normalize("NFKD", str(s)).encode("ascii", "ignore").decode()
    return re.sub(r"\s+", " ", s.upper().strip())


def parse_point(wkt: str):
    try:
        lon, lat = str(wkt).strip()[len("POINT ("):-1].split()
        return float(lon), float(lat)
    except Exception:
        return None, None


def haversine(a, b) -> float:
    R = 6371.0088
    (x1, y1), (x2, y2) = a, b
    p1, p2 = math.radians(y1), math.radians(y2)
    h = math.sin((p2 - p1) / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(math.radians(x2 - x1) / 2) ** 2
    return 2 * R * math.asin(math.sqrt(h))


def line_km(wkt: str) -> float:
    tot = 0.0
    for part in re.findall(r"\(([-0-9.,\s]+)\)", str(wkt)):
        pts = [tuple(map(float, c.split())) for c in part.split(",") if c.strip()]
        tot += sum(haversine(pts[i], pts[i + 1]) for i in range(len(pts) - 1))
    return tot


def load_points(fname: str) -> pd.DataFrame:
    d = pd.read_csv(RAW / fname, low_memory=False)
    for c in [c for c in d.columns if c.endswith("_nom_bdd") or c.startswith("nom_")]:
        d[c] = d[c].astype(str).str.strip()
    d["prefecture_key"] = d["prefecture_nom_bdd"].map(norm)
    if "geometry" in d.columns:
        d[["lon", "lat"]] = d["geometry"].apply(lambda w: pd.Series(parse_point(w)))
    return d


# ============================================================ 1. référentiel territorial
sources = {k: load_points(f) for k, f in {
    "ceet": "agences_ceet.csv", "tde": "agences_tde.csv", "pea": "eau_pea.csv", "pmh": "eau_pmh.csv",
    "finance": "etablissements_finance.csv", "mm": "agents_mobile_money.csv",
    "auto": "auto_ecoles.csv", "routes": "routes_classees.csv"}.items()}

LIB_PREF, PREF_REGION = {}, {}
for d in sources.values():
    for p, r in zip(d["prefecture_nom_bdd"], d["region_nom_bdd"]):
        LIB_PREF.setdefault(norm(p), p)
        PREF_REGION.setdefault(norm(p), str(r).strip())
PREFS = set(LIB_PREF)


def region6(k: str) -> str:
    return "Grand Lomé" if k in GRAND_LOME else PREF_REGION.get(k, "?")


# ============================================================ 2. population 2022 et 2010
pop_raw = pd.read_csv(RAW / "population_rgph5_2022.csv")
pop_raw["key"] = pop_raw["découpage-administratif"].map(norm)
pop_raw["value"] = pop_raw["Value"].astype(int)
rows, cur = [], None
for key, val in zip(pop_raw["key"], pop_raw["value"]):
    if key == "TOGO":
        lvl = "pays"
    elif key in REGIONS_SOURCE:
        lvl, cur = "region", None
    elif cur and re.fullmatch(re.escape(cur) + r" \d+", key):
        lvl = "commune"
    elif key in PREFS and key != cur:
        lvl, cur = "prefecture", key
    else:
        lvl = "infra"
    rows.append((lvl, cur, key, val))
pop = pd.DataFrame(rows, columns=["niveau", "prefecture_key", "key", "population"])
pop22 = pop[pop.niveau == "prefecture"][["key", "population"]].rename(columns={"key": "prefecture_key", "population": "pop_2022"})
if "AVE" not in set(pop22.prefecture_key):
    ave = int(pop.loc[pop.key.str.fullmatch(r"AVE \d+"), "population"].sum())
    pop22 = pd.concat([pop22, pd.DataFrame([{"prefecture_key": "AVE", "pop_2022": ave}])], ignore_index=True)
POP_TOTAL = int(pop.loc[pop.niveau == "pays", "population"].iloc[0])
assert len(pop22) == 39, f"{len(pop22)} préfectures (39 attendues)"

p10 = pd.read_csv(RAW / "population_2010.csv")
p10["key"] = p10["indicateurs"].map(norm)
p10["value"] = pd.to_numeric(p10["Value"], errors="coerce")
POP_2010 = int(p10.loc[p10.key == "TOGO", "value"].iloc[0])
pop10 = (p10[p10.key.isin(PREFS)].groupby("key", as_index=False).value.max()
         .rename(columns={"key": "prefecture_key", "value": "pop_2010"}))

# ============================================================ 3. accès à l'électricité (découpage propre à la source)
el = pd.read_csv(RAW / "electricite_taux_prefecture.csv")
el.columns = [c.strip().lower() for c in el.columns]
el["zone_key"] = el["préfecture"].map(norm)
el["annee"] = pd.to_numeric(el["date"], errors="coerce").astype("Int64")
el["value"] = pd.to_numeric(el["value"], errors="coerce")
el["mesure"] = el["libellés"].map(lambda s: "taux_acces" if "Taux" in str(s) else "abonnes_bt")

# Le fichier d'électricité n'utilise pas les 39 préfectures actuelles : sept zones en regroupent deux.
ZONE_TO_PREFS = {
    "LOME COMMUNE + GOLFE": ["GOLFE"], "AGOENYIVE": ["AGOE-NYIVE"],
    "HAHO + MOYEN MONO": ["HAHO", "MOYEN-MONO"], "OGOU + ANIE": ["OGOU", "ANIE"],
    "LACS + BAS-MONO": ["LACS", "BAS-MONO"], "OTI + OTI SUD": ["OTI", "OTI-SUD"],
    "KPENDJAL + KPENDJAL OUEST": ["KPENDJAL", "KPENDJAL-OUEST"],
    "SOTOUBOUA + PLAINE DE MO": ["SOTOUBOUA", "MO"], "EST MONO": ["EST-MONO"], "AVE": ["AVE"],
}
EXCLUDE = {"ENSEMBLE DU PAYS", "LOME", "REGION MARITIME", "REGION DES PLATEAUX",
           "REGION CENTRALE", "REGION DE LA KARA", "REGION DES SAVANES"}
zones = sorted(set(el.zone_key) - EXCLUDE)
zone_prefs = {z: ZONE_TO_PREFS.get(z, [z] if z in PREFS else []) for z in zones}
missing = [z for z, v in zone_prefs.items() if not v]
assert not missing, f"zones électricité non rattachées : {missing}"

elz = (el[~el.zone_key.isin(EXCLUDE)]
       .pivot_table(index=["zone_key", "annee"], columns="mesure", values="value").reset_index())
elz["libelle"] = elz.zone_key.map(lambda z: " + ".join(LIB_PREF.get(p, p) for p in zone_prefs[z]))
elz["region"] = elz.zone_key.map(lambda z: region6(zone_prefs[z][0]))
elz["nb_prefectures"] = elz.zone_key.map(lambda z: len(zone_prefs[z]))
elz.to_csv(OUT / "electricite_zones.csv", index=False)
el_nat = el[el.zone_key == "ENSEMBLE DU PAYS"].pivot_table(index="annee", columns="mesure", values="value").reset_index()
el_nat.to_csv(OUT / "electricite_national.csv", index=False)
AN_EL = int(elz.annee.max())
taux_by_pref = {p: float(r.taux_acces) for r in elz[elz.annee == AN_EL].itertuples() for p in zone_prefs[r.zone_key]}
zone_by_pref = {p: r.libelle for r in elz[elz.annee == AN_EL].itertuples() for p in zone_prefs[r.zone_key]}

# ============================================================ 4. points de service géolocalisés
def statut_actif(s) -> bool:
    return "Utilise" in str(s) or "Utilisé" in str(s)


pts = []
for key, lib, cat in [("ceet", "Agence CEET", "Électricité"), ("tde", "Agence TdE", "Eau"),
                      ("pea", "Poste d'eau autonome", "Eau"), ("pmh", "Pompe à motricité humaine", "Eau"),
                      ("finance", "Établissement financier", "Services financiers"),
                      ("mm", "Agent mobile money", "Services financiers"),
                      ("auto", "Auto-école", "Mobilité")]:
    d = sources[key]
    sub = pd.DataFrame({
        "categorie": cat, "type": lib,
        "region": d["prefecture_key"].map(region6),
        "prefecture": d["prefecture_key"].map(LIB_PREF),
        "prefecture_key": d["prefecture_key"],
        "commune": d.get("commune_nom_bdd", pd.Series([""] * len(d))),
        "canton": d.get("canton_nom_bdd", pd.Series([""] * len(d))),
        "localite": d.get("nom_localite", pd.Series([""] * len(d))),
        "lon": d.get("lon"), "lat": d.get("lat"),
    })
    if "activite_statut" in d.columns:
        sub["actif"] = d["activite_statut"].map(statut_actif)
    else:
        sub["actif"] = True
    pts.append(sub)
points = pd.concat(pts, ignore_index=True)
points = points[points.prefecture_key.isin(PREFS)]
points.to_csv(OUT / "points_services.csv", index=False)

# routes : longueur par préfecture
ro = sources["routes"].copy()
ro["km"] = ro["geometry"].map(line_km)
km_pref = ro.groupby("prefecture_key").km.sum()
km_rev = ro[ro["route_recouvrement"].isin(["Bitume", "Beton", "Pavé", "Gravier amenagé"])].groupby("prefecture_key").km.sum()

# ============================================================ 5. table PRÉFECTURES et indice d'accès
pref = pd.DataFrame({"prefecture_key": sorted(PREFS)})
pref["prefecture"] = pref.prefecture_key.map(LIB_PREF)
pref["region"] = pref.prefecture_key.map(region6)
pref = pref.merge(pop22, on="prefecture_key", how="left").merge(pop10, on="prefecture_key", how="left")
pref["croissance_pct"] = ((pref.pop_2022 / pref.pop_2010 - 1) * 100).round(1)

act = points[points.actif]
for lib, col in [("Agence CEET", "ceet"), ("Agence TdE", "tde"), ("Poste d'eau autonome", "pea"),
                 ("Pompe à motricité humaine", "pmh"), ("Établissement financier", "finance"),
                 ("Agent mobile money", "mobile_money"), ("Auto-école", "auto_ecoles")]:
    pref[col] = pref.prefecture_key.map(act[act.type == lib].groupby("prefecture_key").size()).fillna(0).astype(int)

pref["km_routes"] = pref.prefecture_key.map(km_pref).fillna(0).round(1)
pref["km_revetues"] = pref.prefecture_key.map(km_rev).fillna(0).round(1)
pref["taux_electricite"] = pref.prefecture_key.map(taux_by_pref)
pref["zone_electrique"] = pref.prefecture_key.map(zone_by_pref)
pref["zone_partagee"] = pref.prefecture_key.map(lambda k: len(zone_prefs.get(
    next((z for z, v in zone_prefs.items() if k in v), ""), [])) > 1)

# --- quatre dimensions d'accès, rapportées à la population
pref["points_eau"] = pref.pea + pref.pmh + pref.tde
pref["eau_10k"] = (pref.points_eau / pref.pop_2022 * 10000).round(2)
pref["finance_10k"] = ((pref.finance + pref.mobile_money) / pref.pop_2022 * 10000).round(2)
pref["m_route_hab"] = (pref.km_routes * 1000 / pref.pop_2022).round(2)
pref["part_revetue"] = (pref.km_revetues / pref.km_routes.where(pref.km_routes > 0) * 100).round(1)

DIMS = {"Eau": "eau_10k", "Électricité": "taux_electricite",
        "Services financiers": "finance_10k", "Mobilité": "m_route_hab"}


def score100(s: pd.Series) -> pd.Series:
    """0 = le moins bien servi des 39, 100 = le mieux servi."""
    s = s.astype(float)
    lo, hi = s.min(), s.max()
    return ((s - lo) / (hi - lo) * 100).round(1) if hi > lo else s * 0


for lab, col in DIMS.items():
    pref[f"score_{col}"] = score100(pref[col].fillna(pref[col].min()))
pref["indice_acces"] = pref[[f"score_{c}" for c in DIMS.values()]].mean(axis=1).round(1)
pref["rang_acces"] = pref.indice_acces.rank(ascending=False, method="min").astype(int)
pref["part_population"] = (pref.pop_2022 / POP_TOTAL * 100).round(2)

MAP_MERGE = {"AGOE-NYIVE": "GOLFE", "KPENDJAL-OUEST": "KPENDJAL", "OTI-SUD": "OTI"}
pref["map_key"] = pref.prefecture_key.map(lambda k: MAP_MERGE.get(k, k))

# ============================================================ 6. Projet COSO
coso = pd.read_csv(RAW / "coso_inventaire.csv", low_memory=False)
coso["sector"] = coso["sector"].astype(str).str.replace("–", "-", regex=False)
h = coso["hierarchy"].astype(str).str.split(">")
coso["coso_prefecture"] = h.map(lambda x: x[-2].strip() if len(x) >= 2 else None)
coso["coso_region"] = h.map(lambda x: x[-1].strip() if len(x) >= 1 else None)
COSO_TO_PREF = {"TANDJOUARE": "TANDJOARE", "KPENDJAL OUEST": "KPENDJAL-OUEST", "OTI SUD": "OTI-SUD"}
coso["prefecture_key"] = coso.coso_prefecture.map(lambda p: COSO_TO_PREF.get(norm(p), norm(p)) if p else None)
coso["montant"] = pd.to_numeric(coso["total_contract_amount_paid"], errors="coerce").fillna(
    pd.to_numeric(coso["contract_amount_work_companies"], errors="coerce")).fillna(0)
coso["beneficiaires"] = pd.to_numeric(coso["estimated_number_of_beneficiaries"], errors="coerce").fillna(
    pd.to_numeric(coso["population"], errors="coerce")).fillna(0)
coso["acheve"] = coso["status"].astype(str).str.contains("100.0%|Achev", regex=True)
coso[["lat", "lon"]] = coso[["latitude", "longitude"]].apply(pd.to_numeric, errors="coerce")
coso.loc[(coso.lat.abs() < 0.001) | (coso.lon.abs() < 0.0001), ["lat", "lon"]] = None
coso_out = coso[["id", "title", "type", "sector", "works_type", "status", "acheve", "montant", "beneficiaires",
                 "location_name", "canton", "coso_prefecture", "coso_region", "prefecture_key", "lat", "lon"]]
coso_out = coso_out.rename(columns={"title": "intitule", "sector": "secteur", "works_type": "nature",
                                    "location_name": "localite", "coso_prefecture": "prefecture_source"})
coso_out.to_csv(OUT / "coso_projets.csv", index=False)

g = coso.groupby("prefecture_key")
pref["coso_projets"] = pref.prefecture_key.map(g.size()).fillna(0).astype(int)
pref["coso_montant"] = pref.prefecture_key.map(g.montant.sum()).fillna(0).round(0)
pref["coso_beneficiaires"] = pref.prefecture_key.map(g.beneficiaires.sum()).fillna(0).astype(int)
pref["coso_couverte"] = pref.coso_projets > 0
pref["coso_fcfa_hab"] = (pref.coso_montant / pref.pop_2022).round(0)

pref = pref.sort_values(["region", "prefecture"]).reset_index(drop=True)
pref.to_csv(OUT / "prefectures.csv", index=False)

# ============================================================ 7. régions, séries nationales
reg = pref.groupby("region", as_index=False).agg(
    pop_2022=("pop_2022", "sum"), pop_2010=("pop_2010", "sum"), prefectures=("prefecture", "count"),
    points_eau=("points_eau", "sum"), finance=("finance", "sum"), mobile_money=("mobile_money", "sum"),
    ceet=("ceet", "sum"), tde=("tde", "sum"), km_routes=("km_routes", "sum"),
    auto_ecoles=("auto_ecoles", "sum"), indice_acces=("indice_acces", "mean"),
    coso_projets=("coso_projets", "sum"), coso_montant=("coso_montant", "sum"))
reg["eau_10k"] = (reg.points_eau / reg.pop_2022 * 10000).round(2)
reg["finance_10k"] = ((reg.finance + reg.mobile_money) / reg.pop_2022 * 10000).round(2)
reg["m_route_hab"] = (reg.km_routes * 1000 / reg.pop_2022).round(2)
reg["indice_acces"] = reg.indice_acces.round(1)
reg["part_population"] = (reg.pop_2022 / POP_TOTAL * 100).round(1)
reg["croissance_pct"] = ((reg.pop_2022 / reg.pop_2010 - 1) * 100).round(1)
reg["region"] = pd.Categorical(reg.region, REGION_ORDER, ordered=True)
reg = reg.sort_values("region")
reg.to_csv(OUT / "regions.csv", index=False)


def load_obs(f: str, dims: tuple[str, ...] = ()) -> pd.DataFrame:
    """Lit un fichier d'observations INSEED (indicateur / région / Unit / Date / Value)."""
    d = pd.read_csv(RAW / f)
    d.columns = [c.strip().lower() for c in d.columns]
    ind = "indicateur" if "indicateur" in d.columns else "indicateurs"
    d = d.rename(columns={ind: "indicateur"})
    d["value"] = pd.to_numeric(d["value"], errors="coerce")
    d["annee"] = pd.to_numeric(d["date"], errors="coerce").astype("Int64")
    # /!\ ne jamais oublier une dimension de ventilation : sans la colonne sexe,
    # la série scolarisation présente 3 lignes identiques par région et par année.
    keep = ["indicateur", "annee", "value"] + [c for c in dims if c in d.columns]
    return d[keep].dropna(subset=["annee", "value"])


load_obs("sante_formations.csv", ("région",)).to_csv(OUT / "sante_formations.csv", index=False)
load_obs("sante_densite.csv", ("région",)).to_csv(OUT / "sante_densite.csv", index=False)
load_obs("scolarisation_primaire.csv", ("région", "sexe")).to_csv(OUT / "scolarisation.csv", index=False)
load_obs("pauvrete.csv").to_csv(OUT / "pauvrete.csv", index=False)

# ============================================================ 8. contours
adm2 = json.load(open(GEO / "togo_adm2.geojson", encoding="utf-8"))
RENAME = {"TANDJOUARE": "TANDJOARE", "PLAINE DE MO": "MO", "LOME COMMUNE": "GOLFE"}
groups: dict[str, list] = {}
for f in adm2["features"]:
    k = RENAME.get(norm(f["properties"]["shapeName"]), norm(f["properties"]["shapeName"]))
    groups.setdefault(k, []).append(shape(f["geometry"]))
LIB_MAP = {"GOLFE": "Golfe + Agoè-Nyivé (Grand Lomé)", "KPENDJAL": "Kpendjal + Kpendjal-Ouest", "OTI": "Oti + Oti-Sud"}
json.dump({"type": "FeatureCollection", "features": [
    {"type": "Feature", "id": k, "properties": {"map_key": k, "libelle": LIB_MAP.get(k, LIB_PREF.get(k, k.title()))},
     "geometry": mapping(unary_union(v).simplify(0.002, preserve_topology=True))} for k, v in groups.items()]},
    open(OUT / "prefectures.geojson", "w", encoding="utf-8"))
assert not (set(pref.map_key) - set(groups)), f"contours manquants : {set(pref.map_key) - set(groups)}"

adm1 = json.load(open(GEO / "togo_adm1.geojson", encoding="utf-8"))
rg = {norm(f["properties"]["shapeName"]).replace(" REGION", ""): shape(f["geometry"]) for f in adm1["features"]}
gl = unary_union(groups["GOLFE"])
rg["MARITIME"] = rg["MARITIME"].difference(gl)
rg["GRAND LOME"] = gl
LIB_REG = {"SAVANES": "Savanes", "KARA": "Kara", "CENTRALE": "Centrale", "PLATEAUX": "Plateaux",
           "MARITIME": "Maritime", "GRAND LOME": "Grand Lomé"}
json.dump({"type": "FeatureCollection", "features": [
    {"type": "Feature", "id": LIB_REG[k], "properties": {"region": LIB_REG[k]},
     "geometry": mapping(g.simplify(0.002, preserve_topology=True))} for k, g in rg.items()]},
    open(OUT / "regions.geojson", "w", encoding="utf-8"))

# ============================================================ 9. indicateurs nationaux
best, worst = pref.loc[pref.indice_acces.idxmax()], pref.loc[pref.indice_acces.idxmin()]
coso_pref = pref[pref.coso_couverte]
non_coso = pref[~pref.coso_couverte]
# 10 préfectures les moins bien servies : combien sont couvertes par COSO ?
bottom10 = pref.nsmallest(10, "indice_acces")
kpi = {
    "pop_2022": POP_TOTAL, "pop_2010": POP_2010,
    "croissance_pct": round((POP_TOTAL / POP_2010 - 1) * 100, 1),
    "prefectures": int(len(pref)),
    "points_services": int(len(points)), "points_actifs": int(len(act)),
    "points_eau": int(pref.points_eau.sum()), "pmh": int(pref.pmh.sum()), "pea": int(pref.pea.sum()),
    "finance": int(pref.finance.sum()), "mobile_money": int(pref.mobile_money.sum()),
    "ceet": int(pref.ceet.sum()), "tde": int(pref.tde.sum()), "auto_ecoles": int(pref.auto_ecoles.sum()),
    "km_routes": round(float(pref.km_routes.sum())),
    "taux_elec_national": round(float(el_nat[el_nat.annee == AN_EL].taux_acces.iloc[0]), 1),
    "annee_elec": AN_EL,
    "indice_max": float(best.indice_acces), "indice_max_pref": str(best.prefecture),
    "indice_min": float(worst.indice_acces), "indice_min_pref": str(worst.prefecture),
    "ecart_indice": round(float(best.indice_acces - worst.indice_acces), 1),
    "eau_max": float(pref.eau_10k.max()), "eau_min": float(pref.eau_10k.min()),
    "eau_ratio": round(float(pref.eau_10k.max() / max(pref.eau_10k.min(), 0.01)), 1),
    "coso_projets": int(pref.coso_projets.sum()), "coso_prefectures": int(pref.coso_couverte.sum()),
    "coso_montant": float(pref.coso_montant.sum()),
    "coso_pop_couverte": int(coso_pref.pop_2022.sum()),
    "coso_part_pop": round(float(coso_pref.pop_2022.sum() / POP_TOTAL * 100), 1),
    "coso_indice_moyen": round(float(coso_pref.indice_acces.mean()), 1),
    "non_coso_indice_moyen": round(float(non_coso.indice_acces.mean()), 1),
    "bottom10_dans_coso": int(bottom10.coso_couverte.sum()),
    "bottom10_hors_coso": ", ".join(bottom10[~bottom10.coso_couverte].prefecture.tolist()),
    "zones_electriques_regroupees": int(sum(1 for v in zone_prefs.values() if len(v) > 1)),
}
json.dump(kpi, open(OUT / "kpi_national.json", "w", encoding="utf-8"), indent=2, ensure_ascii=False)

print("=== Pipeline OK ===")
print(f"population        : {POP_2010:,} (2010) → {POP_TOTAL:,} (2022)  +{kpi['croissance_pct']} %")
print(f"points de service : {len(points):,} dont {len(act):,} actifs "
      f"({kpi['points_eau']:,} eau · {kpi['finance'] + kpi['mobile_money']:,} financiers · {kpi['auto_ecoles']} auto-écoles)")
print(f"réseau routier    : {kpi['km_routes']:,} km")
print(f"indice d'accès    : {kpi['indice_min_pref']} {kpi['indice_min']} → {kpi['indice_max_pref']} {kpi['indice_max']}")
print(f"COSO              : {kpi['coso_projets']} projets, {kpi['coso_prefectures']} préfectures, "
      f"{kpi['coso_montant']/1e9:.1f} Md FCFA, {kpi['coso_part_pop']} % de la population")
print(f"  indice moyen    : {kpi['coso_indice_moyen']} (zone COSO) contre {kpi['non_coso_indice_moyen']} (hors COSO)")
print(f"  parmi les 10 moins bien servies : {kpi['bottom10_dans_coso']}/10 couvertes par COSO")
print(f"  les non couvertes : {kpi['bottom10_hors_coso']}")
print()
print(pref.sort_values("indice_acces")[["prefecture", "region", "pop_2022", "indice_acces", "rang_acces",
                                        "eau_10k", "taux_electricite", "finance_10k", "m_route_hab",
                                        "coso_projets"]].head(12).to_string(index=False))
