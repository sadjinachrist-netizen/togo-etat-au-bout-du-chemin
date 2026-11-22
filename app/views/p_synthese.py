"""Synthèse — le constat, en une page."""
import plotly.graph_objects as go
import streamlit as st

from lib import data as D
from lib import ui

k = D.kpi()
flt = D.sidebar_filters()
pref_all = D.prefectures()
pref = D.f(pref_all, flt)

ui.hero(
    "Open Data Challenge · Défi 01 — données ouvertes du Togo",
    "L'État au bout du chemin",
    "Un Togolais sur six vit dans une préfecture où l'eau, le courant, l'argent et la route "
    "manquent tous les quatre à la fois. Ce tableau de bord mesure, préfecture par préfecture, "
    "la distance qui sépare un habitant des services de base — puis demande si l'investissement "
    "public va bien là où ce manque est le plus grand.",
    [(f"{k['prefectures']}", "préfectures mesurées sur quatre dimensions d'accès", False),
     (f"{ui.fmt(k['points_services'])}", "points de service géolocalisés et recomptés", False),
     (ui.fmt(k["ecart_indice"], 1), "points d'écart entre la préfecture la mieux et la moins bien servie", True),
     (ui.fmt(k["coso_part_pop"], 1, " %"), "de la population couverte par le grand projet d'investissement COSO", True)])

# ------------------------------------------------------------------ 01
ui.section("01", "Ce que disent les données", "Quatre chiffres qui résument le problème.")
b10 = pref_all.nsmallest(10, "indice_acces")
ui.kpis([
    dict(label="L'écart d'accès à l'eau entre préfectures",
         value=f"×{k['eau_ratio']:.0f}", tone="slate",
         sub=f"{ui.fmt(k['eau_max'])} points d'eau pour 10 000 habitants à Assoli, {ui.fmt(k['eau_min'], 2)} dans le Golfe",
         source="Inventaire PEA + PMH, Min. de l'Eau et de l'Hydraulique villageoise"),
    dict(label="Population des 10 préfectures les moins bien servies",
         value=ui.fmt(b10.pop_2022.sum()), tone="red",
         sub=f"soit {ui.fmt(b10.pop_2022.sum() / k['pop_2022'] * 100, 1)} % des Togolais",
         source="RGPH-5 2022, INSEED"),
    dict(label="Taux d'accès à l'électricité à Akébou",
         value="3,7 %", tone="red",
         sub=f"contre {ui.fmt(k['taux_elec_national'], 1)} % au niveau national en {k['annee_elec']}",
         source=f"Abonnés basse tension CEET {k['annee_elec']}"),
    dict(label="Investi par COSO dans 9 préfectures du Nord",
         value="14,3 Md", tone="gold",
         sub=f"{ui.fmt(k['coso_projets'])} ouvrages, {ui.fmt(k['coso_pop_couverte'])} habitants concernés",
         source="Inventaire des réalisations COSO, ANADEB"),
])

# ------------------------------------------------------------------ 02
ui.section("02", "Le classement des 39 préfectures",
           "Indice d'accès composite — 0 = la moins bien servie des 39, 100 = la mieux servie. "
           "Les quatre dimensions pèsent à parts égales.")

d = pref.sort_values("indice_acces")
fig = go.Figure()
for _, r in d.iterrows():
    fig.add_shape(type="line", x0=0, x1=r.indice_acces, y0=r.prefecture, y1=r.prefecture,
                  line=dict(color=ui.C["line"], width=1.6), layer="below")
for reg in [r for r in D.REGION_ORDER if r in set(d.region)]:
    s = d[d.region == reg]
    fig.add_trace(go.Scatter(
        x=s.indice_acces, y=s.prefecture, mode="markers", name=reg,
        marker=dict(size=13, color=ui.REGION_COLORS[reg], line=dict(width=1.3, color="white")),
        customdata=s[["region", "pop_2022", "rang_acces", "coso_projets"]],
        hovertemplate="<b>%{y}</b> · %{customdata[0]}<br>Indice %{x:.1f} — rang %{customdata[2]}/39"
                      "<br>%{customdata[1]:,.0f} habitants"
                      "<br>%{customdata[3]} ouvrages COSO<extra></extra>"))
cos = d[d.coso_couverte]
if len(cos):
    fig.add_trace(go.Scatter(
        x=[1.3] * len(cos), y=cos.prefecture, mode="markers", name="Couverte par COSO",
        marker=dict(symbol="diamond", size=9, color=ui.C["gold"]),
        hovertemplate="<b>%{y}</b> — zone COSO<extra></extra>"))
