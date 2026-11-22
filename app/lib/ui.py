"""Charte graphique — L'État au bout du chemin."""
from __future__ import annotations

import base64
from pathlib import Path

import plotly.graph_objects as go
import plotly.io as pio
import streamlit as st

ASSETS = Path(__file__).resolve().parents[1] / "assets"

# ---------------------------------------------------------------- palette
C = {
    "ink": "#0C1A14", "ink_soft": "#1B2E25", "muted": "#67776E", "line": "#E2E9E5",
    "paper": "#F7F9F8", "white": "#FFFFFF",
    "green": "#0E7C56", "green_deep": "#07301F", "green_pale": "#E4F2EB", "mint": "#4ADE80",
    "gold": "#C9962B", "gold_pale": "#FBF2DC",
    "red": "#C0392F", "red_pale": "#FBEAE8",
    "sand": "#B8743A", "slate": "#2F5D78",
}
REGION_COLORS = {"Grand Lomé": "#07301F", "Maritime": "#0E7C56", "Plateaux": "#4E9E7A",
                 "Centrale": "#C9962B", "Kara": "#B8743A", "Savanes": "#C0392F"}
DIM_COLORS = {"Eau": "#2F6F8F", "Électricité": "#C9962B", "Services financiers": "#0E7C56", "Mobilité": "#8A5A3B"}
SEQ = ["#F2F8F5", "#D2E9DD", "#A9D6C1", "#79BDA0", "#4A9E7E", "#23805F", "#07301F"]
SEQ_WARN = ["#FDF4F2", "#F8DCD7", "#F0BBB2", "#E3938A", "#D16B61", "#C0392F", "#7E221B"]

FONT = "'Inter', 'Segoe UI', Helvetica, Arial, sans-serif"
SERIF = "'Fraunces', 'Cambria', Georgia, serif"


@st.cache_data(show_spinner=False)
def armoiries_b64() -> str:
    p = ASSETS / "armoiries_togo.svg"
    return base64.b64encode(p.read_bytes()).decode() if p.exists() else ""


# ---------------------------------------------------------------- thème Plotly
_t = go.layout.Template()
_t.layout = go.Layout(
    font=dict(family=FONT, size=13, color=C["ink"]),
    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
    margin=dict(l=8, r=8, t=38, b=8),
    colorway=[C["green"], C["gold"], C["slate"], C["sand"], C["red"], "#4E9E7A"],
    xaxis=dict(showgrid=False, zeroline=False, linecolor=C["line"], title_font_size=12, tickfont_size=11),
    yaxis=dict(showgrid=True, gridcolor=C["line"], zeroline=False, title_font_size=12, tickfont_size=11),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, x=0, title=None, font_size=11.5),
    title=dict(font=dict(size=14.5, color=C["green_deep"]), x=0, xanchor="left"),
    hoverlabel=dict(bgcolor="white", bordercolor=C["line"], font_size=12, font_family=FONT),
)
pio.templates["etat"] = _t
pio.templates.default = "etat"


def fmt(n, dec: int = 0, suffix: str = "") -> str:
    if n is None or (isinstance(n, float) and n != n):
        return "—"
    return f"{n:,.{dec}f}".replace(",", " ").replace(".", ",") + suffix


# ---------------------------------------------------------------- CSS
def css() -> str:
    return f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&family=Fraunces:opsz,wght@9..144,500;9..144,700;9..144,900&display=swap');

html, body, [class*="css"] {{ font-family: {FONT}; }}
.stApp {{ background: {C['paper']}; }}
.block-container {{ padding-top: 1.1rem; padding-bottom: 3rem; max-width: 1320px; }}

