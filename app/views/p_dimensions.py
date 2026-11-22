"""Les quatre dimensions prises séparément."""
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from lib import data as D
from lib import ui

k = D.kpi()
flt = D.sidebar_filters()
pref_all = D.prefectures()
pref = D.f(pref_all, flt)
reg = D.fr(D.regions(), flt)

ui.header("Eau, courant, argent, route",
          "Quatre services, quatre sources, quatre géographies du manque. Elles ne se superposent "
          "pas : la préfecture la mieux dotée en eau est aussi l'une des plus mal desservies en "
          "électricité.")

tabs = st.tabs(["💧 Eau", "⚡ Électricité", "🏦 Services financiers", "🛣️ Mobilité",
                "🔀 Les quatre ensemble"])

# ============================================================ EAU
with tabs[0]:
    ui.section("01", "L'eau — 16 036 points recensés",
               "Postes d'eau autonomes (PEA) et pompes à motricité humaine (PMH), relevés par le "
               "ministère de l'Eau et de l'Hydraulique villageoise.")
    ui.kpis([
        dict(label="Pompes à motricité humaine", value=ui.fmt(k["pmh"]),
             sub="l'essentiel du parc rural", source="Inventaire PMH, Min. Eau"),
        dict(label="Postes d'eau autonomes", value=ui.fmt(k["pea"]), tone="slate",
             sub="réseaux de petite taille, souvent solaires", source="Inventaire PEA, Min. Eau"),
        dict(label="Mieux dotée pour 10 000 hab.", value=ui.fmt(k['eau_max'], 1),
             sub="Assoli (Kara) — un point d'eau pour 141 habitants",
             source="calcul de l'auteur"),
        dict(label="Moins dotée pour 10 000 hab.", value=ui.fmt(k['eau_min'], 2), tone="red",
             sub="Golfe — mais le Golfe est raccordé au réseau TdE : le chiffre mesure "
                 "l'hydraulique villageoise, pas l'accès à l'eau",
             source="calcul de l'auteur"),
    ])
    d = pref.sort_values("eau_10k", ascending=False)
    fig = px.bar(d, x="prefecture", y="eau_10k", color="region",
                 color_discrete_map=ui.REGION_COLORS,
                 labels={"eau_10k": "points d'eau / 10 000 hab.", "prefecture": "", "region": ""})
    fig.update_layout(xaxis_tickangle=-55, xaxis=dict(tickfont_size=10))
    ui.chart(fig, h=400)
    ui.source("Inventaire PEA + PMH, Ministère de l'Eau · population RGPH-5 2022, INSEED")
    ui.note(
        "<b>Un piège de lecture, assumé.</b> Cet indicateur mesure l'<i>hydraulique villageoise</i>. "
        "Dans le Grand Lomé, l'eau arrive par le réseau de la Togolaise des Eaux : y lire « 0,4 point "
        "d'eau pour 10 000 habitants » comme une pénurie serait faux. L'indicateur est pertinent pour "
        "les 37 préfectures rurales, et c'est ainsi qu'il faut le lire. Aucun jeu ouvert ne publie le "
        "taux de desserte TdE par préfecture — c'est la première donnée manquante de ce travail.",
        "gold")

