"""L'argent public va-t-il là où le manque est ? — croisement indice × COSO."""
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from lib import data as D
from lib import ui

k = D.kpi()
flt = D.sidebar_filters()
pref_all = D.prefectures()
pref = D.f(pref_all, flt)
cs = D.coso()

ui.header("L'argent va-t-il là où le manque est ?",
          "Le projet COSO (Cohésion sociale des régions Nord du Togo, ANADEB) a livré 813 ouvrages "
          "communautaires pour 14,3 milliards de F CFA. Son inventaire est publié, géolocalisé, "
          "chiffré — c'est le seul jeu ouvert qui permette de confronter une dépense réelle à un "
          "besoin mesuré. C'est ce que fait cette page.")

couv = pref_all[pref_all.coso_couverte].sort_values("indice_acces")
ui.section("01", "Ce que COSO a financé")
ui.kpis([
    dict(label="Ouvrages inventoriés", value=ui.fmt(k["coso_projets"]),
         sub="forages, centres communautaires, salles de classe, marchés, pistes",
         source="Inventaire des réalisations COSO, ANADEB"),
    dict(label="Montant total", value="14,3 Md F", tone="gold",
         sub=f"soit {ui.fmt(k['coso_montant'] / k['coso_pop_couverte'])} F par habitant de la zone",
         source="Inventaire COSO, ANADEB"),
    dict(label="Préfectures couvertes", value=f"{k['coso_prefectures']} / 39", tone="slate",
         sub=f"{ui.fmt(k['coso_pop_couverte'])} habitants, {k['coso_part_pop']} % de la population",
         source="COSO × RGPH-5 2022"),
    dict(label="Indice d'accès moyen de la zone", value=f"{k['coso_indice_moyen']}",
         sub=f"contre {k['non_coso_indice_moyen']} hors zone — le ciblage régional est juste",
         source="calcul de l'auteur"),
])

ui.note(
    f"<b>Première chose à dire, et elle est à l'honneur du projet : le ciblage régional est bon.</b> "
    f"La zone COSO affiche un indice d'accès moyen de {k['coso_indice_moyen']} contre "
    f"{k['non_coso_indice_moyen']} pour le reste du pays. Le programme a donc bien été implanté dans "
    f"la moitié la plus mal servie du Togo. La question qui suit n'est pas celle du <i>où</i> au sens "
    f"large, mais celle de la répartition <i>à l'intérieur</i> de la zone, et celle des préfectures "
    f"aussi mal servies qui restent dehors.")

# ------------------------------------------------------------------ 02
ui.section("02", "Le graphique central",
           "Chaque point est une préfecture. À gauche, les moins bien servies. En haut, celles qui "
           "ont reçu le plus par habitant. Si l'argent suivait le manque, le nuage descendrait de "
           "gauche à droite.")

d = pref_all.copy()
d["statut"] = d.coso_couverte.map({True: "Couverte par COSO", False: "Hors zone COSO"})
fig = px.scatter(
    d, x="indice_acces", y="coso_fcfa_hab", color="statut", size="pop_2022", size_max=42,
    hover_name="prefecture",
    color_discrete_map={"Couverte par COSO": ui.C["gold"], "Hors zone COSO": "#C6D4CC"},
    labels={"indice_acces": "indice d'accès (0 = le moins bien servi des 39)",
            "coso_fcfa_hab": "F CFA investis par habitant", "statut": "", "pop_2022": "population"},
    hover_data={"region": True, "rang_acces": True, "coso_projets": True, "pop_2022": ":,.0f"})
cv = d[d.coso_couverte]
z = go.Scatter(x=cv.indice_acces, y=cv.coso_fcfa_hab, mode="text", text=cv.prefecture,
               textposition="top center", textfont=dict(size=10.5, color=ui.C["ink_soft"]),
               showlegend=False, hoverinfo="skip")
fig.add_trace(z)
# tendance intra-zone
import numpy as np  # noqa: E402

a, b = np.polyfit(cv.indice_acces, cv.coso_fcfa_hab, 1)
xs = np.array([cv.indice_acces.min() - 2, cv.indice_acces.max() + 2])
fig.add_trace(go.Scatter(x=xs, y=a * xs + b, mode="lines", name="tendance dans la zone COSO",
                         line=dict(color=ui.C["red"], width=2.2, dash="dash"),
                         hovertemplate="tendance : +%{y:.0f} F/hab<extra></extra>"))
