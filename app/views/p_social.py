"""Ce que l'accès change — santé, école, pauvreté."""
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from lib import data as D
from lib import ui

flt = D.sidebar_filters()
pref_all = D.prefectures()
reg = D.regions()
regf = D.fr(reg, flt)

ui.header("Ce que l'accès change",
          "L'indice d'accès mesure des infrastructures. Les séries sanitaires, scolaires et de "
          "pauvreté mesurent des résultats. Les unes et les autres ne sont pas publiées au même "
          "niveau géographique — ce qui limite ce qu'on peut honnêtement en conclure, et ce qu'on "
          "peut en dire est dit ici sans forcer.")

ui.note(
    "<b>Avertissement de lecture.</b> L'indice d'accès est calculé par préfecture (39 unités). Les "
    "séries de santé et d'école ne sont publiées que par région (6 unités) ; la pauvreté ne l'est "
    "qu'au niveau national. On ne peut donc pas tester une relation statistique sérieuse : six "
    "points ne font pas une corrélation. Ce qui suit est une mise en regard, pas une démonstration "
    "de causalité — et c'est délibérément présenté comme tel.", "gold")

# ------------------------------------------------------------------ 01
ui.section("01", "La pauvreté, seule série nationale disponible")
pvt = D.pauvrete()
pv = pvt[pvt.indicateur == "Taux de pauvreté"].sort_values("annee")
a0, v0 = int(pv.annee.iloc[0]), pv.value.iloc[0]
a1, v1 = int(pv.annee.iloc[-1]), pv.value.iloc[-1]


def _der(nom, defaut="—"):
    r = pvt[pvt.indicateur.str.startswith(nom)].sort_values("annee")
    return (r.value.iloc[-1], int(r.annee.iloc[-1])) if len(r) else (defaut, 0)


gini, a_gini = _der("Indice GINI")
seuil, a_seuil = _der("Population sous le seuil")
c1, c2 = st.columns([1, 1.3])
with c1:
    ui.kpis([dict(label=f"Taux de pauvreté {a0}", value=ui.fmt(v0, 1, " %"), tone="red",
                  sub="première année publiée de la série",
                  source="QUIBB / EHCVM, INSEED")])
    st.markdown("<div style='height:.6rem'></div>", unsafe_allow_html=True)
    ui.kpis([dict(label=f"Taux de pauvreté {a1}", value=ui.fmt(v1, 1, " %"), tone="",
                  sub=f"{v1 - v0:+.1f} points en {a1 - a0} ans",
                  source="QUIBB / EHCVM, INSEED")])
    st.markdown("<div style='height:.6rem'></div>", unsafe_allow_html=True)
    ui.kpis([dict(label=f"Indice de Gini {a_gini}", value=ui.fmt(gini, 2), tone="gold",
                  sub=f"{ui.fmt(seuil, 1)} % de la population sous le seuil international de 2 $/jour",
                  source="INSEED, via opendata.gouv.tg")])
with c2:
    fig = px.line(pv, x="annee", y="value", markers=True,
                  labels={"value": "taux de pauvreté (%)", "annee": ""})
    fig.update_traces(line=dict(color=ui.C["red"], width=3), marker=dict(size=10))
    fig.update_yaxes(range=[40, 68])
    ui.chart(fig, h=300)
    ui.source("Série du taux de pauvreté, INSEED — opendata.gouv.tg")

pop0, pop1 = 6.19e6, 8.10e6
n0, n1 = pop0 * v0 / 100, pop1 * v1 / 100
ui.note(
    f"<b>Le taux recule, le nombre de personnes pauvres beaucoup moins.</b> La pauvreté passe de "
    f"{ui.fmt(v0, 1)} % en {a0} à {ui.fmt(v1, 1)} % en {a1}. Mais sur la même période la population togolaise "
    f"a augmenté de 30,8 % : rapporté aux effectifs, cela fait passer d'environ "
    f"{ui.fmt(n0 / 1e6, 2)} million de personnes pauvres à {ui.fmt(n1 / 1e6, 2)} million — "
    f"un recul bien plus modeste que celui du pourcentage. Aucune ventilation régionale n'est "
    f"publiée dans ce jeu, ce qui empêche de rapprocher la pauvreté de l'indice d'accès.")