# ============================================================ ÉLECTRICITÉ
with tabs[1]:
    ui.section("02", "L'électricité — publiée sur un découpage périmé",
               "La CEET publie son taux d'accès basse tension par zone commerciale. Ces zones "
               "regroupent plusieurs préfectures et ne suivent pas le découpage administratif actuel.")
    ez = D.elec_zones()
    en = D.elec_national()
    ui.kpis([
        dict(label=f"Taux d'accès national {k['annee_elec']}", value=f"{k['taux_elec_national']} %",
             sub=f"{ui.fmt(en[en.annee == k['annee_elec']].abonnes_bt.iloc[0])} abonnés basse tension",
             source="CEET, via opendata.gouv.tg"),
        dict(label="Zone la moins desservie", value="1,9 %", tone="red",
             sub="Kpendjal + Kpendjal-Ouest — 57 fois moins que la zone la mieux desservie (Zio)",
             source="CEET"),
        dict(label="Zones commerciales publiées", value="33", tone="gold",
             sub="pour 39 préfectures : 6 zones en regroupent 2 à la fois, dont Kpendjal et Oti",
             source="CEET"),
        dict(label="Agences CEET + TdE géolocalisées", value=f"{k['ceet'] + k['tde']}",
             sub=f"{k['ceet']} agences CEET et {k['tde']} agences TdE", tone="slate",
             source="Annuaires des agences, opendata.gouv.tg"),
    ])
    c1, c2 = st.columns([1.3, 1])
    with c1:
        ezf = ez[ez.region.isin(flt["regions"])]
        fig = px.line(ezf.sort_values("annee"), x="annee", y="taux_acces", color="libelle",
                      markers=True, labels={"taux_acces": "taux d'accès BT (%)", "annee": "",
                                            "libelle": ""})
        fig.add_trace(go.Scatter(x=en.annee, y=en.taux_acces, name="Togo", mode="lines+markers",
                                 line=dict(color=ui.C["ink"], width=3.2, dash="dash")))
        ui.chart(fig, h=400)
        ui.source("Abonnés basse tension CEET 2018-2021, opendata.gouv.tg")
    with c2:
        last = ez[ez.annee == ez.annee.max()].sort_values("taux_acces")
        fig = px.bar(last, y="libelle", x="taux_acces", orientation="h", color="region",
                     color_discrete_map=ui.REGION_COLORS,
                     labels={"taux_acces": f"taux d'accès BT {k['annee_elec']} (%)",
                             "libelle": "", "region": ""})
        fig.update_layout(showlegend=False)
        ui.chart(fig, h=400)
        ui.source(f"CEET {k['annee_elec']}")
    ui.note(
        "<b>Deux anomalies à signaler plutôt qu'à masquer.</b> Certaines zones affichent un taux "
        "supérieur à 100 % : le numérateur compte les abonnés, le dénominateur les ménages estimés "
        "— un abonné commercial ou un compteur partagé suffit à faire franchir le seuil. Et le "
        "découpage en zones commerciales étant antérieur à la création des 39 préfectures, les "
        "valeurs de Kpendjal-Ouest, Oti-Sud, Anié, Moyen-Mono et Mô sont <i>héritées</i> de leur "
        "préfecture d'origine. Ce choix est documenté en annexe ; il tire l'indice de ces "
        "préfectures vers le haut, jamais vers le bas.", "red")

# ============================================================ FINANCE
with tabs[2]:
    ui.section("03", "Les services financiers — 20 448 points",
               "Établissements financiers déclarés et agents de mobile money recensés : le réseau "
               "de proximité par lequel passe l'argent.")
    ui.kpis([
        dict(label="Agents mobile money", value=ui.fmt(k["mobile_money"]),
             sub="97 % des points financiers du pays", source="Recensement des agents MM"),
        dict(label="Établissements financiers", value=ui.fmt(k["finance"]), tone="slate",
             sub="banques, IMF, bureaux de change déclarés",
             source="Répertoire des établissements financiers"),
        dict(label="Mieux dotée pour 10 000 hab.", value="59,5",
             sub="Tchaoudjo (Sokodé) — devant le Grand Lomé",
             source="calcul de l'auteur"),
        dict(label="Moins dotée pour 10 000 hab.", value="4,6", tone="red",
             sub="Kpendjal — 13 fois moins que Tchaoudjo",
             source="calcul de l'auteur"),
    ])
    d = pref.sort_values("finance_10k", ascending=False)
    fig = px.bar(d, x="prefecture", y="finance_10k", color="region",
                 color_discrete_map=ui.REGION_COLORS,
                 labels={"finance_10k": "points financiers / 10 000 hab.", "prefecture": "",
                         "region": ""})
    fig.update_layout(xaxis_tickangle=-55, xaxis=dict(tickfont_size=10))
    ui.chart(fig, h=400)
    ui.source("Agents mobile money + établissements financiers, opendata.gouv.tg")
    ui.note(
        "<b>Le mobile money a déjà rattrapé la géographie bancaire.</b> Trente-cinq préfectures sur 39 "
        "comptent plus de 10 points financiers pour 10 000 habitants, un niveau qu'aucun réseau "
        "bancaire physique n'a jamais atteint au Togo. C'est la dimension la moins inégalitaire des "
        "quatre : l'écart entre la mieux et la moins bien dotée est de 13 contre 1, là où il est de "
        "173 contre 1 pour l'eau. Les services financiers ne sont donc plus le frein principal.")