fig.update_layout(yaxis_title="F CFA investis par habitant", legend=dict(y=1.06))
ui.chart(fig, h=470)
ui.source("Inventaire COSO (ANADEB) · indice calculé par l'auteur · population RGPH-5 2022, INSEED")

r = cv.coso_fcfa_hab.corr(cv.indice_acces)
ui.note(
    f"<b>La pente monte, et c'est le résultat principal de ce travail.</b> À l'intérieur même de la "
    f"zone COSO, la corrélation entre l'investissement par habitant et le niveau d'accès est de "
    f"<b>{r:+.2f}</b>. Autrement dit, plus une préfecture de la zone était <i>déjà</i> bien servie, "
    f"plus elle a reçu par habitant. Les quatre les plus mal servies de la zone — Kpendjal-Ouest, "
    f"Kpendjal, Tandjoaré, Tchamba — ont reçu <b>6 061 F par habitant</b>. Les quatre les mieux "
    f"servies — Oti, Cinkassé, Téné, Binah — en ont reçu <b>11 767 F</b>, soit 1,9 fois plus. "
    f"Cinkassé, 11<sup>e</sup> au classement national de l'accès, est la préfecture la mieux dotée "
    f"de la zone avec 23 002 F par habitant ; Kpendjal-Ouest, 38<sup>e</sup> sur 39, en reçoit "
    f"quatre fois moins.", "red")

# ------------------------------------------------------------------ 03
ui.section("03", "Les deux écarts, chiffrés")
c1, c2 = st.columns([1, 1])
with c1:
    st.markdown("**À l'intérieur de la zone — l'ordre est inversé**")
    t = couv[["prefecture", "region", "rang_acces", "indice_acces", "coso_projets",
              "coso_fcfa_hab"]].copy()
    t["coso_fcfa_hab"] = t.coso_fcfa_hab.map(lambda v: ui.fmt(v) + " F")
    st.dataframe(t.rename(columns={"prefecture": "Préfecture", "region": "Région",
                                   "rang_acces": "Rang /39", "indice_acces": "Indice",
                                   "coso_projets": "Ouvrages", "coso_fcfa_hab": "F/habitant"}),
                 hide_index=True, use_container_width=True)
    st.caption("Classées du moins bien servi au mieux servi. La colonne F/habitant devrait décroître.")
with c2:
    st.markdown("**Hors zone — sept préfectures aussi mal servies, sans un franc**")
    b10 = pref_all.nsmallest(10, "indice_acces")
    hors = b10[~b10.coso_couverte][["prefecture", "region", "rang_acces", "indice_acces",
                                    "pop_2022"]].copy()
    hors["pop_2022"] = hors.pop_2022.map(ui.fmt)
    st.dataframe(hors.rename(columns={"prefecture": "Préfecture", "region": "Région",
                                      "rang_acces": "Rang /39", "indice_acces": "Indice",
                                      "pop_2022": "Population 2022"}),
                 hide_index=True, use_container_width=True)
    st.caption(f"Parmi les 10 préfectures les moins bien servies du pays, {k['bottom10_dans_coso']} "
               f"seulement sont couvertes par COSO. Les 7 autres totalisent "
               f"{ui.fmt(b10[~b10.coso_couverte].pop_2022.sum())} habitants.")

ui.note(
    "<b>Ce reproche doit être tempéré, et il l'est ici.</b> COSO est un projet des régions Nord : "
    "son mandat géographique exclut les Plateaux par construction, et il serait malhonnête de lui "
    "reprocher Akébou ou Haho. Le constat juste est en deux parties. À l'intérieur de son mandat, "
    "la répartition de COSO est inversée par rapport au besoin mesuré — cela, le projet peut le "
    "corriger. Et hors de son mandat, cinq préfectures des Plateaux aussi mal servies que celles du "
    "Kpendjal n'ont <i>aucun</i> programme équivalent identifiable dans les données ouvertes — cela, "
    "seule une décision nationale peut le corriger.", "gold")