# ------------------------------------------------------------------ 02
ui.section("02", "La scolarisation au primaire, par région",
           "Taux net de scolarisation publié par l'INSEED, ventilé par région et par sexe.")
sc = D.serie("scolarisation")
sct = sc[(sc.sexe == "Total") & (sc.region != "Togo")]
tg = sc[(sc.sexe == "Total") & (sc.region == "Togo")]
c1, c2 = st.columns([1.3, 1])
with c1:
    scf = sct[sct.region.isin(flt["regions"])] if len(flt["regions"]) < 6 else sct
    fig = px.line(scf.sort_values("annee"), x="annee", y="value", color="region", markers=True,
                  color_discrete_map=ui.REGION_COLORS,
                  labels={"value": "taux net de scolarisation (%)", "annee": "", "region": ""})
    fig.add_trace(go.Scatter(x=tg.annee, y=tg.value, name="Togo", mode="lines",
                             line=dict(color=ui.C["ink"], width=3, dash="dash")))
    ui.chart(fig, h=380)
    ui.source("Taux net de scolarisation au primaire par région, INSEED — opendata.gouv.tg")
with c2:
    last = sct[sct.annee == sct.annee.max()].copy()
    idx = reg[["region", "indice_acces"]].copy()
    m = last.merge(idx, on="region", how="left").dropna()
    fig = px.scatter(m, x="indice_acces", y="value", color="region", size=[34] * len(m),
                     color_discrete_map=ui.REGION_COLORS, text="region", size_max=22,
                     labels={"indice_acces": "indice d'accès régional", "value":
                             f"taux net de scolarisation {int(sct.annee.max())} (%)", "region": ""})
    fig.update_traces(textposition="top center", textfont_size=10)
    fig.update_layout(showlegend=False)
    ui.chart(fig, h=380)
    ui.source("INSEED × indice calculé par l'auteur — 6 points seulement")

rs = m.indice_acces.corr(m.value) if len(m) > 2 else float("nan")
rs_txt = ("+" if rs >= 0 else "") + ui.fmt(rs, 2)
ui.note(
    f"<b>Les Savanes sont dernières sur les deux tableaux.</b> Avec un indice d'accès régional de "
    f"{ui.fmt(reg[reg.region == 'Savanes'].indice_acces.iloc[0], 1)} — le plus bas des six régions — les "
    f"Savanes affichent aussi le taux net de scolarisation le plus faible "
    f"({ui.fmt(last[last.region == 'Savanes'].value.iloc[0], 1)} % contre "
    f"{ui.fmt(tg[tg.annee == tg.annee.max()].value.iloc[0], 1)} % au niveau national). Mais il faut "
    f"s'arrêter là : sur les six régions, la corrélation entre indice d'accès et scolarisation vaut "
    f"{rs_txt}, c'est-à-dire rien. Le Kara, région au meilleur indice d'accès, n'est pas la mieux "
    f"scolarisée ; le Grand Lomé, moyen sur l'indice, l'est largement. <b>Il n'y a donc pas de "
    f"relation visible à ce niveau d'agrégation</b> — ce qui est en soi un résultat : il faudrait "
    f"la scolarisation publiée par préfecture pour tester sérieusement la question.")

ui.note(
    "<b>Une anomalie dans la source, signalée plutôt que recopiée.</b> La série ventilée par sexe "
    "donne, pour « Féminin », des taux supérieurs à 100 % dans six régions sur sept — "
    "mathématiquement impossible pour un taux <i>net</i>, qui ne compte que les enfants de l'âge "
    "officiel. Au Kara, le Total publié (95,4 %) est même inférieur à ses deux composantes "
    "(95,6 % et 105,5 %), ce qu'aucune moyenne pondérée ne permet. La ventilation par sexe de ce "
    "jeu est donc inutilisable en l'état ; seule la colonne « Total » est exploitée ici, et "
    "l'anomalie mérite un signalement au producteur.", "red")

