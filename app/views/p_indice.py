"""L'indice d'accès — construction, carte, décomposition."""
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from lib import data as D
from lib import ui

k = D.kpi()
flt = D.sidebar_filters()
pref_all = D.prefectures()
pref = D.f(pref_all, flt)

ui.header("L'indice d'accès",
          "Quatre dimensions, une échelle commune. L'indice ne dit pas si un service est « bon » — "
          "il dit où une préfecture se situe par rapport aux 38 autres, sur ce que les données "
          "publiques permettent de mesurer.")

# ------------------------------------------------------------------ 01
ui.section("01", "Comment il est construit", "Trois étapes, aucune pondération cachée.")
c1, c2, c3 = st.columns(3)
c1.markdown(
    "<div class='reco'><span class='n'>1</span><span class='t'>Ramener à l'habitant</span>"
    "<p>Chaque dimension est rapportée à la population 2022 de la préfecture : points d'eau pour "
    "10 000 habitants, points financiers pour 10 000 habitants, mètres de route classée par "
    "habitant. L'électricité est déjà un taux.</p></div>", unsafe_allow_html=True)
c2.markdown(
    "<div class='reco'><span class='n'>2</span><span class='t'>Mettre sur la même échelle</span>"
    "<p>Chaque dimension est normalisée de 0 à 100 : 0 pour la préfecture la plus mal dotée des 39, "
    "100 pour la mieux dotée. L'indice est donc <b>relatif</b> : il compare le Togo à lui-même, pas "
    "à une norme internationale.</p></div>", unsafe_allow_html=True)
c3.markdown(
    "<div class='reco'><span class='n'>3</span><span class='t'>Moyenner à parts égales</span>"
    "<p>Les quatre scores sont moyennés sans pondération. Ce choix est discutable et il est "
    "<b>assumé</b> : toute pondération suppose une hiérarchie des besoins que les données ne "
    "permettent pas d'établir. Les quatre scores restent visibles séparément.</p></div>",
    unsafe_allow_html=True)

ui.kpis([
    dict(label="Mieux servie des 39", value=k["indice_max_pref"], tone="",
         sub=f"indice {k['indice_max']} — 70,8 points d'eau / 10 000 hab., 1,25 m de route / hab.",
         source="calcul de l'auteur"),
    dict(label="Moins bien servie des 39", value=k["indice_min_pref"], tone="red",
         sub=f"indice {k['indice_min']} — 3,7 % d'électricité, 0,15 m de route / hab.",
         source="calcul de l'auteur"),
    dict(label="Écart entre les deux", value=ui.fmt(k['ecart_indice'], 1, " pts"), tone="slate",
         sub="sur une échelle de 100 — l'écart interne au pays est plus large que la moitié de l'échelle",
         source="calcul de l'auteur"),
    dict(label="Dimensions mesurées", value="4", tone="gold",
         sub="eau, électricité, services financiers, mobilité — 8 jeux ouverts croisés",
         source="opendata.gouv.tg"),
])

# ------------------------------------------------------------------ 02
ui.section("02", "La carte de l'accès",
           "Les contours disponibles datent de 2017 : ils couvrent 36 entités, les 39 préfectures "
           "actuelles y sont regroupées par population (Agoè-Nyivé dans Golfe, Kpendjal-Ouest dans "
           "Kpendjal, Oti-Sud dans Oti).")

mf = D.map_frame()
gj = D.geo("prefectures")
choix = st.radio("Variable cartographiée", ["Indice d'accès"] + list(D.DIMS), horizontal=True,
                 label_visibility="collapsed")
col, lbl = ("indice_acces", "indice d'accès (0–100)") if choix == "Indice d'accès" else \
    (D.DIMS[choix][0], D.DIMS[choix][2])

m1, m2 = st.columns([1.15, 1])
with m1:
    fig = px.choropleth_map(
        mf, geojson=gj, locations="map_key", featureidkey="properties.map_key",
        color=col, color_continuous_scale=ui.SEQ if choix == "Indice d'accès" else ui.SEQ,
        map_style="carto-positron", zoom=6.75, center=dict(lat=8.72, lon=0.98),
        opacity=0.86, hover_name="prefectures",
        hover_data={"map_key": False, "region": True, "pop_2022": ":,.0f", col: ":.2f",
                    "coso_projets": True})
    fig.update_layout(margin=dict(l=0, r=0, t=0, b=0),
                      coloraxis_colorbar=dict(title=None, thickness=11, len=0.62, x=0.99,
                                              tickfont_size=10))
    ui.chart(fig, h=560)
    ui.source("contours geoBoundaries ADM2 (OpenStreetMap, 2017) · valeurs calculées par l'auteur")
with m2:
    st.markdown(f"<div style='height:.4rem'></div>", unsafe_allow_html=True)
    top = mf.nlargest(8, col)[["prefectures", "region", col]]
    bot = mf.nsmallest(8, col)[["prefectures", "region", col]]
    st.markdown(f"**Les 8 mieux dotées** — {lbl}")
    st.dataframe(top.rename(columns={"prefectures": "Préfecture(s)", "region": "Région", col: lbl}),
                 hide_index=True, use_container_width=True, height=305)
    st.markdown(f"**Les 8 moins dotées** — {lbl}")
    st.dataframe(bot.rename(columns={"prefectures": "Préfecture(s)", "region": "Région", col: lbl}),
                 hide_index=True, use_container_width=True, height=305)