moy = pref_all.indice_acces.mean()
fig.add_vline(x=moy, line=dict(color=ui.C["muted"], width=1, dash="dot"),
              annotation_text=f"moyenne nationale {ui.fmt(moy, 1)}", annotation_font_size=10)
fig.update_layout(xaxis_title="Indice d'accès (0 – 100)", yaxis_title=None,
                  yaxis=dict(showgrid=False, categoryorder="array",
                             categoryarray=list(d.prefecture)),
                  xaxis=dict(range=[0, 74], showgrid=True, gridcolor=ui.C["line"]))
ui.chart(fig, h=max(420, 22 * len(d) + 110))
ui.source("calcul de l'auteur à partir de 8 jeux ouverts d'opendata.gouv.tg — voir « Méthode & sources »")

ui.note(
    f"<b>Le manque n'est pas une affaire de taille.</b> La corrélation entre l'indice d'accès et la "
    f"population d'une préfecture est de {ui.fmt(pref_all.indice_acces.corr(pref_all.pop_2022), 2)} : autant "
    f"dire nulle. Ce ne sont donc pas les petites préfectures qui sont mal servies, ni les grandes qui "
    f"le sont bien. C'est un problème de <i>placement</i>, pas de densité — et un problème de placement "
    f"se corrige.")

# ------------------------------------------------------------------ 03
ui.section("03", "Trois constats qui tiennent les données",
           "Chacun est vérifiable dans les pages suivantes.")
c1, c2, c3 = st.columns(3)
with c1:
    st.markdown(
        "<div class='reco'><span class='n'>1</span><span class='t'>Les Plateaux, angle mort</span>"
        "<p>Cinq des dix préfectures les moins bien servies sont dans les Plateaux — Akébou, Anié, "
        "Haho, Est-Mono, Moyen-Mono — et <b>aucune n'est couverte</b> par le grand programme "
        "d'investissement communautaire. Akébou ferme le classement national avec 3,7 % d'accès "
        "à l'électricité et zéro ouvrage.</p></div>", unsafe_allow_html=True)
with c2:
    st.markdown(
        "<div class='reco'><span class='n red'>2</span><span class='t'>L'argent va au moins mal servi</span>"
        "<p>Dans la zone COSO elle-même, l'enveloppe par habitant <b>augmente</b> avec le niveau "
        "d'accès (corrélation +0,63). Les quatre préfectures les moins bien servies de la zone "
        "reçoivent 6 061 F CFA par habitant ; les quatre mieux servies, 11 767 F — près du "
        "double.</p></div>", unsafe_allow_html=True)
with c3:
    st.markdown(
        "<div class='reco'><span class='n'>3</span><span class='t'>Le courant, maillon faible</span>"
        "<p>Des quatre dimensions, c'est l'électricité qui creuse le plus l'écart : de 1,9 % d'accès "
        "au Kpendjal à plus de 100 % dans le Zio. Et c'est la seule encore publiée sur un découpage "
        "administratif <b>périmé</b>, qui fond 39 préfectures en 7 zones commerciales.</p></div>",
        unsafe_allow_html=True)

# ------------------------------------------------------------------ 04
ui.section("04", "Comment lire ce tableau de bord")
st.markdown("""
| Page | Ce qu'on y trouve |
|---|---|
| **L'indice d'accès** | La construction de l'indice, la carte des contours, le détail dimension par dimension |
| **Eau, courant, argent, route** | Les quatre dimensions prises séparément, avec leurs sources et leurs angles morts |
| **Les 36 880 points** | Chaque point d'eau, agence, auto-école et agent mobile money sur la carte, filtrable |
| **L'argent va-t-il au manque ?** | Le croisement entre l'indice d'accès et les 813 ouvrages COSO — le cœur de l'analyse |
| **Ce que l'accès change** | Ce que les séries de santé, d'école et de pauvreté disent des mêmes territoires |
| **Méthode & sources** | Le calcul complet, les 17 jeux utilisés avec leurs liens, les cinq limites assumées |
""")

ui.note(
    "<b>Ce que ce tableau de bord ne dit pas.</b> Un point d'eau recensé n'est pas un point d'eau "
    "qui coule : les inventaires PEA et PMH ne publient aucun champ d'état de service, et aucune "
    "date de dernier contrôle. L'électricité n'est publiée que par zone commerciale CEET, pas "
    "par préfecture. Et le réseau mesuré ici est le réseau <i>classé</i> : les pistes rurales, qui "
    "font l'essentiel du dernier kilomètre, n'y figurent pas. Les cinq limites sont détaillées en "
    "annexe — elles ne cassent aucun des trois constats ci-dessus, mais elles en fixent la portée.",
    "gold")
