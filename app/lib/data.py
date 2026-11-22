"""Chargement des données et filtres globaux."""
from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
PROC = ROOT / "data" / "processed"

REGION_ORDER = ["Grand Lomé", "Maritime", "Plateaux", "Centrale", "Kara", "Savanes"]
DIMS = {
    "Eau": ("eau_10k", "score_eau_10k", "points d'eau / 10 000 hab."),
    "Électricité": ("taux_electricite", "score_taux_electricite", "taux d'accès BT (%)"),
    "Services financiers": ("finance_10k", "score_finance_10k", "points financiers / 10 000 hab."),
    "Mobilité": ("m_route_hab", "score_m_route_hab", "mètres de route classée / hab."),
}
# harmonisation des libellés régionaux des séries sanitaires et scolaires
REG_FIX = {"Lomé Commune": "Grand Lomé", "Lomé-Golfe": "Grand Lomé",
           "TOGO": "Togo", "Togo": "Togo"}


@st.cache_data(show_spinner=False)
def prefectures() -> pd.DataFrame:
    d = pd.read_csv(PROC / "prefectures.csv")
    d["region"] = pd.Categorical(d["region"], REGION_ORDER, ordered=True)
    return d


@st.cache_data(show_spinner=False)
def regions() -> pd.DataFrame:
    d = pd.read_csv(PROC / "regions.csv")
    d["region"] = pd.Categorical(d["region"], REGION_ORDER, ordered=True)
    return d.sort_values("region")


@st.cache_data(show_spinner=False)
def points() -> pd.DataFrame:
    return pd.read_csv(PROC / "points_services.csv")


@st.cache_data(show_spinner=False)
def coso() -> pd.DataFrame:
    return pd.read_csv(PROC / "coso_projets.csv")


@st.cache_data(show_spinner=False)
def elec_zones() -> pd.DataFrame:
    return pd.read_csv(PROC / "electricite_zones.csv")


@st.cache_data(show_spinner=False)
def elec_national() -> pd.DataFrame:
    return pd.read_csv(PROC / "electricite_national.csv")


@st.cache_data(show_spinner=False)
def serie(nom: str) -> pd.DataFrame:
    d = pd.read_csv(PROC / f"{nom}.csv")
    if "région" in d.columns:
        d = d.rename(columns={"région": "region"})
        d["region"] = d["region"].replace(REG_FIX)
    return d


@st.cache_data(show_spinner=False)
def pauvrete() -> pd.DataFrame:
    return pd.read_csv(PROC / "pauvrete.csv")


@st.cache_data(show_spinner=False)
def geo(nom: str) -> dict:
    return json.loads((PROC / f"{nom}.geojson").read_text(encoding="utf-8"))


@st.cache_data(show_spinner=False)
def kpi() -> dict:
    return json.loads((PROC / "kpi_national.json").read_text(encoding="utf-8"))


# ------------------------------------------------------------------ filtres
def sidebar_filters() -> dict:
    """Filtres persistants, partagés par toutes les pages."""
    pref = prefectures()
    st.sidebar.markdown("<div class='sb-grp'>Filtres</div>", unsafe_allow_html=True)

    regs = st.sidebar.multiselect(
        "Régions", REGION_ORDER, default=st.session_state.get("f_reg", REGION_ORDER),
        key="f_reg", placeholder="Toutes les régions")
    regs = regs or REGION_ORDER

    dispo = pref.loc[pref["region"].isin(regs), "prefecture"].sort_values().tolist()
    sel = [p for p in st.session_state.get("f_pref", []) if p in dispo]
    st.session_state["f_pref"] = sel
    prefs = st.sidebar.multiselect("Préfectures", dispo, key="f_pref",
                                   placeholder=f"Les {len(dispo)} préfectures")
    prefs = prefs or dispo

    coso_only = st.sidebar.toggle("Zone COSO uniquement", value=st.session_state.get("f_coso", False),
                                  key="f_coso", help="Les 9 préfectures couvertes par le projet COSO (Nord)")
    if coso_only:
        couv = set(pref.loc[pref["coso_couverte"], "prefecture"])
        prefs = [p for p in prefs if p in couv] or sorted(couv)

    if st.sidebar.button("Réinitialiser", use_container_width=True):
        for k in ("f_reg", "f_pref", "f_coso"):
            st.session_state.pop(k, None)
        st.rerun()

    actif = len(prefs) < pref.shape[0]
    st.sidebar.caption(f"{len(prefs)} préfecture(s) · {len(regs)} région(s)"
                       + ("  —  filtre actif" if actif else ""))
    return {"regions": regs, "prefectures": prefs, "coso_only": coso_only, "actif": actif}


def f(df: pd.DataFrame, flt: dict, col: str = "prefecture") -> pd.DataFrame:
    return df[df[col].isin(flt["prefectures"])] if col in df.columns else df


def fr(df: pd.DataFrame, flt: dict) -> pd.DataFrame:
    return df[df["region"].isin(flt["regions"])] if "region" in df.columns else df


@st.cache_data(show_spinner=False)
def map_frame() -> pd.DataFrame:
    """Agrège les 39 préfectures sur les 36 contours disponibles (moyenne pondérée
    par la population) : Agoè-Nyivé est fondue dans Golfe, Kpendjal-Ouest dans
    Kpendjal, Oti-Sud dans Oti — les contours OSM de 2017 datent d'avant le
    découpage en 39 préfectures."""
    d = prefectures().copy()
    num = ["eau_10k", "taux_electricite", "finance_10k", "m_route_hab", "indice_acces"]
    for c in num:
        d[c + "_w"] = d[c] * d["pop_2022"]
    g = d.groupby("map_key", as_index=False).agg(
        pop_2022=("pop_2022", "sum"), prefectures=("prefecture", lambda s: " + ".join(sorted(s))),
        region=("region", "first"), coso_projets=("coso_projets", "sum"),
        coso_montant=("coso_montant", "sum"),
        **{c + "_w": (c + "_w", "sum") for c in num})
    for c in num:
        g[c] = (g[c + "_w"] / g["pop_2022"]).round(2)
    g["coso_couverte"] = g["coso_projets"] > 0
    g["indice_acces"] = g["indice_acces"].round(1)
    return g.drop(columns=[c + "_w" for c in num])
