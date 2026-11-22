"""Les 36 880 points de service sur la carte."""
import plotly.express as px
import streamlit as st

from lib import data as D
from lib import ui

k = D.kpi()
flt = D.sidebar_filters()
pts_all = D.points()
pts = D.f(pts_all, flt)

ui.header("Les 36 880 points de service",
          "Chaque point d'eau, chaque agence, chaque auto-école et chaque agent de mobile money "
          "publié en données ouvertes, replacé sur la carte du Togo. C'est la matière première de "
          "l'indice d'accès — et sa limite se voit à l'œil nu.")

CATS = ["Eau", "Électricité", "Services financiers", "Mobilité"]
CAT_COLORS = {"Eau": ui.DIM_COLORS["Eau"], "Électricité": ui.DIM_COLORS["Électricité"],
              "Services financiers": ui.DIM_COLORS["Services financiers"],
              "Mobilité": ui.DIM_COLORS["Mobilité"]}

ui.section("01", "Ce qu'il y a dans la base")
ui.kpis([
    dict(label="Points géolocalisés", value=ui.fmt(k["points_services"]),
         sub=f"dont {ui.fmt(k['points_actifs'])} sans signalement de fermeture",
         source="7 jeux ouverts croisés, opendata.gouv.tg"),
    dict(label="Points d'eau", value=ui.fmt(k["points_eau"]), tone="slate",
         sub=f"{ui.fmt(k['pmh'])} pompes manuelles et {ui.fmt(k['pea'])} postes autonomes",
         source="Inventaires PMH et PEA, Min. de l'Eau"),
    dict(label="Points financiers", value=ui.fmt(k["mobile_money"] + k["finance"]),
         sub=f"{ui.fmt(k['mobile_money'])} agents mobile money, {k['finance']} établissements",
         source="Recensement MM + répertoire financier"),
    dict(label="Points fermés signalés", value=f"{k['points_services'] - k['points_actifs']}",
         tone="red", sub="78 établissements financiers, 12 agences TdE, 7 agences CEET — "
                         "les inventaires de points d'eau, eux, ne publient aucun état de service",
         source="champ « statut » des annuaires d'agences"),
])

# ------------------------------------------------------------------ 02
ui.section("02", "La carte", "Filtrez par catégorie, par type et par état de service.")
c1, c2, c3 = st.columns([1.5, 1.5, 1])
cats = c1.multiselect("Catégories", CATS, default=CATS, placeholder="Toutes")
cats = cats or CATS
sub = pts[pts.categorie.isin(cats)]
types = sorted(sub.type.unique())
tsel = c2.multiselect("Types", types, default=[], placeholder=f"Les {len(types)} types")
if tsel:
    sub = sub[sub.type.isin(tsel)]
etat = c3.selectbox("État", ["Tous", "En service", "Hors service"])
if etat == "En service":
    sub = sub[sub.actif]
elif etat == "Hors service":
    sub = sub[~sub.actif]

st.caption(f"{ui.fmt(len(sub))} points affichés sur {ui.fmt(len(pts_all))}")

# échantillonnage d'affichage : la carte reste lisible et le navigateur suit
MAXP = 14000
shown, ech = sub, False
if len(sub) > MAXP:
    shown = sub.sample(MAXP, random_state=7)
    ech = True

fig = px.scatter_map(
    shown, lat="lat", lon="lon", color="categorie", color_discrete_map=CAT_COLORS,
    hover_name="type", zoom=6.8, center=dict(lat=8.72, lon=0.98), map_style="carto-positron",
    hover_data={"prefecture": True, "localite": True, "actif": True, "lat": False, "lon": False},
    labels={"categorie": ""})
fig.update_traces(marker=dict(size=5, opacity=0.68))
fig.update_layout(margin=dict(l=0, r=0, t=0, b=0),
                  legend=dict(orientation="h", y=1.02, x=0, bgcolor="rgba(255,255,255,.8)"))
ui.chart(fig, h=620)
ui.source("inventaires PEA/PMH, agences CEET et TdE, établissements financiers, agents mobile money, "
          "auto-écoles — opendata.gouv.tg")
if ech:
    st.caption(f"Affichage échantillonné à {ui.fmt(MAXP)} points sur {ui.fmt(len(sub))} pour rester "
               f"fluide. Tous les calculs de l'indice portent sur la totalité des points.")

# ------------------------------------------------------------------ 03
ui.section("03", "Répartition par catégorie et par région")
c1, c2 = st.columns([1.2, 1])
with c1:
    t = (pts.groupby(["region", "categorie"], observed=True).size().reset_index(name="n"))
    fig = px.bar(t, x="region", y="n", color="categorie", color_discrete_map=CAT_COLORS,
                 labels={"n": "points de service", "region": "", "categorie": ""})
    fig.update_layout(xaxis=dict(categoryorder="array", categoryarray=D.REGION_ORDER))
    ui.chart(fig, h=380)
    ui.source("calcul de l'auteur")
with c2:
    t2 = pts.groupby("type", observed=True).size().reset_index(name="n").nlargest(12, "n")
    fig = px.bar(t2.sort_values("n"), y="type", x="n", orientation="h",
                 labels={"n": "points", "type": ""},
                 color_discrete_sequence=[ui.C["green"]])
    ui.chart(fig, h=380)
    ui.source("calcul de l'auteur")

ui.note(
    "<b>La carte dit deux choses à la fois.</b> La première est attendue : la densité suit la "
    "population, et le Grand Lomé est une tache. La seconde l'est moins — regardez les vides. "
    "Le centre du pays, entre Sotouboua et Tchamba, et le massif de Mô ne portent presque aucun "
    "point, toutes catégories confondues. Ces vides ne sont pas des zones inhabitées : ce sont "
    "des zones où aucun des sept jeux publiés ne recense quoi que ce soit. C'est précisément là "
    "que l'indice d'accès est le plus bas, et c'est là qu'une politique de donnée ouverte a le "
    "plus à gagner.", "gold")

with st.expander("Voir le tableau détaillé des points filtrés"):
    st.dataframe(
        sub[["categorie", "type", "region", "prefecture", "commune", "localite", "actif"]]
        .rename(columns={"categorie": "Catégorie", "type": "Type", "region": "Région",
                         "prefecture": "Préfecture", "commune": "Commune",
                         "localite": "Localité", "actif": "En service"})
        .head(2000), hide_index=True, use_container_width=True, height=420)
    st.caption("Les 2 000 premières lignes du filtre courant.")
