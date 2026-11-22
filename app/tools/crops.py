"""Captures ciblees des visuels utilises dans le rapport PPTX."""
import sys, time
from pathlib import Path
from playwright.sync_api import sync_playwright

BASE = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8519"
OUT = Path(__file__).resolve().parents[2] / "rapport" / "captures"
OUT.mkdir(parents=True, exist_ok=True)

# (nom, chemin, selecteur, index)
SHOTS = [
    ("classement",  "/",             ".stPlotlyChart", 0),
    ("carte_indice", "/p_indice",    ".stPlotlyChart", 0),
    ("decomposition", "/p_indice",   ".stPlotlyChart", 1),
    ("eau",         "/p_dimensions", ".stPlotlyChart", 0),
    ("points",      "/p_territoire", ".stPlotlyChart", 0),
    ("coso_scatter", "/p_coso",      ".stPlotlyChart", 0),
    ("coso_carte",  "/p_coso",       ".stPlotlyChart", 3),
    ("coso_secteur", "/p_coso",      ".stPlotlyChart", 1),
]

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 1500, "height": 1000}, device_scale_factor=2)
    cur = None
    for nom, path, sel, idx in SHOTS:
        if path != cur:
            pg.goto(BASE + path, wait_until="networkidle")
            time.sleep(5)
            try:
                pg.wait_for_selector(".js-plotly-plot .main-svg", timeout=20000)
            except Exception:
                pass
            time.sleep(4)
            cur = path
        els = pg.query_selector_all(sel)
        if idx >= len(els):
            print(f"!! {nom}: {len(els)} elements seulement")
            continue
        els[idx].scroll_into_view_if_needed()
        time.sleep(2.5)
        els[idx].screenshot(path=str(OUT / f"{nom}.png"))
        print(f"{nom:16s} ok")
    b.close()