# ------------------------------------------------------------------ 03
ui.section("03", "Décomposer l'indice",
           "Un indice moyen cache des profils très différents : certaines préfectures sont "
           "faibles partout, d'autres n'ont qu'un seul point noir.")

sc = {n: v[1] for n, v in D.DIMS.items()}
d = pref.sort_values("indice_acces", ascending=False)
fig = go.Figure()
for dim, col_s in sc.items():
    fig.add_trace(go.Bar(x=d.prefecture, y=d[col_s] / 4, name=dim,
                         marker_color=ui.DIM_COLORS[dim],
                         customdata=d[[col_s]],
                         hovertemplate=f"<b>%{{x}}</b><br>{dim} : score %{{customdata[0]:.1f}}/100"
                                       "<extra></extra>"))
fig.update_layout(barmode="stack", xaxis_tickangle=-55,
                  yaxis_title="contribution à l'indice (pts)", xaxis_title=None,
                  xaxis=dict(tickfont_size=10))
ui.chart(fig, h=430)
ui.source("calcul de l'auteur — chaque barre vaut un quart du score de la dimension")

faible = pref_all.assign(
    pire=pref_all[[v[1] for v in D.DIMS.values()]].idxmin(axis=1).map(
        {v[1]: n for n, v in D.DIMS.items()}))
rep = faible.pire.value_counts()
ui.note(
    "<b>Le point noir n'est pas le même partout.</b> Pour "
    + " · ".join(f"<b>{n}</b> : {v} préfectures" for n, v in rep.items())
    + ". Une politique nationale uniforme traiterait donc la bonne dimension pour une minorité "
      "de territoires seulement : les scores par dimension, ci-dessus, sont le bon niveau de lecture.")

# ------------------------------------------------------------------ 04
viz = st.toggle("Afficher le profil détaillé d'une préfecture", value=True)
if viz:
    ui.section("04", "Profil d'une préfecture")
    choix_p = st.selectbox("Préfecture", sorted(pref.prefecture), label_visibility="collapsed")
    r = pref_all[pref_all.prefecture == choix_p].iloc[0]
    g1, g2 = st.columns([1, 1.25])
    with g1:
        vals = [r[v[1]] for v in D.DIMS.values()]
        fg = go.Figure(go.Scatterpolar(
            r=vals + [vals[0]], theta=list(D.DIMS) + [list(D.DIMS)[0]], fill="toself",
            line=dict(color=ui.C["green"], width=2.2), fillcolor="rgba(14,124,86,.18)",
            name=choix_p, hovertemplate="%{theta} : score %{r:.1f}/100<extra></extra>"))
        moy = [pref_all[v[1]].mean() for v in D.DIMS.values()]
        fg.add_trace(go.Scatterpolar(
            r=moy + [moy[0]], theta=list(D.DIMS) + [list(D.DIMS)[0]], fill="toself",
            line=dict(color=ui.C["gold"], width=1.4, dash="dot"), fillcolor="rgba(201,150,43,.08)",
            name="moyenne des 39", hovertemplate="moyenne %{theta} : %{r:.1f}<extra></extra>"))
        fg.update_layout(polar=dict(radialaxis=dict(range=[0, 100], tickfont_size=9,
                                                    gridcolor=ui.C["line"]),
                                    angularaxis=dict(tickfont_size=11)))
        ui.chart(fg, h=370)
    with g2:
        ui.kpis([dict(label="Indice d'accès", value=ui.fmt(r.indice_acces, 1),
                      sub=f"rang {int(r.rang_acces)} sur 39 · région {r.region}",
                      tone="red" if r.rang_acces > 29 else "",
                      source="calcul de l'auteur"),
                 dict(label="Population 2022", value=ui.fmt(r.pop_2022),
                      sub=f"{r.croissance_pct:+.1f} % depuis 2010", tone="slate",
                      source="RGPH-5 2022, INSEED")])
        st.markdown("<div style='height:.7rem'></div>", unsafe_allow_html=True)
        det = pd.DataFrame({
            "Dimension": list(D.DIMS),
            "Valeur brute": [f"{ui.fmt(r[v[0]], 2)} {v[2].split(' / ')[0] if '/' in v[2] else v[2]}"
                             for v in D.DIMS.values()],
            "Score /100": [ui.fmt(r[v[1]], 1) for v in D.DIMS.values()],
            "Rang /39": [int((pref_all[v[0]] > r[v[0]]).sum() + 1) for v in D.DIMS.values()],
        })
        st.dataframe(det, hide_index=True, use_container_width=True)
        if r.coso_couverte:
            ui.note(f"Cette préfecture est couverte par COSO : <b>{int(r.coso_projets)} ouvrages</b> "
                    f"pour {ui.fmt(r.coso_montant / 1e6, 1)} millions F CFA, soit "
                    f"{ui.fmt(r.coso_fcfa_hab)} F par habitant.", "gold")
        else:
            ui.note("Cette préfecture n'est <b>pas couverte</b> par le programme COSO : aucun des "
                    "813 ouvrages inventoriés ne s'y trouve.", "red")