# ------------------------------------------------------------------ 03
ui.section("03", "L'offre de soins, par région",
           "Nombre de formations sanitaires, de lits, et nombre d'habitants par lit.")
sd = D.serie("sante_densite")
ind = st.selectbox("Indicateur sanitaire", sorted(sd.indicateur.unique()),
                   index=sorted(sd.indicateur.unique()).index("Nombre de personnes par lit")
                   if "Nombre de personnes par lit" in set(sd.indicateur) else 0)
sub = sd[(sd.indicateur == ind) & (sd.region != "Togo")]
c1, c2 = st.columns([1.3, 1])
with c1:
    subf = sub[sub.region.isin(flt["regions"])] if len(flt["regions"]) < 6 else sub
    fig = px.bar(subf.sort_values("annee"), x="region", y="value", color="annee",
                 barmode="group", color_continuous_scale=ui.SEQ,
                 labels={"value": ind, "region": "", "annee": "année"})
    fig.update_layout(xaxis=dict(categoryorder="array", categoryarray=D.REGION_ORDER))
    ui.chart(fig, h=380)
    ui.source("Densité sanitaire, Min. de la Santé — opendata.gouv.tg")
with c2:
    sf = D.serie("sante_formations")
    tot = (sf[sf.region != "Togo"].groupby(["annee"], as_index=False).value.sum())
    fig = px.line(tot, x="annee", y="value", markers=True,
                  labels={"value": "formations sanitaires (toutes catégories)", "annee": ""})
    fig.update_traces(line=dict(color=ui.C["green"], width=3), marker=dict(size=9))
    ui.chart(fig, h=380)
    ui.source("Inventaire des formations sanitaires, Min. de la Santé")

# ------------------------------------------------------------------ 04
ui.section("04", "Le tableau de bord régional, tout ensemble",
           "Les six régions, leurs indices d'accès, leurs résultats sociaux et l'investissement "
           "COSO reçu — sur une seule ligne chacune.")
t = regf[["region", "pop_2022", "part_population", "indice_acces", "eau_10k", "finance_10k",
          "m_route_hab", "coso_projets", "coso_montant"]].copy()
sco = sct[sct.annee == sct.annee.max()][["region", "value"]].rename(
    columns={"value": "scolarisation"})
t = t.merge(sco, on="region", how="left")
t["coso_montant"] = (t.coso_montant / 1e9).round(2)
t["pop_2022"] = t.pop_2022.map(ui.fmt)
st.dataframe(
    t.rename(columns={"region": "Région", "pop_2022": "Population 2022",
                      "part_population": "% du pays", "indice_acces": "Indice d'accès",
                      "eau_10k": "Eau /10 000 hab.", "finance_10k": "Finance /10 000 hab.",
                      "m_route_hab": "Route m/hab.", "coso_projets": "Ouvrages COSO",
                      "coso_montant": "COSO (Md F)", "scolarisation": "Scolarisation (%)"}),
    hide_index=True, use_container_width=True)
ui.source("RGPH-5 2022 · INSEED · COSO/ANADEB · indices calculés par l'auteur")

ui.note(
    "<b>Le Kara est le contre-exemple utile.</b> C'est la région au meilleur indice d'accès "
    f"({ui.fmt(reg[reg.region == 'Kara'].indice_acces.iloc[0], 1)}), portée par l'hydraulique villageoise "
    "— et pourtant elle n'est ni la plus riche ni la mieux scolarisée. L'accès physique à un "
    "service est une condition, pas un résultat : un forage posé ne garantit ni son entretien, ni "
    "son usage, ni l'école à côté. C'est la raison pour laquelle cet indice est présenté comme un "
    "indicateur de <i>couverture</i>, et jamais comme un indicateur de bien-être.")