# ------------------------------------------------------------------ 04
ui.section("04", "Ce que COSO a construit", "Par secteur et par nature d'ouvrage.")
csf = cs[cs.prefecture_key.isin(pref.prefecture_key)] if len(pref) < 39 else cs
c1, c2 = st.columns([1.15, 1])
with c1:
    t = (csf.groupby("secteur", as_index=False)
         .agg(ouvrages=("id", "count"), montant=("montant", "sum"))
         .sort_values("montant"))
    fig = px.bar(t, y="secteur", x="montant", orientation="h",
                 labels={"montant": "F CFA engagés", "secteur": ""},
                 color_discrete_sequence=[ui.C["green"]], text="ouvrages")
    fig.update_traces(texttemplate="%{text} ouvrages", textposition="outside", cliponaxis=False,
                      textfont_size=10)
    ui.chart(fig, h=400)
    ui.source("Inventaire COSO, ANADEB")
with c2:
    t2 = (csf.groupby("type", as_index=False).agg(n=("id", "count"))
          .nlargest(10, "n").sort_values("n"))
    fig = px.bar(t2, y="type", x="n", orientation="h", labels={"n": "ouvrages", "type": ""},
                 color_discrete_sequence=[ui.C["gold"]])
    ui.chart(fig, h=400)
    ui.source("Inventaire COSO, ANADEB")

ui.section("05", "Où sont les 813 ouvrages")
fig = px.scatter_map(csf, lat="lat", lon="lon", color="secteur", size="montant", size_max=20,
                     hover_name="intitule", zoom=7.45, center=dict(lat=10.3, lon=0.45),
                     map_style="carto-positron",
                     hover_data={"prefecture_key": True, "localite": True, "montant": ":,.0f",
                                 "beneficiaires": ":,.0f", "lat": False, "lon": False},
                     labels={"secteur": ""})
fig.update_traces(marker=dict(opacity=0.75))
fig.update_layout(margin=dict(l=0, r=0, t=0, b=0),
                  legend=dict(orientation="h", y=1.02, x=0, bgcolor="rgba(255,255,255,.82)"))
ui.chart(fig, h=560)
ui.source("Inventaire géolocalisé des réalisations COSO, ANADEB — opendata.gouv.tg")

# ------------------------------------------------------------------ 06
ui.section("06", "Trois recommandations",
           "Chacune est chiffrée sur les données de cette page, et chacune a un destinataire.")
ui.reco(1, "Réaligner le solde de COSO sur l'indice d'accès",
        "+5 706 F", "par habitant à rattraper au Kpendjal-Ouest",
        "Pour que les quatre préfectures les plus mal servies de la zone atteignent le niveau par "
        "habitant des quatre mieux servies, il faudrait y réorienter <b>3,1 milliards de F CFA</b> "
        "— soit 22 % de l'enveloppe déjà engagée. Appliquer la règle sur les seuls décaissements "
        "restants suffirait à redresser la pente sans rouvrir un seul marché. "
        "<i>Destinataire : ANADEB, comité de pilotage COSO.</i>",
        "ANADEB", "gold")
ui.reco(2, "Ouvrir un volet Plateaux-Nord",
        "814 000", "habitants dans cinq préfectures sans programme",
        "Akébou, Anié, Haho, Est-Mono et Moyen-Mono figurent parmi les dix préfectures les moins "
        "bien servies du pays et ne relèvent d'aucun programme d'investissement communautaire "
        "identifiable dans les données ouvertes. Akébou cumule le dernier rang national, 3,7 % "
        "d'accès à l'électricité et zéro ouvrage. Un volet calqué sur COSO y toucherait 10,1 % de "
        "la population togolaise. <i>Destinataire : ministère du Développement à la base.</i>",
        "Priorité nationale", "red", red=True)
ui.reco(3, "Publier l'électricité par préfecture, et l'eau par desserte",
        "19 / 39", "préfectures dont le point noir est l'électricité",
        "L'électricité est le premier point faible de 19 préfectures sur 39, et c'est la seule "
        "dimension encore publiée sur un découpage commercial antérieur aux 39 préfectures : six "
        "zones en regroupent deux à la fois, ce qui rend cinq préfectures invisibles. Publier le "
        "taux d'accès BT par préfecture, et le taux de desserte TdE par préfecture, suffirait à "
        "rendre cet indice entièrement reproductible — et à rendre arbitrables les deux "
        "recommandations précédentes. <i>Destinataires : CEET, TdE, MESPTN.</i>",
        "Donnée manquante", "green")