/* ---------- barre latérale ---------- */
section[data-testid="stSidebar"] {{
  background: linear-gradient(175deg, {C['green_deep']} 0%, #0A4030 55%, #08291D 100%);
}}
section[data-testid="stSidebar"] {{ min-width:292px !important; }}
section[data-testid="stSidebar"] * {{ color: #E8F2ED; }}
section[data-testid="stSidebar"] [data-testid="stBaseButton-secondary"] {{
  background: rgba(255,255,255,.09); border:1px solid rgba(255,255,255,.22);
  color:#E8F2ED !important; font-weight:650; font-size:.82rem; }}
section[data-testid="stSidebar"] [data-testid="stBaseButton-secondary"]:hover {{
  background: rgba(74,222,128,.2); border-color:{C['mint']}; color:#fff !important; }}
section[data-testid="stSidebar"] [data-baseweb="select"] > div,
section[data-testid="stSidebar"] [data-baseweb="tag"] {{ border-radius:8px; }}
section[data-testid="stSidebar"] [data-baseweb="select"] > div {{
  background: rgba(255,255,255,.07); border-color: rgba(255,255,255,.18); }}
section[data-testid="stSidebar"] [data-baseweb="tag"] {{ background:{C['green']} !important; }}
section[data-testid="stSidebar"] [data-testid="stCaptionContainer"] p {{
  color: rgba(232,242,237,.62) !important; font-size:.73rem !important; }}
section[data-testid="stSidebar"] a[data-testid="stSidebarNavLink"] {{ border-radius: 9px; margin: 1px 0; }}
section[data-testid="stSidebar"] a[data-testid="stSidebarNavLink"]:hover {{ background: rgba(255,255,255,.07); }}
section[data-testid="stSidebar"] a[aria-current="page"] {{ background: rgba(74,222,128,.16); box-shadow: inset 2px 0 0 {C['mint']}; }}
section[data-testid="stSidebar"] a[aria-current="page"] span {{ color: {C['mint']}; font-weight: 650; }}
section[data-testid="stSidebar"] [data-testid="stSidebarNavSectionHeader"] {{
  color: rgba(232,242,237,.5); letter-spacing: .14em; font-size: .66rem; font-weight: 700; text-transform: uppercase; }}
section[data-testid="stSidebar"] label p {{ font-size: .78rem !important; color: #A9C6B8 !important; font-weight: 600; letter-spacing: .02em; }}
/* armoiries + signature, tout en haut de la barre */
section[data-testid="stSidebar"] [data-testid="stSidebarHeader"] {{
  display:flex; align-items:center; gap:.72rem; padding:1rem 1.1rem .35rem; flex-wrap:nowrap; }}
section[data-testid="stSidebar"] [data-testid="stLogoSpacer"] {{ display:none; }}
section[data-testid="stSidebar"] [data-testid="stSidebarHeader"] img[data-testid="stLogo"] {{
  height:52px !important; width:auto !important; max-width:52px; margin:0;
  filter: drop-shadow(0 2px 7px rgba(0,0,0,.4)); }}
section[data-testid="stSidebar"] [data-testid="stSidebarHeader"]::after {{
  content:"L'État au\A bout du chemin"; white-space:pre;
  font-family:{SERIF}; font-size:1.1rem; font-weight:700; color:#fff; line-height:1.16;
  flex:1 1 auto; }}
section[data-testid="stSidebar"] [data-testid="stSidebarHeader"]::after {{
  background:linear-gradient(transparent 0 0); }}
section[data-testid="stSidebar"] [data-testid="stSidebarCollapseButton"] {{ flex:0 0 auto; }}
.sb-grp {{ color:{C['mint']}; font-size:.64rem; font-weight:800; letter-spacing:.15em; margin:1.1rem 0 .2rem; text-transform:uppercase; }}
.sb-foot {{ margin-top:1.3rem; padding-top:.9rem; border-top:1px solid rgba(255,255,255,.1);
  font-size:.7rem; color:rgba(232,242,237,.6); line-height:1.6; }}

/* ---------- titres ---------- */
h1 {{ font-family:{SERIF}; font-weight:900; letter-spacing:-.025em; color:{C['green_deep']}; font-size:2.25rem; line-height:1.1; }}
h2,h3 {{ font-family:{SERIF}; font-weight:700; color:{C['green_deep']}; letter-spacing:-.01em; }}
.kick {{ color:{C['muted']}; font-size:1.03rem; line-height:1.5; margin:-.3rem 0 1.4rem; max-width:62rem; }}

/* ---------- bandeau d'ouverture ---------- */
.hero {{ position:relative; overflow:hidden; border-radius:18px; padding:2rem 2.2rem 1.8rem;
  background: linear-gradient(135deg, {C['green_deep']} 0%, #0B5138 58%, #0E7C56 100%); color:#fff; margin-bottom:1.5rem; }}
.hero::after {{ content:''; position:absolute; right:-80px; top:-80px; width:320px; height:320px; border-radius:50%;
  background: radial-gradient(circle, rgba(74,222,128,.22) 0%, rgba(74,222,128,0) 70%); }}
.hero .eyebrow {{ font-size:.68rem; letter-spacing:.2em; font-weight:800; color:{C['mint']}; text-transform:uppercase; }}
.hero h1 {{ color:#fff; font-size:2.5rem; margin:.5rem 0 .6rem; max-width:34rem; }}
.hero p {{ color:rgba(255,255,255,.82); font-size:1.02rem; max-width:40rem; margin:0; line-height:1.55; }}
.hero .stats {{ display:flex; gap:2.4rem; margin-top:1.5rem; flex-wrap:wrap; position:relative; z-index:1; }}
.hero .stat .v {{ font-family:{SERIF}; font-size:2rem; font-weight:900; line-height:1; }}
.hero .stat .l {{ font-size:.76rem; color:rgba(255,255,255,.7); margin-top:.3rem; max-width:13rem; line-height:1.35; }}
.hero .stat .v.alert {{ color:{C['mint']}; }}

/* ---------- sections ---------- */
.sect {{ display:flex; align-items:baseline; gap:.7rem; margin:1.9rem 0 .15rem; }}
.sect .n {{ font-family:{SERIF}; font-size:.78rem; font-weight:900; color:{C['green']}; letter-spacing:.1em; }}
.sect .t {{ font-size:.76rem; font-weight:800; letter-spacing:.13em; text-transform:uppercase; color:{C['muted']}; }}
.sect-sub {{ color:{C['muted']}; font-size:.92rem; margin:0 0 .85rem; }}

/* ---------- cartes KPI ---------- */
.kpi {{ background:{C['white']}; border:1px solid {C['line']}; border-radius:13px; padding:.85rem 1rem .7rem; height:100%;
  position:relative; overflow:hidden; transition:transform .12s ease, box-shadow .12s ease; }}
.kpi::before {{ content:''; position:absolute; left:0; top:0; bottom:0; width:3px; background:{C['green']}; }}
.kpi.red::before {{ background:{C['red']}; }}
.kpi.gold::before {{ background:{C['gold']}; }}
.kpi.slate::before {{ background:{C['slate']}; }}
.kpi:hover {{ transform:translateY(-2px); box-shadow:0 6px 20px rgba(7,48,31,.08); }}
.kpi .lbl {{ font-size:.78rem; font-weight:650; color:{C['ink_soft']}; line-height:1.3; }}
.kpi .val {{ font-family:{SERIF}; font-size:clamp(1.25rem, 2.1vw, 1.95rem); font-weight:900;
  color:{C['green_deep']}; line-height:1.08; margin:.25rem 0 .12rem; white-space:nowrap;
  overflow:hidden; text-overflow:ellipsis; }}
.kpi.red .val {{ color:{C['red']}; }} .kpi.gold .val {{ color:#A07714; }} .kpi.slate .val {{ color:{C['slate']}; }}
.kpi .sub {{ font-size:.76rem; color:{C['muted']}; line-height:1.35; }}
.kpi .src {{ font-size:.66rem; color:#9AAAA2; margin-top:.5rem; padding-top:.4rem; border-top:1px dotted {C['line']}; }}

/* ---------- encarts ---------- */
.note {{ border-radius:11px; padding:.85rem 1.1rem; margin:.5rem 0 1.2rem; font-size:.94rem; line-height:1.55;
  background:{C['green_pale']}; border-left:4px solid {C['green']}; color:{C['ink']}; }}
.note.red {{ background:{C['red_pale']}; border-left-color:{C['red']}; }}
.note.gold {{ background:{C['gold_pale']}; border-left-color:{C['gold']}; }}
.note b {{ color:{C['green_deep']}; }}
.note.red b {{ color:{C['red']}; }}

/* ---------- recommandations ---------- */
.reco {{ background:{C['white']}; border:1px solid {C['line']}; border-radius:14px; padding:1rem 1.15rem; margin-bottom:.8rem; }}
.reco .n {{ display:inline-flex; align-items:center; justify-content:center; width:30px; height:30px; border-radius:9px;
  background:{C['green']}; color:#fff; font-family:{SERIF}; font-weight:900; margin-right:.6rem; }}
.reco .n.red {{ background:{C['red']}; }}
.reco .t {{ font-family:{SERIF}; font-weight:700; font-size:1.06rem; color:{C['green_deep']}; }}
.reco .impact {{ font-family:{SERIF}; font-size:1.5rem; font-weight:900; color:{C['red']}; }}
.reco .impact small {{ font-family:{FONT}; font-size:.76rem; color:{C['muted']}; font-weight:500; }}
.reco p {{ margin:.4rem 0 0; font-size:.93rem; color:{C['ink']}; line-height:1.55; }}
.tag {{ display:inline-block; padding:.16rem .6rem; border-radius:999px; font-size:.68rem; font-weight:800; letter-spacing:.05em; }}
.tag.red {{ background:{C['red_pale']}; color:{C['red']}; }}
.tag.green {{ background:{C['green_pale']}; color:{C['green']}; }}
.tag.gold {{ background:{C['gold_pale']}; color:#8A6510; }}

.src-line {{ color:{C['muted']}; font-size:.75rem; margin-top:-.45rem; }}
footer {{ visibility:hidden; }}
div[data-testid="stExpander"] details {{ border:1px solid {C['line']}; border-radius:11px; background:#fff; }}
</style>
"""


def inject() -> None:
    st.markdown(css(), unsafe_allow_html=True)


def hero(eyebrow: str, titre: str, texte: str, stats: list[tuple[str, str, bool]]) -> None:
    s = "".join(f"<div class='stat'><div class='v {'alert' if a else ''}'>{v}</div><div class='l'>{l}</div></div>"
                for v, l, a in stats)
    st.markdown(f"""<div class='hero'><div class='eyebrow'>{eyebrow}</div><h1>{titre}</h1>
<p>{texte}</p><div class='stats'>{s}</div></div>""", unsafe_allow_html=True)


def header(titre: str, kicker: str) -> None:
    st.markdown(f"# {titre}")
    st.markdown(f"<div class='kick'>{kicker}</div>", unsafe_allow_html=True)


def section(num: str, titre: str, sub: str = "") -> None:
    st.markdown(f"<div class='sect'><span class='n'>{num}</span><span class='t'>{titre}</span></div>"
                + (f"<div class='sect-sub'>{sub}</div>" if sub else ""), unsafe_allow_html=True)


def kpis(items: list[dict]) -> None:
    for col, it in zip(st.columns(len(items)), items):
        col.markdown(
            f"<div class='kpi {it.get('tone','')}'><div class='lbl'>{it['label']}</div>"
            f"<div class='val'>{it['value']}</div><div class='sub'>{it.get('sub','')}</div>"
            f"<div class='src'>{it.get('source','')}</div></div>", unsafe_allow_html=True)


def note(txt: str, kind: str = "") -> None:
    st.markdown(f"<div class='note {kind}'>{txt}</div>", unsafe_allow_html=True)


def reco(n: int, titre: str, impact: str, impact_lbl: str, corps: str, tag: str, tag_kind: str, red: bool = False) -> None:
    st.markdown(f"""<div class='reco'><span class='n {'red' if red else ''}'>{n}</span><span class='t'>{titre}</span>
<span class='tag {tag_kind}' style='float:right;margin-top:.4rem'>{tag}</span>
<div style='margin-top:.5rem'><span class='impact'>{impact} <small>{impact_lbl}</small></span></div>
<p>{corps}</p></div>""", unsafe_allow_html=True)


def source(t: str) -> None:
    st.markdown(f"<div class='src-line'>Source : {t}</div>", unsafe_allow_html=True)


def chart(fig: go.Figure, h: int = 380) -> None:
    fig.update_layout(height=h)
    st.plotly_chart(fig, use_container_width=True,
                    config={"displaylogo": False, "locale": "fr",
                            "modeBarButtonsToRemove": ["lasso2d", "select2d", "autoScale2d"]})
