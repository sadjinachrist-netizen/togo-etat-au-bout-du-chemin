"""L'État au bout du chemin — où les services publics s'arrêtent au Togo.
Open Data Challenge · Défi 01 — Togo AI Lab / MESPTN."""
from pathlib import Path

import streamlit as st

st.set_page_config(page_title="L'État au bout du chemin · Togo",
                   page_icon="🇹🇬", layout="wide",
                   initial_sidebar_state="expanded")

from lib import data as D  # noqa: E402
from lib import ui  # noqa: E402

ui.inject()

# ------------------------------------- armoiries, tout en haut de la barre
st.logo(str(Path(__file__).parent / "assets" / "armoiries_togo.svg"), size="large")

PAGES = {
    "Le constat": [
        st.Page("views/p_synthese.py", title="Synthèse", icon=":material/flag:", default=True),
        st.Page("views/p_indice.py", title="L'indice d'accès", icon=":material/stacked_line_chart:"),
    ],
    "Les quatre dimensions": [
        st.Page("views/p_dimensions.py", title="Eau, courant, argent, route", icon=":material/grid_view:"),
        st.Page("views/p_territoire.py", title="Les 36 880 points", icon=":material/map:"),
    ],
    "L'action publique": [
        st.Page("views/p_coso.py", title="L'argent va-t-il au manque ?", icon=":material/account_balance:"),
        st.Page("views/p_social.py", title="Ce que l'accès change", icon=":material/school:"),
    ],
    "Annexes": [
        st.Page("views/p_methode.py", title="Méthode & sources", icon=":material/library_books:"),
    ],
}

nav = st.navigation(PAGES)
nav.run()

# ------------------------------- pied de page latéral (après les filtres)
k = D.kpi()
st.sidebar.markdown(
    f"""<div class='sb-foot'>
<b style="color:#4ADE80">Données</b><br/>
17 jeux ouverts · {k['prefectures']} préfectures<br/>
opendata.gouv.tg — 100 % des jeux<br/>
Contours : geoBoundaries (OSM)<br/><br/>
<b style="color:#4ADE80">Auteur</b><br/>
SADJINA Christ<br/>
Open Data Challenge · Défi 01<br/>
Togo AI Lab — novembre 2026
</div>""", unsafe_allow_html=True)