# ============================================================ MOBILITÉ
with tabs[3]:
    ui.section("04", "La mobilité — 3 373 km de routes classées",
               "Longueur mesurée directement sur les tracés publiés (MULTILINESTRING), par sommation "
               "des distances orthodromiques entre points successifs.")
    ui.kpis([
        dict(label="Réseau classé mesuré", value=f"{ui.fmt(k['km_routes'])} km",
             sub="nationales, régionales et préfectorales géoréférencées",
             source="Réseau routier classé, opendata.gouv.tg"),
        dict(label="Mieux dotée", value="1,47 m/hab.",
             sub="Agou (Plateaux)", source="calcul de l'auteur"),
        dict(label="Préfecture sans route classée", value="Mô", tone="red",
             sub="0 mètre géoréférencé — la seule des 39 dans ce cas",
             source="calcul de l'auteur"),
        dict(label="Auto-écoles géolocalisées", value=ui.fmt(k["auto_ecoles"]), tone="slate",
             sub="proxy de l'accès au permis, très concentré dans le Grand Lomé",
             source="Répertoire des auto-écoles"),
    ])
    c1, c2 = st.columns([1.35, 1])
    with c1:
        d = pref.sort_values("m_route_hab", ascending=False)
        fig = px.bar(d, x="prefecture", y="m_route_hab", color="region",
                     color_discrete_map=ui.REGION_COLORS,
                     labels={"m_route_hab": "mètres de route classée / hab.", "prefecture": "",
                             "region": ""})
        fig.update_layout(xaxis_tickangle=-55, xaxis=dict(tickfont_size=10))
        ui.chart(fig, h=400)
        ui.source("Réseau routier classé, opendata.gouv.tg · population RGPH-5 2022")
    with c2:
        ae = pref.nlargest(10, "auto_ecoles")[["prefecture", "auto_ecoles", "region"]]
        fig = px.bar(ae.sort_values("auto_ecoles"), y="prefecture", x="auto_ecoles",
                     orientation="h", color="region", color_discrete_map=ui.REGION_COLORS,
                     labels={"auto_ecoles": "auto-écoles", "prefecture": "", "region": ""})
        fig.update_layout(showlegend=False)
        ui.chart(fig, h=400)
        ui.source("Répertoire des auto-écoles, opendata.gouv.tg")
    ui.note(
        "<b>Mô n'est pas une donnée manquante : c'est un résultat.</b> Aucune route classée ne "
        "traverse la préfecture de Mô dans le jeu publié, et la préfecture est absente de plusieurs "
        "autres jeux géolocalisés. Le réseau mesuré ici est par ailleurs le réseau <i>classé</i> : "
        "il ignore les pistes rurales, qui portent l'essentiel du dernier kilomètre. La valeur à "
        "retenir n'est donc pas « combien de route » mais « quelle préfecture est hors du réseau "
        "structurant » — et Mô l'est entièrement.", "red")

# ============================================================ ENSEMBLE
with tabs[4]:
    ui.section("05", "Les quatre dimensions ne se superposent pas",
               "Si elles mesuraient la même chose, les points s'aligneraient. Ils ne s'alignent pas.")
    cols = {n: v[0] for n, v in D.DIMS.items()}
    corr = pref_all[list(cols.values())].corr()
    corr.index = corr.columns = list(cols)
    fig = px.imshow(corr.round(2), text_auto=True, color_continuous_scale=ui.SEQ,
                    zmin=-0.3, zmax=1, aspect="auto")
    fig.update_layout(coloraxis_showscale=False, xaxis_title=None, yaxis_title=None)
    c1, c2 = st.columns([1, 1.25])
    with c1:
        ui.chart(fig, h=360)
        ui.source("corrélations de Pearson sur les 39 préfectures — calcul de l'auteur")
    with c2:
        x, y = st.columns(2)
        dx = x.selectbox("Axe horizontal", list(D.DIMS), index=1)
        dy = y.selectbox("Axe vertical", list(D.DIMS), index=0)
        fg = px.scatter(pref, x=cols[dx], y=cols[dy], color="region", size="pop_2022",
                        color_discrete_map=ui.REGION_COLORS, hover_name="prefecture",
                        size_max=34, labels={cols[dx]: D.DIMS[dx][2], cols[dy]: D.DIMS[dy][2],
                                             "region": ""})
        ui.chart(fg, h=360)
        ui.source("calcul de l'auteur — la taille des bulles est la population 2022")
    r_ef = pref_all.taux_electricite.corr(pref_all.eau_10k)
    ui.note(
        f"<b>Électricité et eau varient en sens inverse</b> (corrélation {ui.fmt(r_ef, 2)}). Ce n'est pas "
        f"un paradoxe : l'hydraulique villageoise se déploie précisément là où le réseau électrique "
        f"n'arrive pas, et le Grand Lomé est électrifié sans avoir besoin de pompes. Un indice "
        f"composite a donc un sens ici — il ne redit pas quatre fois la même chose. Et une préfecture "
        f"faible sur <i>toutes</i> les dimensions à la fois, comme Akébou ou Kpendjal-Ouest, l'est "
        f"pour de bonnes raisons, pas par artefact de calcul.")
